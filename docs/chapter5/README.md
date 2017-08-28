# Command

This chapter describes how the commands that are used to define a CAC simulation are formatted in a CAC input script `cac.in`.

In a CAC simulation, default settings for some commands are first established by `defaults.f90`, then the entire `cac.in` is read to override some of the default settings: (i) a blank line or a line with the "\#" character in column one (a comment line) is discarded, and (ii) each command should contain no more than 200 characters. Subsequently, `input_checker.f90` is run to check whether all commands that do not have default settings are provided in `cac.in`. In preparing `cac.in`, it is important to follow the syntax and to distinguish between an interger and a real number, e.g., a real number must be written as _2._ or _2.0_, instead of _2_.

The sequence of the commands in `cac.in` does not matter, except for the [modify](modify.md), [group](group.md), [fix](fix.md), and [cal](cal.md) commands, in which case extra commands that (i) appear later and (ii) exceed the numbers in [`modify_number`](modify_num.md), [`new_group_number`, `fix_number`, and `cal_number`](group_num.md), respectively, will be ignored. For example, if [`cal_number`](group_num.md) = _2_, the last [cal](cal.md) command below will be ignored:

	cal group_1 energy
	cal group_2 force
	cal group_3 stress

During the CAC simulation, the user may get a self-explanatory error message, followed by termination of the program by:

	call mpi_abort(mpi_comm_world, 1, ierr)

if something is potentially wrong or a warning message.

When [`boolean_restart`](restart.md) = _t_, the elements/nodes/atoms are read from the `cac_in.restart` file, in which case all commands in the _Simulation Cell_ category below become irrelevant; otherwise, the simulation cell is built from scratch.

Below is a list of all 34 CAC commands, grouped by category.

* _Simulation Cell_

	[boundary](boundary.md), [box_dir](box_dir.md), [grain\_dir](grain_dir.md), [grain\_mat](grain_mat.md), [grain\_move](grain_move.md), [grain\_num](grain_num.md), [modify\_num](modify_num.md), [modify](modify.md), [subdomain](subdomain.md), [unit_num](unit_num.md), [unit_type](unit_type.md), [zigzag](zigzag.md)

* _Materials_

	[lattice](lattice.md), [mass](mass.md), [potential](potential.md)

* _Settings_

	[cal](cal.md), [constrain](constrain.md), [dump\_num](dump_num.md), [dynamics](dynamics.md), [element](element.md), [group\_num](group_num.md), [group](group.md), [limit](limit.md), [minimize](minimize.md), [neighbor](neighbor.md), [simulator](simulator.md), [temperature](temperature.md)

* _Actions_

	[deform](deform.md), [fix](fix.md), [refine](refine.md), [restart](restart.md), [run](run.md)

* _Miscellanies_

	[convert](convert.md), [debug](debug.md)