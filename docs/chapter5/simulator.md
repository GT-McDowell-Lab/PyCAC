## simulator

### Syntax

	simulator simulator_type

* simulator = _dynamics_ or _statics_ or _hybrid_

### Examples

	simulator dynamics
	simulator hybrid

### Description

Set the simulator used in PyCAC simulations: _dynamics_ (dynamic CAC), _statics_ (quasistatic CAC), or _hybrid_ (dynamic CAC with periodic energy minimization).

### Related commands

The dynamic and quasistatic simulation styles are set by the [dynamics](dynamics.md) and [minimize](minimize.md) commands.

### Related files

`dynamics.f90`, `quasi_statics.f90`, and `hybrid.f90`

### Default

	simulator dynamics