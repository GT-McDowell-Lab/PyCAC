# Command

This chapter describes how a CAC input script `cac.in` is formatted and the input script commands used to define a CAC simulation.

Note that the [PyCAC input script](../chapter4/README.md) has a different format.

In a CAC simulation, default settings for some commands are first established by `defaults.f90`, then the entire `cac.in` is read to override some of the default settings: (i) the sequence of commands in `cac.in` does not matter, (ii) a blank line or a line with the "\#" character in the beginning is discarded, and (iii) each command should contain no more than 350 characters. Subsequently, `input_checker.f90` is run to check whether all commands that do not have default settings are provided in `cac.in`. In preparing `cac.in`, it is important to follow the syntax and to distinguish between an interger and a real number, e.g., a real number must be written as _2._ or _2.0_, instead of _2_.

During the CAC simulation, a self-explanatory Error message, followed by termination of the program by:

	call mpi_abort(mpi_comm_world, 1, ierr)

or a Warning message may be issued if something is potentially wrong.

When [`boolean_restart`](restart.md) = _t_, the elements/nodes/atoms are read from the `cac_in.restart` file, in which case all commands in the _Simulation Cell_ category below become irrelevant; otherwise, the simulation cell is built from scratch.

Below is a list of all 36 CACS commands, grouped by category.

Simulation Cell:

[boundary](boundary.md), [box_dir](box_dir.md), [grain\_dir](grain_dir.md), [grain\_mat](grain_mat.md), [grain\_move](grain_move.md), [grain\_num](grain_num.md), [modify\_num](modify_num.md), [modify](modify.md), [subdomain](subdomain.md), [unit_num](unit_num.md), [unit_type](unit_type.md), [zigzag](zigzag.md)

Materials:

[lattice](lattice.md), [mass](mass.md), [potential](potential.md)

Settings:

[bd\_group](bd_group.md), [cal\_num](cal_num.md), [cal](cal.md), [constrain](constrain.md), [simulator](simulator.md), [dump\_num](dump_num.md), [ensemble](ensemble.md), [group\_num](group_num.md), [group](group.md), [limit](limit.md), [mass_mat](mass_mat.md) [neighbor](neighbor.md), [temperature](temperature.md)

Actions:

[deform](deform.md), [dynamics](dynamics.md), [minimize](minimize.md), [refine](refine.md), [restart](restart.md), [run](run.md)

Miscellanies:

[convert](convert.md), [debug](debug.md)