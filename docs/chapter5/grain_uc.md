## grain_uc

### Syntax

	grain_uc {grain_id element_size_type_number}

* grain_id, element_size_type_number = integer

### Examples

	grain_uc {1 3}
	grain_uc {1 1} {2 2}

### Description

Set the number of `element_size_type` in each grain. The first example suggests that there are three types of `element_size` in the first grain, which could be, say, `6`, `16` and `10`. When the `element_size` is `6`, this type of element contains $$(6+1)^3 = 343$$ atoms.

### Related commands

The specific `element_size` is set in the [ele_size](ele_size.md) command.

### Related files

`box_init.f90`

### Default

None.