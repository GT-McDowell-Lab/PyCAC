## ele_size

### Syntax

	ele_size {grain_id [element_size_type_id element_size]}

* `grain_id`, `element_size_type_id` = positive integer
* `element_size` = positive even integer

### Examples

	ele_size {1 [1 12]}
	ele_size {1 [1 12] [2 8]} {2 [1 6] [2 16] [3 10]}
	ele_size {1 [1 14]} {2 [1 4]} {3 [1 6]}

### Description

The command sets the `element_size` in each element size type and in each grain in a PyCAC simulation. Note that the curly brackets `{` and `}` as well as the square brackets `[` and `]` in the syntax/examples are to separate different element size types and grains, the number of which is [`element_size_type_number`](grain_uc.md) and [`grain_number`](grain_num.md), respectively; all brackets should not be included in preparing `cac.in`.

The number of atoms per element is $$(`element_size`+1)^3$$, where `element_size` must be even because the first order Gaussian quadrature is employed in the PyCAC code to solve the [governing equations](../chapter2/govern-eq.md). For more information of the Gaussian quadrature implementation, read Appendices A and B of [Xu et al., 2015](http://dx.doi.org/10.1016/j.ijplas.2015.05.007).

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
