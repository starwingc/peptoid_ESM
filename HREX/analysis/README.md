# Workflow for Omega Data Analysis

## Step 1: Extract Omega Data  
Run **`omega_analysis.ipynb`** to obtain the omega data for every replica and every state.  
- output file in `omega_data/`
    - `omegas_rep*.pkl` include the omegas along an intact replica
    - `omegas_state*.pkl` include the state omegas  

## Step 2: Perform Clustering Analysis  
Run **`clustering.ipynb`**
- read in the `omegas_state0.pkl`
- convert them into simple two state cis/trans [0, 1]
- Analyze cluster formations.  
- Calculate cluster errors.

## Step 3: Analysis of the result 

### `cistrans_population.ipynb`
- take in the `omegas_state0.pkl`
- calculate the trans population (0, 1) along the time

### `implied_timescale.ipynb` (need to double check)
- take in the `omegas_rep*.pkl`
- convert them into simple two state cis/trans [0, 1]
- built a transition matrix
- calculate the implied timescale (second most important eigenvalue) across each tau for three omega angles

### `autocoorelation.ipynb`
- take in the `omegas_rep*.pkl`
- convert them into simple two state cis/trans [0, 1]
- calculate autocoorelation timescale arocss six replicas for three difference omega angles 