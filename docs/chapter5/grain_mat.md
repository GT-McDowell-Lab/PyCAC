## grain_mat

### Syntax

	boundary x y z

* x,y,z = _p_ or _s_ or _f_

		p is periodic
		f is non-periodic and fixed
		s is non-periodic and shrink-wrapped

### Examples

	boundary p f s

### Description

Set the style of boundaries for the global simulation box in each dimension. The same style is assigned to both the lower and upper face of the box.

The style _p_ means the box is periodic, so that atoms/nodes interact across the boundary, and they can exit one end of the box and re-enter the other end.

The styles _f_ and _s_ mean the box is non-periodic, so that particles do not interact across the boundary and do not move from one side of the box to the other. For style _f_, the position of the face is fixed. For style _s_, the position of the face is set so as to encompass the atoms in that dimension (shrink-wrapping), no matter how far they move.

### Related commands

When the style of a boundary is _p_, the corresponding [zigzag](zigzag.md) arg is changed to _f_. In other words, a boundary has to be flat to apply the periodic boundary condition.

### Related files

`grain.f90`

### Default

