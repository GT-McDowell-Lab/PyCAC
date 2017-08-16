## cal_num

### Syntax

	cal_num cal_number

* `cal_number` = non-negative integer (<= 19))

### Examples

	cal_num 0
	cal_num 3

### Description

This command sets the number of [group-based calculations](cal.md).

### Related commands

[Calculations](cal.md) are based on [group](group.md).

### Related files

`dump_init.f90` and `group_cal.f90`

### Default

	cal_num 0