# Command

This chapter describes how a CAC input script `cac.in` is formatted and the input script commands used to define a CAC simulation.

Note that the PyCAC input script 

CACS reads the entire `cac.in` and then performs a simulation with all the settings. Thus, the sequence of commands does not matter.

A blank line or a line with the "\#" character in the beginning is discarded.

Many input script errors are detected and an Error or Warning message is printed.

Each command should contain no more than 350 characters.

When preapring `cac.in`, it is important to distinguish between an interger and a real number. For example, a real number must be written as _2._ or _2.0_, instead of _2_, which may cause errors.

The default settings of some commands are provided in `defaults.f90`. The commands without default settings must be provided in `cac.in`, which is checked by `input_checker.f90`.

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