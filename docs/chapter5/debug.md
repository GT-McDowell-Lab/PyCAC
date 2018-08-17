## debug

### Syntax

	debug boolean_debug boolean_mpi

* `boolean_debug`, `boolean_mpi` = _t_ or _f_

		t is true
		f is faulse

### Examples

	debug t f
	debug t t

### Description

This command generates a writable file named `debug` for debugging purpose. The file is created only when `boolean_debug` = _t_; the unit number is 13. The user can then write whatever he/she wants to the `debug` file using unit number 13, i.e.,

	write(13, format) output

When `boolean_mpi` = _t_, all processors have access to the `debug` file, otherwise only the [root](../chapter8/rank.md) does.

### Related commands

None.

### Related files

`debug_init.f90`

### Default

	debug f f

