## unit_num

### Syntax

	unit_num {grain_id [subdomain_id x unit_num_x y unit_num_y z unit_num_z]}

* `grain_id`, `subdomoain_id` = positive integer

* `unit_num_x`, `unit_num_y`, `unit_num_z` = positive integer

### Examples

	unit_num {1 [1 x 2 y 3 z 4]}
	unit_num {1 [1 x 8 y 20 z 12] [2 x 40 y 2 z 60]} {2 [1 x 40 y 1 z 60] [2 x 8 y 25 z 12] [3 x 6 y 7 z 10]}
	unit_num {1 [1 x 2 y 3 z 4]} {2 [1 x 6 y 1 z 2]} {3 [1 x 10 y 2 z 3]}

### Description

This command sets the size of each subdomain along three directions in each grain. The `unit_num_x`, `unit_num_y`, and `unit_num_z` are in unit of the `x`, `y`, and `z` length of the projection of the [unit](unit_type.md) (primitive unit cell in the atomistic domain or the finite element in the coarse-grained domain) on the `yz`, `xz`, and `xy` planes, respectively.

Similar to the [unit_type](unit_type.md) command, this command consists of two loops. The outer loop, illustrated by `{}`, is based on grain; the inner loop, illustrated by `[]`, is based on subdomain. Note that the curly brackets `{` and `}` as well as the square brackets `[` and `]` in the syntax/examples are to separate different subdomains and grains, the number of which are [`subdomain_number`](subdomain.md) and [`grain_number`](grain_num.md), respectively; all brackets should not be included in preparing `cac.in`.

When [`grain_number`](grain_num.md) > 1 and/or [`subdomain_number`](subdomain_num.md) > 1, the size of each subdomain set directly by this command is most likely not the same, which may be problematic in some cases, e.g., in a bicrystal, as shown in Fig. (a) below. Assume the [grain stack direction](grain_dir.md) is _x_, the CAC code will then increase the size of all subdomains along both _y_ and _z_ directions to match the subdomain(s) with the largest _y_ and _z_ length, respectively, as shown in Fig. (b) below.

![unit-num](fig/unit-num.jpg)

The three examples above correspond to the three examples in the [subdomain](subdomain.md) command.

The maximum `grain_id` must be larger than or equal to [`grain_number`](grain_num.md). All information related to `grain_id` that is larger than `grain_number` is discarded.

### Related commands

Within each grain, the maximum `subdomain_id` must equal the corresponding [subdomain_number](subdomain.md).

### Related files

`box_init.f90` and `model_init.f90`

### Default

None.