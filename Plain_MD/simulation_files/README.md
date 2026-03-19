# Plain Molecular Dynamics Simulation of Peptoid 19AE1-4-A

This repository contains the setup and instructions for running a plain Molecular Dynamics (MD) simulation of peptoid 19AE1-4-A in an aqueous environment, intended for deployment on Folding@home.

## System Details
* **Molecule:** Peptoid 19AE1-4-A
* **Solvent:** Water
* **Force Field:** STEPs
* **Water Model:** TIP3P
* **Production Scale:** 100 clones
* **Original Directory:** `../../19AE-1-4-A/all_cis_trans_combination/`

## Starting Conformations
The project includes 8 starting shapes based on all possible cis/trans combinations. Navigate to the corresponding folder to start a simulation from that specific geometry:

| Directory | Conformation |
| :--- | :--- |
| **RUN0** | ccc |
| **RUN1** | cct |
| **RUN2** | ctc |
| **RUN3** | ctt |
| **RUN4** | tcc |
| **RUN5** | tct |
| **RUN6** | ttc |
| **RUN7** | ttt |

---

## Execution Instructions

To start a simulation from any of the shapes listed above, navigate into its respective folder (e.g., `cd RUN0`) and run the following commands.

### Step 1: Prepare the Run Input File (`.tpr`)

First, compile the atomic coordinates, system topology, and simulation parameters into a single binary run input file (`.tpr`) using the `grompp` module.

```bash
gmx grompp -c prod.gro -f prod.mdp -p topol.top -n index.ndx -o prod.tpr -maxwarn 1
```

### Step 2: Execute the Simulation

Once the `prod.tpr` file is successfully generated, initiate the simulation using the `mdrun` command:

```bash
gmx mdrun -v -s prod.tpr -deffnm prod
```

**Command Breakdown:**
* **`-v`**: Enables verbose mode, printing the simulation progress and estimated time to completion to the terminal.
* **`-s prod.tpr`**: Specifies the input run file generated in Step 1.
* **`-deffnm prod`**: Sets the default file name prefix for all output files (e.g., `prod.xtc`, `prod.edr`, `prod.log`) to keep your directory clean and organized.

