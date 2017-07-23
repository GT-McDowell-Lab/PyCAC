## ensemble

### Syntax

	ensemble boolean_t boolean_p

* `boolean_t`, `boolean_p` = _t_ or _f_

		t is true
		f is false

### Examples

	ensemble t f

### Description

This command decides whether the temperature (`boolean_t`) and the pressure (`boolean_p`) are kept a constant in a CAC simulation.

### Related commands

The temperature is kept a constant only when [`dyn_style`](dynamics.md) = _ld_. As mentioned in the [`dynamics`](dynamics.md) command, the user will get a warning message if other [`dyn_style`](dynamics.md) is used. The pressure cannot be kept a constant in the current PyCAC code and the `boolean_p` is just a placeholder for now.

### Related files

`thermostat.f90`

### Default

	ensemble f f