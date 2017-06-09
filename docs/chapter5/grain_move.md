## grain_move

### Syntax

	grain_move {grain_id move_x move_y move_z}

* `grain_id` = positive integer

* `move_x`, `move_y`, `move_z` = real number

### Examples

	grain_move {1 0. 0. 0.} {2 0.5 -0.301 0.001}

### Description

This command sets the displacements of the origin of each grain along the _x_, _y_, and _z_ axis. Note that the curly brackets `{` and `}` in the syntax/examples are to separate different grains, the number of which is [`grain_number`](grain_num.md); all brackets should not be included in preparing `cac.in`.

The maximum `grain_id` must be larger than or equal to [`grain_number`](grain_num.md). All information related to `grain_id` that is larger than `grain_number` is discarded.

### Related commands

When the displacement vector is along the [group stack direction](grain_dir.md), result by this command may be equivalent to setting the `overlap` between adjacent grains. Note that the same `overlap` is applied between all adjacent grains, while this command sets the displacement vector for each grain independently.

This command becomes irrelevant when [`boolean_restart`](restart.md) = _t_.

### Related files

`box_init.f90`

### Default

	grain_move 1 0. 0. 0.