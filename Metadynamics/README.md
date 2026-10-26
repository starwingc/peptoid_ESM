ExtractOmega script -> AutoCorrFromExtract -> TransitionMatrix. The extract omega script worked based on the full plumed datafiles which are enormous, the pared down sanitycheck data files should be smaller and sufficient for all of the rest of the calculations. So I would go straight to the autocorrelation / transition matrix scripts if needed.

See `analysis/README.md` for the full notebook-by-notebook workflow (including the convergence-over-time and population-over-time steps) and for what each data subfolder under `analysis/` holds.
