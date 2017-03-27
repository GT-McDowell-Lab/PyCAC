## cal

### Syntax

	cal group_name cal_variable

* group_name = a string with length <= 30
* cal_variable = _energy_ or _force_ or _stress_

### Examples

	cal group_1 force
	cal group_3 stress

### Description

Decide a group and associated quantities that are calculated and saved to a file named `group_cal_#` where # is the ID of cal.

The style _energy_, _force_, and _stress_ correspond to a scalar, a 3 by 1 vector, and a 3 by 3 tensor, respectively.

### Related commands

There cannot be fewer `cal` commands than the cal\_num defined by the `cal_num` command. The group name must match one of the groups defined in the `group` command.

### Default

None.

