# Workflow for Omega Data Analysis

## Step 1: Extract Omega Data  
Run **`omega_analysis.ipynb`** to obtain the omega data for every replica and every state.  
- The output will be saved as `.npy` files in the `omega_data/` directory.

## Step 2: Perform Clustering Analysis  
Run the clustering script to:  
- Analyze cluster formations.  
- Calculate cluster errors.

## Step 3: Compute Isomerization Timescales  
Run **`isomerization_timescales.ipynb`** to determine the isomerization timescales of the data.
