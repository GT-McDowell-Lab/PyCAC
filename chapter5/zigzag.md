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

If one of the three booleans in this command is _f_, atoms will be filled in the corresponding jagged interstices, resulting in flat boundaries normal to the corresponding direction, unless the boundaries were already flat with rhomboheral elements, e.g., parallel to a {111} plane in an FCC lattice or to a {110} plane in a BCC lattice. Examples of the filled atoms include Fig. C27(b) of [Xu et al., 2015](http://dx.doi.org/10.1016/j.ijplas.2015.05.007) and the figure for the [subdomain](subdomain.md) command in which the atoms are filled in at the leftmost and rightmost simulation cell boundaries. If a certain boolean is _t_, no atoms will be filled in at the boundaries.

### Related commands

When a boundary is [periodic](boundary.md), the corresponding [zigzag](zigzag.md) boolean becomes _f_, regardless of what is set in this command, because the periodic boundaries must be flat in CAC simulations.

This command becomes irrelevant when [`boolean_restart`](restart.md) = _t_, in which case there is no need for the boundary shape information.

### Related files

`model_init.f90`

### Default

	zigzag t t t