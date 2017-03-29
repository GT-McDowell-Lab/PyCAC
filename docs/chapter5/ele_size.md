## ele_size

### Syntax

	ele_size {grain_id [element_size_type_id element_size]}

* all = integer

### Examples

	ele_size 1 1 12
	ele_size 1 1 12 2 8 2 1 6 2 16 3 10
	ele_size 1 1 14 2 1 4 3 1 6

### Description

Set the `element_size` in each element\_size\_type and in each grain in a PyCAC simulation. The number of atoms per element is then $$(element\_size+1)^3$$. Note that `element_size` must be even.

This command consists of two loops, the outer loop is grain. In the first example, there is only one grain, marked by the first `1`, and only one element\_size\_type, marked by the second `1`. In the second example, there are two grains, marked by the first `1` and the second `2`, respectively. In other words, the second example is

	ele_size {1 1 12 2 8} {2 1 6 2 16 3 10}
	
where the first and the second grains are in the first and the second curly brackets, respectively. Note that the curly braces are not allowed in actual command, but just an illustration here. Within each grain, the second example is also

	ele_size {1 [1 12] [2 8]} {2 [1 6] [2 16] [3 10]}

where each pair of square brackets refers to a element\_size\_type. Within the first grain, there are two element\_size\_types: the first type is the element with $$(12+1)^3$$ atoms, the second type is the element with $$(8+1)^3$$ atoms. Within the second grain, there are three element\_size\_types: the first type is the element with $$(6+1)^3$$ atoms, the second type is the element with $$(16+1)^3$$ atoms, and the third type is the element with $$(10+1)^3$$ atoms. Similarly, the third example is

	ele_size {1 [1 14]} {2 [1 4]} {3 [1 6]}

where there are three grains, each of which contains one element\_size\_type.

### Related commands

The maximum `grain_id` must be the number of grain dictated by the [grain\_num](grain_num.md) command. Within each grain, the maximum `element_size_type_id` must be the number of elment size type dictated by the [grain\_uc](grain_uc.md) command.

### Related files

`model_init.f90`

### Default

None.
