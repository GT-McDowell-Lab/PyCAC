## group_num

### Syntax

	group_num new_group_number restart_group_number fix_number cal_number

* `new_group_number`, `restart_group_number`, `fix_number`, `cal_number` = non-negative integer (<= 40)

### Examples

	group_num 3 0 3 0
	group_num 2 1 1 2

### Description

This command sets the numbers of [new groups](group.md), restart groups, [fix](fix.md), and [calculations](cal.md). In CAC, a group is a collection of elements/nodes/atoms. There are two purposes of having groups: (i) to [apply a displacement/force](fix.md) to certain elements/nodes/atoms, (ii) to [calculate](cal.md) some mechanical quantities, e.g., energy, force, and stress, of certain elements/nodes/atoms.

The new groups are defined in the [group](group.md) command. The elements/nodes/atoms contained in restart groups, named `group_#`, are read from the `group_in_#.id` files, where `#` is a positive integer starting from `new_group_number` + 1, yet their displacement/force information is set in the [fix](fix.md) command.

The total number of groups, i.e., `new_group_number` + `restart_group_number`, cannot be larger than 40. For each group, CAC outputs a `group_out_#.id` file containing relevant elements/nodes/atoms information, where `#` is the group id starting from 1. One may rename `group_out_#.id` to `group_in_#.id` and use the latter for the restart groups.

The total number of fix and calculations, `fix_number` + `cal_number`, must equal `new_group_number` + `restart_group_number`. As a result, `fix_number` + `cal_number` cannot be larger than 40.

### Related commands

The new groups are defined in the [group](group.md) command. The displacement/force and calculation information of each group is set in the [fix](fix.md) and [cal](cal.md) commands, respectively.

### Related files

`group.f90`, `group_fix.f90`, `group_cal.f90`

### Default

	group_num 0 0 0 0