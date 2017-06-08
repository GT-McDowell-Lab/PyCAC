## zigzag

### Syntax

	zigzag boolean_x boolean_y boolean_z

* `boolean_x`, `boolean_y`, `boolean_z` = _t_ or _f_

		t is true
		f is false

### Examples

	zigzag t f f
	zigzag t t t

### Description

This command decides whether the simulation cell boundaries are left zigzagged along the _x_, _y_, and _z_ directions, respectively.

Due to the rhombohedral shape of the finite elements in the coarse-grained domain, the simulation cell mostly likely has zigzagged boundaries, as shown in Fig. C27(a) of [Xu et al., 2015](http://dx.doi.org/10.1016/j.ijplas.2015.05.007). On the other hand, flat boundaries are sometimes desirable to enforce the periodic boundary conditions or to lower the aphysical stress concentrations at the boundaries.

If one of the three booleans in this command is _f_, atoms will be filled in the jagged interstices, resulting in flat boundaries for the corresponding direction, as shown in ig. C27(b) of [Xu et al., 2015](http://dx.doi.org/10.1016/j.ijplas.2015.05.007), unless the boundaries were already flat with rhomboheral elements, e.g., on {111} planes in an FCC and on {110} planes in a BCC lattice. If a certain boolean is _t_, no atoms will be filled in at the boundaries.

### Related commands

When a boundary is [periodic](boundary.md), the corresponding [zigzag](zigzag.md) boolean becomes _f_, regardless of what is set in this command, because the periodic boundaries must be flat in the current code.

This command becomes irrelevant when [`boolean_restart`](restart.md) = _t_.

### Related files

`model_init.f90`

### Default

	zigzag t t t