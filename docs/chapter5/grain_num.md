## grain_num

### Syntax

	grain_num grain_number

* `grain_number` = integer

### Examples

	grain_num 2

### Description

Set the number of grains in the simulation cell. There is no limit of how many grains should exist in one cell.

### Related commands

In commands [ele_size](ele_size.md), [grain_dir](grain_dir.md), [grain_mat](grain_mat.md), [grain_move](grain_move.md), [grain_uc](grain_uc.md), and [uc_num](uc_num.md), any `grain_id` that is larger than the `grain_number` set in this command will be ignored, along with all arguments associated with those `grain_id`.

### Related files

`box_init.f90` and `grain.f90`

### Default

	grain_num 1