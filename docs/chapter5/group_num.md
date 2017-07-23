## group_num

### Syntax

	group_num new_group_number restart_group_number

* `new_group_number`, `restart_group_number` = non-negative integer

### Examples

	group_num 3 0
	group_num 2 1

### Description

This command sets the numbers of new groups and restart groups. In CAC, a group is a collection of elements/nodes/atoms. There are two purposes of having groups: (i) to apply a controlled displacement to certain elements/nodes/atoms, (ii) to [calculate](cal.md) some mechanical quantities, e.g., energy, force, and stress, of certain elements/nodes/atoms.

The new groups are defined in the [group](group.md) command. The elements/nodes/atoms contained in restart groups are read from the `group_in_#.id` files, where `#` is a positive integer starting from `new_group_number` + 1, yet their displacement information is set in the [group](group.md) command.

The total number of groups, i.e., `new_group_number` + `restart_group_number` + [the number of boundary groups](bd_group.md), cannot be larger than 39. For each group, CAC outputs a `group_out_#.id` file containing relevant elements/nodes/atoms information, where `#` is the group id starting from 1. One may rename `group_out_#.id` to `group_in_#.id` and use the latter for the restart groups.

### Related commands

The controlled displacement information of each group is set in the [group](group.md) command.

### Related files

`group_init.f90` and `group.f90`

### Default

	group_num 0 0