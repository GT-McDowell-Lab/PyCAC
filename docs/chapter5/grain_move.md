## grain_move

### Syntax

	grain_move {grain_id move_x move_y move_z}

* grain\_id = integer

* move\_x, move\_y, move\_z = real number

### Examples

	grain_move {1 0.0 0.0 0.0} {2 0.5 -0.301 0.001}

### Description

Set the displacement of each grain along the _x_, _y_, and _z_ axis. The number of grain is specified by the [grain_num](grain_num.md) command.

### Related commands

This command is somewhat similar to the [grain_dir](grain_dir.md) in that the same result of the `overlap` would be achieved if the axis is the same as that is set by the `direction`.

### Related files

`box_init.f90`

### Default

	grain_move 1 0.

