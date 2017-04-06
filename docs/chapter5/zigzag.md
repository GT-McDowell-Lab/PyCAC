## zigzag

### Syntax

	zigzag boolean_x boolean_y boolean_z

* boolean\_x, boolean\_y, boolean\_z = _t_ or _f_

		t is true
		f is false

### Examples

	zigzag t f f
	zigzag t t t

### Description

Set the style of the zigzag boundaries along the _x_, _y_, and _z_ directions.

Take the _x_ boundary as an example, when `boolean_x` is _t_, the code won't do anything to the zigzag boundary which is naturally formed because of the shape of the rhombohedral element; when `boolean_x` is _f_, the code will fill the zigzag boundary with atoms such that the boundary will be flat, see [Xu et al., IJP, 2015]. The flat boundary is used either to enforce the periodic boundary conditions or to lower the stress concentration to reduce unwanted dislocation nucleation.

### Related commands

When the style of a boundary is _p_, the corresponding [zigzag](zigzag.md) arg is changed to _f_, regardless of what is specified in this command. In other words, a boundary has to be flat to apply the periodic boundary condition.

### Related files

`model_init.f90`

### Default

	zigzag t t t