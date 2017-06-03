## ensemble

### Syntax

	ensemble boolean_t boolean_p

* `boolean_t`, `boolean_p` = _t_ or _f_

		t is true
		f is false

### Examples

	ensemble t f

### Description

This command decides whether the temperature (`boolean_t`) and the pressure (`boolean_p`) are kept a constant in a PyCAC simulation.

### Related commands

The temperature is kept a constant only when [`dyn_style` = _ld_](dynamics.md). A warning will be issued if other `dyn_style` is used. The pressure cannot be kept a constant in the current PyCAC code.

### Related files

`thermostat.f90`

### Default

	ensemble f f

