## boundary

### Syntax

	boundary x y z

* `x`, `y`, `z` = _p_ or _s_

		p is periodic
		s is non-periodic and shrink-wrapped

### Examples

	boundary p s s

### Description

This command sets the boundary conditions of the simulation cell along the _x_, _y_, and _z_ directions. Along each axis, the same condition is applied to both the lower and upper faces of the cell.

_p_ sets periodic boundary conditions (PBCs). The nodes/atoms interact across the boundary and can exit one end of the cell and re-enter the other end. For more information of the PBCs in the coarse-grained domain, read chapter 3 of [Shuozhi Xu's Ph.D. dissertation](https://smartech.gatech.edu/handle/1853/56314).

_s_ sets non-periodic boundary conditions, where nodes/atoms do not interact across the boundary and do not move from one side of the cell to the other. The positions of both faces are set so as to encompass the nodes/atoms in that dimension, no matter how far they move.

Under neither boundary condition will any nodes/atoms be lost during a CAC simulation.

### Related commands

When _p_ is set along a certain direction, the corresponding [zigzag](zigzag.md) is set to _f_. In other words, a boundary has to be flat to apply the PBCs.

This command becomes irrelevant when [`boolean_restart`](restart.md) = _t_, in which case the boundary conditions are read from the [`cac_in.restart`](../chapter) file.

### Default

	boundary p p p