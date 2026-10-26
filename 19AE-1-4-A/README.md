# 19AE1-4-A

Base GROMACS input set for peptoid 19AE1-4-A ([Peptoid Data Bank
entry](https://databank.peptoids.org/peptoid/19AE1-4-A)) — an unconstrained
linear tetramer solvated in TIP3P water with the [STEPs force
field](https://pubs.acs.org/doi/10.1021/acs.jpcb.3c01424), prepared with
GROMACS. See the root [README.md](../README.md) for the full system
description and reference.

## Files

- `input.pdb` / `input.gro` - solvated starting structure (peptoid + TIP3P
  water + Na/Cl ions, 0.1 M background electrolyte with neutralizing counter
  ions).
- `peptoid.top` - GROMACS topology (STEPs force field).
- `index.ndx` - GROMACS index groups for this system.

## `all_cis_trans_combination/`

Pre-built starting structures covering all 8 cis/trans combinations of the
backbone omega dihedrals, used to seed the **Plain MD** Folding@home runs.
See `all_cis_trans_combination/README.md`.
