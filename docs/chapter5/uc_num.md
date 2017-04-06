## uc_num

### Syntax

	uc_num {grain_id [element_size_type_id x element_num_x y element_num_y z element_num_z]}

* grain\_id, element\_size\_type\_id = integer

* element\_num\_x, element\_num\_y, element\_num\_z = integer

### Examples

	uc_num {1 [1 x 2 y 3 z 4]} {2 [1 x 6 y 1 z 2]}
	uc_num {1 [1 x 8 y 20 z 12] [2 x 40 y 2 z 60]} {2 [1 x 40 y 1 z 60] [2 x 8 y 25 z 12]}

### Description

Set the size of each element type domain, in unit of a primitive unit cell and an element in the atomistic and coarse-grained domains, respectively.

The outer and inner loops of this command are based on `grain_id` and `element_size_type_id`, respectively, the same as in the [ele_size](ele_size.md) command.

Assume the direction of the grain aggrevate (set by the [grain_dir](grain_dir.md) command) is _x_, the `element_num_y` and `element_num_z` given in this command most likely do not yield the same length of each element type domain along the _y_ and _z_ direction. In this case, the code will increase the length of all domains along these two directions to match the largest length so that a good bi/tri.. crystal is created.

### Related commands

The number of grains in the system is set by the [grain_num](grain_num.md) command. The number of element size type is set by the [grain_uc](grain_uc.md) command.

### Related files

`box_init.f90` and `model_init.f90`

### Default

None.