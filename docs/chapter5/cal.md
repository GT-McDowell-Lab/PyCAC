## cal

### Syntax

	cal group_name cal_variable

* `group_name` = a string (length <= 30)

* `cal_variable` = _energy_ or _force_ or _stress_

### Examples

	cal group_1 force
	cal group_3 stress

### Description

This commands calculates certain quantities associated with a [group](group.md).

_energy_ is the total potential energy in a group divided by the number of nodes/atoms in the group. It is a scalar.

_force_ and _stress_ are the total force and stress in a group, respectively. _force_ is a $$3\times 1$$ vector while _stress_ is a $$3\times 3$$ tensor.

Results of this command are written to `group_cal_#` at certain simulation step, where `#` is the ID of calculation. For _stress_, a $$3\times 3$$ strain tensor of the simulation box is appended right after the stress tensor.

### Related commands

There cannot be fewer `cal` commands than [`cal_number`](cal_num.md). When there are too many `cal` commands in `cac.in`, those appearing later will be ignored. The `group_name` must match one for the groups set in the [group](group.md) command.

### Related files

`group_cal.f90`

### Default

None.