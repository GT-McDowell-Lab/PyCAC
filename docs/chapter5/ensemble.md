## ensemble

### Syntax

	ensemble boolean_t boolean_p

* boolean\_t, boolean\_p = _t_ or _f_

		t is true
		f is false

### Examples

	ensemble t f

### Description

Decide whether the temperature (in unit of K) or the pressure (in unit of GPa) is controlled in a PyCAC simulation.

### Related commands

The temperature can only be controlled when the `dyn_style` is `ld`, as specified in the [dynamics](dynamics.md) command. If other `dyn_style` is used, a warning will be issued.

### Related files

`thermostat.f90`

### Default

	ensemble f f

