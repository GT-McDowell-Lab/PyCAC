## restart

### Syntax

	restart boolean_restart boolean_restart_refine boolean_restart_group

* boolean\_restart, boolean\_restart\_refine, boolean\_restart\_group = _t_ or _f_

		t is true
		f is false

### Examples

	restart f f f
	restart t f f
	restart t t f

### Description

Set the restart properties.

When `boolean_restart` is _t_, the code reads information of the elements/nodes/atoms from the `cac_in.restart` file. Otherwise, the model is built from scratch and both `boolean_restart_refine` and `boolean_restart_group` become _f_.

When `boolean_restart_refine` is _t_, some elements in the coarse-grained domain, if any, are refined to atomic scale.

When `boolean_restart_group` is _t_, some group information is read from the `group_in_#.id` file, instead of being created from scratch.

### Related commands

When `boolean_restart_refine` is _t_, the refine properties are set by the [refine](refine.md) command. Otherwise, the [refine](refine.md) command becomes irrelevant.

When `boolean_restart_group` is _t_, the restarted group number is set by the [group_num](group_num.md). While the `group_in_#.id` file contains some group information, e.g., the ID of elements/atoms, there is additional information, e.g., the velocity, that needs to be specified by the [group](group.md) command.

### Related files

`read_restart.f90` and `write_restart.f90`

### Default

	restart f f f