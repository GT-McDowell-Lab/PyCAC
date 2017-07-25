## unit_type

### Syntax

	unit_type {grain_id [subdomain_id unitype]}

* `grain_id`, `subdomain_id` = positive integer

* `unitype` = 1 or positive even integer (>= 4)

### Examples

	unit_type {1 [1 12]}
	unit_type {1 [1 1] [2 8]} {2 [1 6] [2 16] [3 10]}
	unit_type {1 [1 14]} {2 [1 1]} {3 [1 6]}

### Description

The command sets the `unitype` in each subdomain in each grain.

Similar to the [unit_num](unit_num.md) command, this command consists of two loops. The outer loop, illustrated by `{}`, is based on grain; the inner loop, illustrated by `[]`, is based on subdomain. Note that the curly brackets `{` and `}` as well as the square brackets `[` and `]` in the syntax/examples are to separate different grains and subdomains, the number of which are [`grain_number`](grain_num.md) and [`subdomain_number`](subdomain.md), respectively; all brackets should not be included in preparing `cac.in`.

The number of atoms per unit is $$(\mathrm{unitype}+1)^3$$, where `unitype` must be either 1 (atomistic domain) or an even integer that is no less than 4 (coarse-grained domain): in the latter case, (i) it must be even because the first order Gaussian quadrature is employed in the PyCAC code to solve the [governing equations](../chapter2/govern-eq.md), (ii) it must be >= 4 because the second nearest neighbor (2NN) element with 125 integration points is employed and so there cannot be fewer than 125 atoms in one element. For more information of the 2NN element and the Gaussian quadrature implementation, read Appendices A and B of [Xu et al., 2015](http://dx.doi.org/10.1016/j.ijplas.2015.05.007).

The three examples above correspond to the three examples in the [subdomain](subdomain.md) command:

* In the first example, there is only one grain, designated by the first _1_, having only one subdomain, designated by the second _1_, with the `unitype` = _12_.
* In the second example, there are two grains, designated by the first _1_ and the second _2_, respectively. The first grain has two subdomains: the first is atomistics because `unitype` = _1_; the second contains elements each of which has $$(8+1)^3 = 729$$ atoms. The second grain has three subdomains: the first contains elements each of which has $$(6+1)^3 = 343$$ atoms; the second contains elements each of which has $$(16+1)^3 = 4913$$ atoms; the third contains elements each of which has $$(10+1)^3 = 1331$$ atoms.
* In the third example, there are three grains, each of which contains one unit type. Note that the second grain is atomistics because `unitype` = _1_.

The maximum `grain_id` must be larger than or equal to [`grain_number`](grain_num.md). All information related to `grain_id` that is larger than `grain_number` is discarded.

### Related commands

Within each grain, the maximum `subdomain_id` must equal the corresponding [subdomain_number](subdomain.md).

This command becomes irrelevant when [`boolean_restart`](restart.md) = _t_, in which case there is no need for the subdomain information.

### Related files

`model_init.f90`

### Default

None.