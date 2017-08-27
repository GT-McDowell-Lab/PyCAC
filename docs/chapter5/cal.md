## cal

### Syntax

	cal group_name cal_variable

* `group_name` = a string (length <= 30)

* `cal_variable` = _energy_ or _force_ or _stress_

### Examples

	cal group_1 force
	cal group_3 stress

### Description

This commands calculates certain quantities associated with [new groups](group.md) and/or restart groups. The `group_name` must match that of one of these groups.

_energy_ is the total potential energy in a group divided by the total number of nodes and atoms in the group. It is a scalar.

_force_ and _stress_ are the total force and stress in a group, respectively. _force_ is a $$3\times 1$$ vector while _stress_ is a $$3\times 3$$ tensor.

Results of this command are written to `group_cal_#` with a frequency of [`reduce_freq`](dump.md), where `#` is the ID of calculation. For _stress_, a $$3\times 3$$ strain tensor of the simulation box is appended right after the stress tensor.

### Related commands

There cannot be fewer `cal` commands than [`cal_number`](group_num.md), which should not be larger than [`new_group_number` + `restart_group_number`](group_num.md). When there are more `cal` commands in `cac.in` than [`cal_number`](group_num.md), those appearing later will be ignored. 

### Related files

`calculation.f90` and `group_cal.f90`

### Default

None.
