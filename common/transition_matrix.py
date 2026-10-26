"""Shared Markov-model utilities for the per-method transition-matrix notebooks.

Used by EE/analysis/, HREX/analysis/, Plain_MD/analysis/, and REDs/analysis/'s
transition_matrix.ipynb / transition_matrix_res.ipynb, which all built a
2-state or 8-state (3-residue) cis/trans Markov model out of extracted omega
angles and estimated its stationary distribution and implied timescale. The
five copies of this code were identical except for the state-index encoding,
which depends on the number of lambda/replica states each method samples
(HREX: 6, EE: 4, REDs: 3, Plain_MD: none) -- `state_to_index_vectorized` /
`index_to_state` take that count as a parameter instead of hardcoding it.

Metadynamics keeps its own local copies: its pipeline (bootstrap resampling
over a single long trajectory) diverges enough structurally that forcing it
through the same higher-level functions isn't a good fit, even though a few
of its primitives happen to match these.
"""

import numpy as np
from joblib import Parallel, delayed
from tqdm import tqdm


def omega2cistrans(omega):
    """Converts a sequence of float omega angles (in degrees) to an array of ints: 0 cis and 1 trans."""

    shifted_omega = (omega + 90.0) % 360.0 - 90.0  # shift into (-90, 270) range to avoid periodic boundaries

    cistrans = np.where(shifted_omega > 90.0, 1, 0).astype(int)
    return cistrans


def state_to_index_vectorized(all_state, n_lambda_states=None):
    """
    Converts an (N, M, k) or (N, M, k+1) array of states into (N, M) flat indices.

    Without `n_lambda_states`, `all_state` holds k binary bits (0 or 1) per
    snapshot, and the index is their base-2 value, in [0, 2**k - 1].

    With `n_lambda_states` (= n), the last of the k+1 entries is an extra
    state x in [0, n-1] (e.g. a lambda/replica index) and the first k
    entries are binary bits; the index is n * (base-2 value of the bits) + x,
    in [0, n * 2**k - 1].

    Rows containing a NaN anywhere remain NaN in the output.

    Parameters
    ----------
    all_state : array-like
        An array of shape (N, M, k) (or (N, M, k+1) if `n_lambda_states` is given).
    n_lambda_states : int, optional
        Number of values the trailing extra state can take, if present.

    Returns
    -------
    indexed_states : ndarray
        A float array of shape (N, M). Rows with NaNs in the input remain NaN.
    """
    all_state_array = np.array(all_state, dtype=float)
    if all_state_array.ndim != 3:
        raise ValueError(f"Unexpected shape: {all_state_array.shape}, expected (N, M, k).")

    n_cols = all_state_array.shape[-1]
    n_bits = n_cols - 1 if n_lambda_states is not None else n_cols

    if n_lambda_states is not None:
        bit_weights = n_lambda_states * (2.0 ** np.arange(n_bits - 1, -1, -1))
        weights = np.concatenate([bit_weights, [1.0]])
    else:
        weights = 2.0 ** np.arange(n_bits - 1, -1, -1)

    nan_mask = np.isnan(all_state_array).any(axis=-1)  # shape: (N, M)
    indexed_states = np.full(all_state_array.shape[:-1], np.nan, dtype=float)  # shape: (N, M)
    valid_mask = ~nan_mask
    indexed_states[valid_mask] = all_state_array[valid_mask] @ weights

    return indexed_states


def index_to_state(index, n_bits, n_lambda_states=None):
    """
    Inverse of `state_to_index_vectorized`.

    Converts an integer index (scalar or array-like) back into a (n_bits,)
    array of bits, or a (n_bits + 1,) array of [bits..., x] if
    `n_lambda_states` is given.

    Parameters
    ----------
    index : int or array-like of ints
    n_bits : int
        Number of binary bits encoded in the index.
    n_lambda_states : int, optional
        Number of values the trailing extra state can take, if present.
    """
    index = np.asarray(index)
    max_index = (n_lambda_states * 2**n_bits if n_lambda_states is not None else 2**n_bits) - 1
    if np.any((index < 0) | (index > max_index)):
        raise ValueError(f"Index out of range: {index}. Expected 0..{max_index}.")

    if n_lambda_states is not None:
        x = index % n_lambda_states
        binary_index = index // n_lambda_states
    else:
        binary_index = index

    def _bits(i):
        return np.array([int(b) for b in format(int(i), f'0{n_bits}b')], dtype=int)

    if binary_index.ndim == 0:
        bits = _bits(binary_index)
        return bits if n_lambda_states is None else np.concatenate([bits, [int(x)]])
    else:
        bits = np.stack([_bits(i) for i in binary_index])
        return bits if n_lambda_states is None else np.concatenate([bits, x[..., None]], axis=-1)


def compute_transition_matrix(subset, num_states, lagtime, pseudocount=0.25):
    """Compute transition matrix for a given subset of trajectories."""

    C = np.zeros((num_states, num_states))  # Initialize count matrix

    for traj in subset:
        for t in range(len(traj) - lagtime):
            from_state = traj[t]
            to_state = traj[t + lagtime]

            # Skip NaN transitions
            if np.isnan(from_state) or np.isnan(to_state):
                continue

            # Convert states to integers for indexing
            from_state = int(from_state)
            to_state = int(to_state)

            # Count transitions
            C[from_state, to_state] += 1.0

    # Add pseudocounts to avoid zero entries
    C += pseudocount

    # Normalize rows to get probabilities
    row_sums = C.sum(axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1  # Prevent division by zero
    T = C / row_sums

    return T


def get_transition_matrices(n_trajs, num_states, lagtime, cluster_size=10, pseudocount=0.25, n_jobs=-1):
    """
    Compute transition matrices for subsets of trajectories in parallel.
    """

    num_trajs = n_trajs.shape[0]  # Number of trajectories

    # Shuffle indices
    indices = np.arange(num_trajs)
    np.random.shuffle(indices)

    # Split into clusters
    clusters = [indices[i:i + cluster_size] for i in range(0, num_trajs, cluster_size)]

    # Merge last small cluster with the second-last if needed
    if len(clusters) > 1 and len(clusters[-1]) < cluster_size:
        clusters[-2] = np.concatenate([clusters[-2], clusters[-1]])
        clusters.pop()

    # Parallel computation of transition matrices
    def process_cluster(cluster):
        subset = n_trajs[cluster]
        T = compute_transition_matrix(subset, num_states, lagtime, pseudocount)
        return T

    # Use joblib's Parallel for parallelism.
    # `delayed(process_cluster)(c)` calls `process_cluster(c)` lazily.
    # `n_jobs=-1` uses all available CPUs unless specified otherwise.
    transition_matrices = Parallel(n_jobs=n_jobs)(
        delayed(process_cluster)(cluster)
        for cluster in tqdm(clusters, desc="Computing transition matrices", unit="cluster")
    )

    return transition_matrices


def compute_stationary_distribution(T, lagtime):
    """Compute the stationary distribution of a transition matrix T.

    INPUT:
    T - Transition matrix where T_ij is the probability of transitioning i -> j.

    RETURN:
    pi - The stationary distribution (1D NumPy array).
    t2 - The implied timescale (in units of steps).
    """
    try:
        # Compute the implied timescale
        evals = np.linalg.eigvals(T.transpose())  # will be something like [0.99754545 1.        ]
        evals_sorted = np.sort(evals)      # ascending order
        mu2 = evals_sorted[-2]            # second-largest eigenvalue

        t2 = -1.0 * lagtime / np.log(mu2.real)  # the implied timescale relation

        # Compute the stationary state distribution
        n_states = T.shape[0]
        A = np.transpose(T) - np.eye(n_states)  # (T' - I)
        A = np.vstack([A, np.ones(n_states)])  # Append normalization row
        b = np.zeros(n_states + 1)
        b[-1] = 1  # Ensure probability sums to 1

        # Solve for stationary distribution using least squares
        pi, *_ = np.linalg.lstsq(A, b, rcond=None)

        # Ensure non-negative values and normalize
        pi = np.maximum(pi, 0)  # Prevent small negative values due to numerical error
        pi /= np.sum(pi)  # Normalize to sum to 1

    except Exception as e:
        print(f"Error computing stationary distribution: {e}")
        t2 = np.nan
        pi = None

    return pi, t2


def process_trajectory(n_trajs, lagtime, num_states, cluster_size):
    """Compute the mean/std stationary population and mean/std implied timescale
    across bootstrap subsets of trajectories, at one lag time."""

    # Calculate the transition matrix
    transition_matrices = get_transition_matrices(n_trajs, num_states, lagtime, cluster_size, pseudocount=0.25, n_jobs=-1)
    transition_matrices = np.array(transition_matrices)

    # Calculate the stationary population
    pi_all = []
    t2_all = []

    for T in transition_matrices:
        pi, t2 = compute_stationary_distribution(T, lagtime)
        pi_all.append(pi)
        t2_all.append(t2)

    pi_all = np.array(pi_all)
    t2_all = np.array(t2_all)

    t2_mean = np.exp(np.mean([np.log(t2) for t2 in t2_all]))
    t2_std = np.exp(np.sqrt(np.var([np.log(t2) for t2 in t2_all])))
    pi_means = np.mean(pi_all, axis=0)  # Mean across trajectories
    pi_std = np.std(pi_all, axis=0)  # Standard deviation

    return pi_means, pi_std, t2_mean, t2_std
