## box_dir

### Syntax

	box_dir x i j k y i j k z i j k

* `i`, `j`, `k` = real number

### Examples

	box_dir x 1. 0. 0. y 0. 1. 0. z 0. 0. 1.
	box_dir x 1. 0. 0. y 0. 0.94281 -0.33333 z 0. 0. 1.

### Description

Decide the grain boundary (GB) plane or the atomistic/coarse-grained domain interface orientation with respect to the simulation cell when there is more than one grain, i.e., `grain_num` > 1 in the [grain_num](grain_num.md) command. When `grain_num` = 1, this command does not take effect.

Assume that `direction` = 2 in the [grain_dir](grain_dir.md) command, i.e., the grains are stacked along the _y_ direction, the `box` command in the first example results in a GB plane normal to the _y_ axis; the `box` command in the second example, however, results in a GB plane inclined with respect to the _y_ axis, as shown in the figure below.

![box-dir](fig/box-dir.jpg)

In the literature, this command has been used to create the $$\Sigma 3\{111\}$$ coherent twin boundary in Fig. 1 of [Xu et al. 2016](http://dx.doi.org/10.1038/npjcompumats.2015.16) and Fig. 1(a) of [Xu et al. 2017](http://dx.doi.org/10.1007/s11837-017-2302-1) and the $$\Sigma 11\{113\}$$ symmetric tilt grain boundary in Fig. 1(b) of [Xu et al. 2017](http://dx.doi.org/10.1007/s11837-017-2302-1).

### Related commands

As opposed to the [grain\_mat](grain\_mat.md) command whose orientations are for the lattice, the orientations in this command are with respect to the simulation cell. One may use the [convert](convert.md) command to convert the lattice-based orientation to the simulation cell-based orientation.

### Related files

`model_init.f90`, among many

### Default

	box_dir x 1. 0. 0. y 0. 1. 0. z 0. 0. 1.