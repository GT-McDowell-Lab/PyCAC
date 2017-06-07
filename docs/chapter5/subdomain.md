## subdomain

### Syntax

	subdomain {grain_id subdomain_number}

* `grain_id`, `subdomain_number` = positve integer

### Examples

	subdomain {1 1}
	subdomain {1 2} {2 3}
	subdomain {1 1 2 1 3 1}

### Description

This command sets the number of subdomains in each grain.

In CAC, a unit is either the primitive unit cell of the lattice (for the atomistic domain) or a finite element (for the coarse-grained domain). Finite elements of different sizes are different types of unit. In a CAC simulation cell, each spatial region consisting of the same type of unit is a subdomain, as illustrated in the figure below:

![subdomain](fig/subdomain.jpg)

The size of and the unit type in each subdomain in each grain is specified in the [unit_num](unit_num.md) and [unit_type](unit_type.md) commands, respectively. The three examples above correspond to the three examples in the [unit_num](unit_num.md) and [unit_type](unit_type.md) commands:

* In the first example, there is one grain designated by the first `1`, which has one subdomain designated by the second `1`.
* In the second example, there are two grains: the first grain has two subdomains designated by the first `2`, the second grain has three subdomains designated by `3`.
* In the third example, there are three grains, each of which has one subdomain, designated by the second `1`, the third `1`, and the fourth `1`, respectively.

The maximum `grain_id` must be larger than or equal to [`grain_number`](grain_num.md). All information related to `grain_id` that is larger than `grain_number` is discarded.

### Related commands

In the [unit_num](unit_num.md) and [unit_type](unit_type.md) commands, the maximum `subdomain_id` in each grain must equal the corresponding `subdomain_number`.

### Related files

`box_init.f90`

### Default

	subdomain 1 1