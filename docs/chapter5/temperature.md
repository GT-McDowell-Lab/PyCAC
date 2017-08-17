## temperature

### Syntax

	temperature boolean temp

* `boolean` = _t_ or _f_

		t is true
		f is false

* `temp` = non-negative real number

### Examples

	temperature t 10.
	temperature t 300.

### Description

This command sets whether the temperature is kept a constant in the system (`boolean`) for the [dynamic and hybrid](simulator.md) CAC simulations; and if yes, what is the desired temperature in K (`temp`).

A constant zero temperature is maintained in the system only when [`dyn_style`](dynamics.md) = _ld_ or _qd_, i.e., Langevin dynamics or quenched dynamics. Note that in this case, [the equation of motion for the Langevin dynamics reduces to that for the damped dynamics](dynamics.md).

A constant finite temperature is maintained in the system only when [`dyn_style`](dynamics.md) = _ld_, i.e., Langevin dynamics. The user will get a warning message if `temp` is finite and if [`dyn_style`](dynamics.md) = _qd_.

In [quasi-static](minimize.md) simulations, the temperature is effectively 0 K.

### Related commands

If `boolean` = _t_ and [`dyn_style`](dynamics.md) = _vv_, the user will get a warning message and the temperature `temp` becomes irrelevant, because the Velocity Verlet option cannot maintain a constant temperature.

### Related files

`thermostat.f90`, `langevin_dynamics.f90`, and `langevin_vel.f90`

### Default

	temperature t 10.