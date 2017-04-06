## modify_num

### Syntax

	modify_num number_of_modification

* number\_of\_modification = integer (<= 19)

### Examples

	modify_num 2

### Description

Set the number of modifications to the simulation cell that is created from scratch instead of read from a `*.restart` file.

### Related commands

The specific types of modifications is set by the [modify](modify.md) command.

### Related files

`model_modify.f90`

### Default

	modify_num 0