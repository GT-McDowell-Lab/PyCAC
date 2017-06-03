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

This command generates a writable file named `debug` for debugging purpose. The file is created only when `boolean_debug` is _t_; the unit number is 13. The user can then write whatever he/she wants to `debug` using unit number 13, i.e.,

	write(13, format) output

When `boolean_mpi` is _t_, all processors have access to `debug`, otherwise only the [root](rank.md) does.

### Related commands

None.

### Related files

`debug_init.f90`

### Default

	debug f f

