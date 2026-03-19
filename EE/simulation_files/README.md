# Expanded Ensemble (EE) Simulation

The following instructions outline the process for preparing and executing an Expanded Ensemble (EE) simulation for the peptoid system. These commands are optimized for **GROMACS 2020**.

## Step 1: Prepare the Run Input File (`.tpr`)

First, compile the atomic coordinates, system topology, and simulation parameters into a single binary run input file (`.tpr`) using the `grompp` module.

```bash
gmx grompp -c prod.gro -f prod.mdp -p topol.top -n index.ndx -o prod.tpr  -maxwarn 1
```

## Step 2: Execute the Simulation

Once the `prod.tpr` file is successfully generated, initiate the simulation using the `mdrun` command:

```bash
gmx mdrun -s prod.tpr  -deffnm prod
```

### Command Breakdown:
* **`-v`**: Enables verbose mode, printing the simulation progress and estimated time to completion to the terminal.
* **`-deffnm prod`**: Sets the default file name prefix for all outputs (e.g., `prod.xtc`, `prod.edr`, `prod.log`) to match your `.tpr` file.

***

Would you like me to draft a follow-up section explaining how to extract and analyze the free energy data (such as processing the `dhdl.xvg` file) from this simulation?