## modify_num

### Syntax

	modify_num modify_number

* `modify_number` = non-negative integer (<= 19)

### Examples

	modify_num 2

### Description

This command sets the number of [modifications](modify.md) that are made to the elements/nodes/atoms that are built from scratch, i.e., when [`boolean_restart`](restart.md) = _f_.

### Related commands

The modification style is set by the [modify](modify.md) command.

This command becomes irrelevant when [`boolean_restart`](restart.md) = _t_.

### Related files

`model_modify.f90`

### Default

	modify_num 0