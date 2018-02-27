## group_num

### Syntax

	group_num new_group_number restart_group_number fix_number cal_number

* `new_group_number`, `restart_group_number`, `fix_number`, `cal_number` = non-negative integer (<= 40)

### Examples

	group_num 3 0 3 0
	group_num 2 1 1 2

### Description

This command sets the numbers of [new groups](group.md), restart groups, [fix](fix.md), and [calculations](cal.md). In CAC, a group is a collection of elements/nodes/atoms. There are two purposes of having groups: (i) to [apply a displacement/force](fix.md) to certain elements/nodes/atoms, (ii) to [calculate](cal.md) some mechanical quantities, e.g., energy, force, and stress, of certain elements/nodes/atoms.

The new groups are defined in the [group](group.md) command. The elements/nodes/atoms contained in the restart groups, named `group_*`, are read from the `group_in_*.id` files, where `*` is a positive integer starting from `new_group_number` + 1, yet their displacement/force information is set in the [fix](fix.md) command.

The total number of groups, i.e., `new_group_number` + `restart_group_number`, cannot be larger than 40. Files `group_in_*.id` contain information of the restart groups. On the one hand, there cannot be fewer `group_in_*.id` files than `restart_group_number`; on the other hand, any `group_in_*.id` file with `*` > `new_group_number` + `restart_group_number` will be ignored. When [`boolean_restart`](restart.md) = _f_, `restart_group_number` becomes 0, regardless of its value set in this command.

`fix_number` should not be larger than `new_group_number` + `restart_group_number`; neither should `cal_number`. Also, `fix_number` + `cal_number` should not be smaller than `new_group_number` + `restart_group_number`.

### Related commands

The new groups are defined in the [group](group.md) command. The displacement/force and calculation information of each group is set in the [fix](fix.md) and [cal](cal.md) commands, respectively.

### Related files

`group.f90`, `fix_displacement.f90`, `fix_force.f90`, `group_cal.f90`

### Default

	group_num 0 0 0 0
