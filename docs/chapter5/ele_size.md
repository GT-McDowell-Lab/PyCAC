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

The number of atoms per element is $$(\mathrm{element\_size}+1)^3$$, where `element_size` must be even because the first order Gaussian quadrature is employed in the PyCAC code to solve the [governing equations](../chapter2/govern-eq.md). For more information of the Gaussian quadrature implementation, read Appendices A and B of [Xu et al., 2015](http://dx.doi.org/10.1016/j.ijplas.2015.05.007).

This command consists of two loops. The outer loop, illustrated by `{}`, is based on grain; the inner loop, illustrated by `[]`, is based on element size type.

* In the first example, there is only one grain, designated by the first `1`, and only one element size type, designated by the second `1`.
* In the second example, there are two grains, designated by the first `1` and the second `2`, respectively. The first grain has two element size types: the first type is the element with $$(12+1)^3 = 2197$$ atoms and the second type is the element with $$(8+1)^3 = 729$$ atoms. The second grain has three element size types: the first type is the element with $$(6+1)^3 = 343$$ atoms, the second type is the element with $$(16+1)^3 = 4913$$ atoms, and the third type is the element with $$(10+1)^3 = 1331$$ atoms.
* In the third example, there are three grains, each of which contains one element size type.

### Related commands

The maximum `grain_id` must equal [grain_number](grain_num.md). Within each grain, the maximum `element_size_type_id` must equal the corresponding [element_size_type_number](grain_uc.md).

### Related files

`model_init.f90`

### Default

None.