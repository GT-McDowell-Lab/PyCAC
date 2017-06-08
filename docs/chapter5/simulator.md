## simulator

### Syntax

	simulator simulation_style

* `simulation_style` = _dynamics_ or _statics_ or _hybrid_

### Examples

	simulator dynamics
	simulator hybrid

### Description

This command sets the `simulation_style` in PyCAC simulations: _dynamics_ (dynamic CAC), _statics_ (quasistatic CAC), or _hybrid_ (dynamic CAC with periodic energy minimization). The former two `simulation_style` have different [schemes](../chapter3/scheme.md).

### Related commands

More style information for the PyCAC are set in the [dynamics](dynamics.md) and [minimize](minimize.md) commands.

### Related files

`dynamics.f90`, `quasi_statics.f90`, and `hybrid.f90`

### Default

	simulator dynamics