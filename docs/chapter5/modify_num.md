## modify_num

### Syntax

	modify_num modify_number

* `modify_number` = positive integer (<= 19)

### Examples

	modify_num 2

### Description

This command sets the number of [modifications](modify.md) that are made to the elements/nodes/atoms that are [created from scratch](restart.md), etc.

### Related commands

The modification style is set by the [modify](modify.md) command.

### Related files

`model_modify.f90`

### Default

	modify_num 0