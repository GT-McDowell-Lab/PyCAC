## refine

### Syntax

	refine refine_type refine_group_number all_element_size

* refine\_type = _all_ or _group_

* refine\_group\_number, all\_element\_size = integer

### Examples

	refine all 1 6
	refine group 1 12
	refine group 2 6

### Description

Set refinement properties after reading a `cac_in.restart` file.

`refine_type` is either _all_ or _group_.

`refine_group_number`, relevant only when `refine_type` is _group_, is the number of groups that need to be refined to atomic scale. For each group, a file named `group_in_#.id` is required, where `#` is 1, 2, 3 ...

`all_element_size`, relevant only when `refine_type` is _all_, is the size of the element in the coarse-grained domain. Note that currently, only one type of element size is allowed in this command. In the first example, the `cac_in.restart` file refers to a model with a coarse-grained domain with the same type of elements having $$(6+1)^3 = 343$$ atoms.

### Related commands

This command is relevant only when the `boolean_restart_refine` is _t_ in the [restart](restart.md) command.

### Related files

`refine_init.f90`

### Default

None.