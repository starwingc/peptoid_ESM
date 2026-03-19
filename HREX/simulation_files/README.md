
# Hamiltonian Replica Exchange Molecular Dynamics (HREMD) for Peptoid Tetramers

This repository contains the scripts and instructions required to set up and run a Hamiltonian Replica Exchange Molecular Dynamics (HREMD) simulation for a peptoid tetramer using GROMACS.

## Step 1: Prepare the Topology (`.tpr`) Files

First, you need to generate the `.tpr` files for each replica state and create their respective directories. This is handled by the `prepare_tpr.sh` script.

Make the script executable and run it:

```bash
chmod +x prepare_tpr.sh
./prepare_tpr.sh
```

### Modifying Lambda Values
If you need to change the lambda values or the number of intermediate states, open `prepare_tpr.sh` in a text editor and modify the following variables:

```bash
# Number of alchemical intermediate states (e.g., 6 replicas)
n=6

# Define fep-lambdas values for each state
fep_lambdas=(0.00 0.20 0.40 0.60 0.80 1.00)

# Loop over the states (Make sure this matches n-1)
for i in {0..5}
do
  # ... tpr generation commands ...
done
```

## Step 2: Run the HREMD Simulation

Once the `state_X` directories are created and populated with `.tpr` files, you can initiate the replica exchange simulation using MPI.

Execute the following commands (or place them in your job submission script):

```bash
# Define the state directories for the -multidir flag
state_dirs=$(echo state_{0..5} | tr ' ' ' ')

# Run the GROMACS mdrun with MPI
mpirun -np 168 mdrun_mpi -deffnm HREMD -dhdl dhdl.xvg -replex 5000 -multidir $state_dirs -noappend
```

### ⚠️ Important Execution Notes:

* **MPI Ranks (`-np 168`)**: The total number of processors you allocate (`-np`) **must be a multiple of the number of replicas**. For example, if you have 6 replicas and allocate 168 cores, GROMACS will dedicate exactly 28 cores to each replica ($168 \div 6 = 28$).
* **Exchange Frequency (`-replex 5000`)**: This flag dictates how often GROMACS attempts to exchange replicas. `5000` means an exchange is attempted every 5,000 integration steps. Make sure this aligns with the time step (`dt`) defined in your `.mdp` file to achieve your desired exchange time interval.

