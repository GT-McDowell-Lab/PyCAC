## grain_dir

### Syntax

	grain_dir direction overlap

* direction = 1 or 2 or 3

* overlap = real number

### Examples

	grain_dir 1 0.1
	grain_dir 2 0.2

### Description

Set the grain aggregation direction and the overlap between adjacent grains along that direction.

The `direction` can only be 1, 2, or 3, corresponding to the _x_, _y_, or _z_ directions, respectively.

The `overlap`, in unit of the periodic length of the lattice, refers to the overlapping length of adjacent grains along the `direction`. It is used to adjust the relative position between neighboring grains to find the energy minimized structure. If the `overlap` is so large that many atoms from different grains are too close to each other, one may use the `cutoff` style in the [modify](modify.md) command to delete atoms that are within a certain distance from each other.

### Related commands

This command is only relevant when the number of grain as specified in the [grain_num](grain_num.md) command is more than one.

### Related files

`box_init.f90` and `model_init.f90`

### Default

	grain_dir 3 0.