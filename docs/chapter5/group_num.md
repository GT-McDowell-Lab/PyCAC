## group_num

### Syntax

	group_num number_of_new_group number_of_restart_group

* number\_of\_new\_group, number\_of\_restart\_group = integer

### Examples

	group_num 3 0
	group_num 2 1

### Description

Set the number of new groups and the number of restart groups. The restart groups are read from the files `group_in_#.id` where the `#` is an integer equalling `number_of_new_group` + 1, 2, 3 ... Note that for each new group, a series of `group_out_#.id` files containing corresponding nodal and atomic ID are created.

Note that the total number of groups, i.e., `number_of_new_group` + `number_of_restart_group` + the number of groups specified in the [bd_group](bd_group.md), cannot be larger than 39.

### Related commands

Properties associated with each group is set in the [group](group.md) command.

### Related files

`group_init.f90` and `group.f90`

### Default

number\_of\_restart\_group = 0