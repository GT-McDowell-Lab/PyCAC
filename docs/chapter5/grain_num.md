## grain_num

### Syntax

	grain_num grain_number

* `grain_number` = positive integer

### Examples

	grain_num 2

### Description

This command sets the number of grains in the simulation cell. When `grain_number` > 1, grains are stacked along the [`direction`](grain_dir.md). Each grain has its own [lattice orientations](grain_mat.md), [origin displacements](grain_move.md), and [number of subdomains](subdomain.md).

### Related commands

In commands [grain_mat](grain_mat.md), [grain_move](grain_move.md), [subdomain](subdomain.md), [unit_num](unit_num.md), and [unit_type](unit_type.md), all information related to `grain_id` that is larger than `grain_number` in this command will be discarded.

### Related files

`box_init.f90` and `grain.f90`

### Default

	grain_num 1