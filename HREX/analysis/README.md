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

### `autocoorelation.ipynb`
- take in the `omegas_rep*.pkl`
- convert them into simple two state cis/trans [0, 1]
- calculate autocoorelation timescale arocss six replicas for three difference omega angles 

### `transition_matrix_res.ipynb`
- take in the `omegas_state{0...5}.pkl`
- convert them into simple two state cis/trans [0, 1]
- manually assign each residues-wise cis/tran into 12 state ( trans/cis state x 6 lambda state), and create a transition matrix between 12 state for difference lag time 
- alcualte the eigenvector (stationary state population) of the identity eigenvalue 
- plot the stationary state population along each tau 

### `transition_matrix.ipynb`
- take in the `omegas_state{0...5}.pkl`
- convert them into simple two state cis/trans [0, 1]
- manually assign each cis/tran into 48 state (8 trans/cis state x 8 lambda state), and  transition matrix between 48 state for difference lag time 
- alcualte the eigenvector (stationary state population) of the identity eigenvalue 
- plot the stationary state population along each tau 

### `cistrans_population.ipynb`
- take in the `omegas_state{0...5}.pkl`
- separate the oemga into 6 states 
- calculate the trans population (0, 1) along the time of each states

### `cistrans_8_conform_population.ipynb`
- take in the `omegas_state{0...5}.pkl`
- separate the oemga into 6 states 
- calculate the 8 conformation population (0, 1) along the time of each states

