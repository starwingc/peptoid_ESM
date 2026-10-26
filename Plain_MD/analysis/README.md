# Workflow for Omega Data Analysis

## Step 1: Extract Omega Data and Perform Clustering Analysis  
Run **`clustering.ipynb`**
- Using pyemma to extracted the omega angle data from the xtc
- create a `data.pkl` for storing the omega data (742, x, 3) dimension
- Clustering
- ** Doesn't do a clustering error estimation yet **

## Step 2: Analysis of the result 

### `cistrans_population.ipynb`
- take in the `data.pkl`
- calculate the trans population (0, 1) along the time

### `cistrans_8_conform_population.ipynb`
- take in the `data.pkl`
- same idea as `cistrans_population.ipynb` but for the 8-conformer model
  (all combinations of cis/trans across the 3 residues)

### `autocorrelation.ipynb`
- take in the `data.pkl`
- convert them into simple two state cis/trans [0, 1]
- calculate autocoorelation timescale arocss six replicas for three difference omega angles 
- output `autocoorel_data/` with all the mean and variance stored as pkl

### `transition_matrix.ipynb`
- take in the `data.pkl`
- convert them into simple two state cis/trans [0, 1]
- manually assign each cis/tran into 8 state, and create a (742, somenumber inlude nah for placeholder) 
- create a transition matrix between 8 state for difference lag time 
- alcualte the eigenvector (stationary state population) of the identity eigenvalue 
- plot the stationary state population along each tau 

### `transition_matrix_res.ipynb`
- same as `transition_matrix.ipynb` but builds an independent 2-state
  (cis/trans) transition matrix per residue instead of the joint 8-state one
- also used to calculate the implied timescale (second-largest eigenvalue)
  across each tau for the three omega angles
