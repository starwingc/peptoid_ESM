# Workflow for Omega Data Analysis

## Step 1: Extract Omega Data and Perform Clustering Analysis  
Run **`clustering.ipynb`**
- Using pyemma to extracted the omega angle data from the xtc
- create a `data.pkl` for storing the omega data (742, x, 3) dimension
- Clustering
- ** Doesn't do a clustering error estimation yet **

## Step 2: Analysis of the result 

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