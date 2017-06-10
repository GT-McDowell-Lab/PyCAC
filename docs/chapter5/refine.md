## refine

### Syntax

	refine refine_style refine_group_number unitype

* `refine_style` = _all_ or _group_

* `refine_group_number`, `unitype` = positive integer

### Examples

	refine all 1 6
	refine group 1 12
	refine group 2 6

### Description

This command sets refinement styles when [`boolean_restart_refine`](restart.md) = _t_.

There are two `refine_style`: _all_ or _group_.

When `refine_style` = _all_, all elements in the coarse-grained domain are refined into atomic scale. This is used when, e.g., the users want to perform an equivalent full atomistic simulation with the CAC code. Currently, this option is correctly trigered only when all elements have the same size, i.e., the same [`unitype`](unit_type.md) had been used in all coarse-grained [subdomains](subdomain.md) based on which the `cac_in.restart` file was created. In the first example, the `cac_in.restart` file refers to a simulation cell with elements each of which has $$(6+1)^3 = 343$$ atoms. `refine_group_number` is irrevelant for this `refine_style`.

When `refine_style` = _group_, selected elements in the  `group_in_#.id` files (where `#` is a positive integer starting from 1) in the coarse-grained domain are refined into atomic scale. The `group_in_#.id` files are renamed from the `group_out_#.id` files that were created automatically in previous CAC simulations when the total number of groups > 0. `unitype` is irrevelant for this `refine_style`.

### Related commands

This command becomes irrelevant when [`boolean_restart_refine`](restart.md) = _f_.

### Related files

`refine_init.f90`

### Default

None.