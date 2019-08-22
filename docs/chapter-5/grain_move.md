
### Syntax

	grain_move {grain_id move_x move_y move_z}

* `grain_id` = positive integer

* `move_x`, `move_y`, `move_z` = real number

### Examples

	grain_move {1 0. 0. 0.} {2 0.5 -0.301 0.001}

### Description

This command sets the displacements of the origin of each grain along the _x_, _y_, and _z_ axis, respectively. When `move_x`, `move_y`, and `move_z` are all 0.0, the next grain's lower boundary is the current grain's upper boundary along the [grain stack direction](grain_dir.md). Note that the curly brackets `{` and `}` in the syntax/examples are to separate different grains, the number of which is [`grain_number`](grain_num.md); all brackets should not be included in preparing `cac.in`.

The maximum `grain_id` must be larger than or equal to [`grain_number`](grain_num.md). All information related to `grain_id` that is larger than `grain_number` is discarded.

### Related commands

When the displacement vector is along the [grain stack direction](grain_dir.md), result by this command may be equivalent to setting the [`overlap`](grain_dir.md) between adjacent grains. Note that the same [`overlap`](grain_dir.md) is applied between all adjacent grains, while this command sets the displacement vector for each grain independently.

This command becomes irrelevant when [`boolean_restart`](restart.md) = _t_, in which case there is no need for the grain information.

### Related files

`box_init.f90`

### Default

	grain_move 1 0. 0. 0.