## grain_mat

### Syntax

	grain_mat {grain_id x i j k y i j k z i j k}

* `i`, `j`, `k` = real number

### Examples

	grain_mat {1 x -1. 1. -2. y 1. 1. 0. z 1. -1. -1.}
	grain_mat {1 x 1. 1. 0. y -1. 1. 2. z 1. -1. 1.} {2 x 1. 1. 0. y -1. 1. -2. z -1. 1. 1.}

### Description

This command sets the crystallographic orientations in each grain, along the _x_, _y_, and _z_ directions, respectively. Note that the curly brackets `{` and `}` in the syntax/examples are to separate different grains, the number of which is [`grain_number`](grain_num.md); all brackets should not be included in preparing `cac.in`.

Any two sets of vector must be normal to each other, i.e.,

$$\mathbf{x} \cdot \mathbf{y} = 0$$

$$\mathbf{y} \cdot \mathbf{z} = 0$$

$$\mathbf{x} \cdot \mathbf{z} = 0$$

The right hand rule must also be obeyed, i.e.,

$$\mathbf{x} \times \mathbf{y} \parallel \mathbf{z}$$

$$\mathbf{y} \times \mathbf{z} \parallel \mathbf{x}$$

$$\mathbf{z} \times \mathbf{x} \parallel \mathbf{y}$$

The user will get an error message followed by the termination of the program if any of these requirements is not satisfied.

The maximum `grain_id` must be larger than or equal to [`grain_number`](grain_num.md). All information related to `grain_id` that is larger than `grain_number` is discarded.

### Related commands

The number of grain is specified in the [grain_num](grain_num.md) command.

This command becomes irrelevant when [`boolean_restart`](restart.md) = _t_, in which case there is no need for the crystallographic orientations information.

### Related files

`grain.f90`

### Default

	grain_mat 1 x 1. 0. 0. y 0. 1. 0. z 0. 0. 1.