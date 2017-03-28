## box

### Syntax

	box x i j k y i j k z i j k

* i,j,k = real number

### Examples

	box x 1. 0. 0. y 0. 1. 0. z 0. 0. 1.
	box x 1. 0. 0. y 0. 0.94281 -0.33333 z 0. 0. 1.

### Description

Decide the grain boundary (GB) plane orientation with respect to the simulation cell when there is more than one grain as defined by [grain\_num](grain\_num.md)

Suppose that the grain\_dir = 2, i.e., the grains are aggregated along the y direction, the `box` command in the first example results in a GB plane normal to the y axis; the `box` command in the second example, however, results in a GB plane inclined with respect to the y axis, as shown in Fig. 1 of [Xu et al. 2016]() and Fig. 1(a) of [Xu et al. 2017]().

### Related commands

As opposed to the [grain\_mat](grain\_mat.md) command whose orientations are for the lattice, the orientations in the concurrent command are with respect to the simulation cell. To convert the lattice orientation to the simulation cell orientation, one may use the [convert](convert.md) to calculate the latter based on the former.

### Related files

`model_init.f90`, among many

### Default

	box x 1. 0. 0. y 0. 1. 0. z 0. 0. 1.