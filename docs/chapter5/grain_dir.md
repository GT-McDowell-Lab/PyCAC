## grain_dir

### Syntax

	grain_dir direction overlap

* `direction` = 1 or 2 or 3
* `overlap` = real number

### Examples

	grain_dir 1 0.1
	grain_dir 2 0.2

### Description

This command sets the grain stack direction and the overlap between adjacent grains along that direction, as shown in the figure below:

![grain-dir](fig/grain-dir.jpg)

`direction` can only be 1, 2, or 3, corresponding to the _x_, _y_, or _z_ directions, respectively.

`overlap`, in unit of the [periodic length of the lattice](../chapter8/lattice-space.md), sets the overlap between adjacent grains along the `direction`. It is used to adjust the relative position along a certain direction between adjacent grains to find the energy minimized grain boundary structure. If `overlap` is so large that some atoms from different grains are too close to each other, one may use the `cutoff` style in the [modify](modify.md) command to delete some atoms that are within a certain distance from others.

### Related commands

This command is only relevant when [`grain_number`](grain_num.md) is more than one.

### Related files

`box_init.f90` and `model_init.f90`

### Default

	grain_dir 3 0.