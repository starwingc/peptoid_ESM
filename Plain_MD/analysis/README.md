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

### `implied_timescale.ipynb` (need to double check)
- take in the `data.pkl`
- convert them into simple two state cis/trans [0, 1]
- built a transition matrix
- calculate the implied timescale (second most important eigenvalue) across each tau for three omega angles

### `autocoorelation.ipynb`
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
