## minimize

### Syntax

	minimize minimizor max_outer_iteration tolerance

* minimizor = _cg_ or _sd_ or _fire_ or _qd_

* dmax\_outer\_iteration = maximum outer iteraion

* tolerance = real number

### Examples

	minimize cg 1000 1d-5
	minimize fire 100 1d-6

### Description

Set the energy minimization style.

When the minimizor is _cg_, the conjugate gradient algorithm is applied. 

When the minimizor is _sd_, the steepest descent algorithm is applied.

Note that both _cg_ and _sd_ use the negative gradient of potential energy as the initial direction; from the second step, however, the _sd_ method uses the current negative gradient while the _cg_ method uses the negative gradient conjugated to the current potential surface. The line search is used to find the length along which the nodes/atoms need to move along the designated direction to find the minimized energy.

When the minimizor is _fire_, the fast inertial relaxation engine is applied.

When the minimizor is _qd_, the quenched dynamics algorithm is applied.

The energy minimiztion is considered to converge when either the outer iteration reaches the `max_outer_iteraction` or the energy variation between successive iterations divided by the energy of the current iteration is less than the `tolerance`.

### Related commands

This command is relevant only when the [simulator](simulator.md) is statics or hybrid.

### Related files

`mini_init.f90`, `mini_energy.f90`, and `hybrid.f90`, among many

### Default

	minimize cg 1000 1d-6