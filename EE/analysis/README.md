# Workflow for Omega Data Analysis

## Step 1: Extract Omega Data and Perform Clustering Analysis  
Run **`clustering.ipynb`**
- Using pyemma to extracted the omega angle data from the xtc
- create a `all_omega.pkl` for storing the omega data (85, x, 3) dimension of all the traj
- create `omega_state*.pkl` for separate the omega at difference lambda state using the log file (which indicate the state of frames for every frames)
- Clustering and error analysis

## Step 2: Analysis of the result 

### `cistrans_population.ipynb`
- take in the `data.pkl`
- calculate the trans population (0, 1) along the time

### `implied_timescale.ipynb` (need to double check)
- take in the `data.pkl`
- convert them into simple two state cis/trans [0, 1]
- built a transition matrix
- calculate the implied timescale (second most important eigenvalue) across each tau for three omega angles

### `autocoorelation.ipynb`
- take in the `all_omega.pkl`
- convert them into simple two state cis/trans [0, 1]
- calculate autocoorelation timescale arocss six replicas for three difference omega angles 
- output `autocoorel_data/` with all the mean and variance stored as pkl

### `transition_matrix.ipynb`
- take in the `all_omega.pkl`
- convert them into simple two state cis/trans [0, 1]
- manually assign each cis/tran into 32 state (8 trans/cis state x 4 lambda state), and create a (85, somenumber inlude nah for placeholder) 
- create a transition matrix between 32 state for difference lag time 
- alcualte the eigenvector (stationary state population) of the identity eigenvalue 
- plot the stationary state population along each tau 

### `plot_free_energy.ipynb` (for EE only)
- Take in the results help generated Julie
- Plot the convergence of free energy
- ensure the random walk of simulaiton 
