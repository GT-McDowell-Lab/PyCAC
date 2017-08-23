## Input

To run a CAC simulation, one may choose to do one of the following:

1. create/modify `pycac.in`, which is then read by the [Python scripting interface](../chapter4/README.md) to create `cac.in`
2. create/modify `cac.in`, in which the [commands](../chapter5/README.md) provide all input parameters for a CAC simulation.

The `cac.in` file, along with the potential files (`embed.tab`, `pair.tab`, and `edens.tab` for the EAM potential; `lj.para` for the LJ potential), are read by the Fortran CAC code to [run the CAC simulation](../chapter1/comp-and-exec.md).

The potential files for some FCC metals are provided in the `potentials` directory.

### EAM potential

The EAM formulation for potential energy is

$$E = \frac{1}{2}\sum_i\sum_{j\neq i} V(r^{ij}) + \sum_i F(\bar{\rho}^i)$$

where

$$\bar{\rho}^i = \sum_{i \neq j} \rho^{ij}(r^{ij})$$

The first line of each `*.tab` file is

	N first_val last_val

where `N` is a positive integer that equals the number of data pair (each line starting from the second line), `first_val` and `last_val` are non-negative real numbers suggesting the first and the last datum in the first column (starting from the second line), respectively.

* In `embed.tab`, the first column is the unitless host electron energy $$\bar{\rho}$$; the second column is the embedded energy $$F$$, in eV.
* In `pair.tab`, the first column is the interatomic distance $$r$$, in Angstrom; the second column is the pair potential $$V$$, in eV.
* In `edens.tab`, the first column is the interatomic distance $$r$$, in Angstrom; the second column is the unitless local electron density $$\rho$$.

For example, the first few lines of `potentials/eam/Ag/williams/edens.tab` are

	3000 0.5018316703334310 5.995011000293092
	0.5018316703334310       8.9800288540000004E-002
	0.5036633406668621       9.0604138970000001E-002
	0.5054950110002930       9.1404200869999990E-002
	0.5073266813337241       9.2200486049999988E-002

In CAC simulations, an approximation is introduced to calculate the host electron density $$\bar{\rho}$$ of the integration points in the coarse-grained domain. For more information, read chapter 3 of [Shuozhi Xu's Ph.D. dissertation](https://smartech.gatech.edu/handle/1853/56314).

The readers may find EAM potential files in these database:

* [NIST](https://www.ctcms.nist.gov/potentials)
* [University of Edinburgh](http://www.homepages.ed.ac.uk/gja/moldy/moldy.html)
* [Other resources](https://www.ctcms.nist.gov/potentials/resources.html)

Note that most of these files do not have the format that suits the CAC simulation.

### LJ potential

The LJ formulation for potential energy is

$$E = \frac{1}{2}\sum_i\sum_{j\neq i} 4\epsilon \left[ \left( \frac{\sigma}{r^{ij}} \right)^{12} - \left( \frac{\sigma}{r^{ij}} \right)^6 \right]$$

where $$\epsilon$$ and $$\sigma$$ are two parameters. In the PyCAC code, the interatomic force, not the energy, is shifted such that the force goes continuously to zero at the cut-off distance $$r_\mathrm{c}$$, i.e., if $$r < r_\mathrm{c}$$, $$f = f(r) - f(r_\mathrm{c})$$; otherwise, $$f = 0$$.

In `lj.para`, a blank line or a line with the "\#" character in column one (a comment line) is ignored; three positive real numbers ($$\epsilon$$, $$\sigma$$, and $$r_\mathrm{c}$$) and one non-negative real number ($$r_0$$) are given in any sequence, where $$r_0$$ is a place holder that should always be 0.0 for the LJ potential. Note that for the EAM potential, $$r_0$$ equals the minimum interatomic distance, i.e., the smaller `first_val` given in `pair.tab` and `edens.tab`.

For example, `potentials/lj/Cu/kluge/lj.para` reads

	# parameters for the LJ potential
	
	epsilon   0.167
	sigma     2.315
	rcmin     0.
	rcoff     5.38784

where `epsilon` = $$\epsilon$$, `sigma` = $$\sigma$$, `rcmin` = $$r_0$$, and `rcoff` = $$r_\mathrm{c}$$.

### Other files

When [`boolean_restart`](../chapter5/restart.md) = _t_, a `cac_in.restart` file needs to be provided. This file is renamed from one of the [`cac_out_#.restart`](output.md) files, where `#` is a positive integer.

When [`boolean_restart_group`](../chapter5/restart.md) = _t_ and [`restart_group_num`](../chapter5/group_num.md) > 0, or when [`boolean_restart_refine`](../chapter5/restart.md) = _t_ and [`refine_style`](../chapter5/refine.md) = _group_, one or more `group_in_#.id` files need to be provided, where `#` is a positive integer. These files are renamed from `group_out_#.id` files, which are [created](output.md) automatically when the total number of [new group, restart group](../chapter5/group_num.md), and [boundary group](../chapter5/bd_group.md) > 0.
