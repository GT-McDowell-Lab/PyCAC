# Command

This chapter describes how a PyCAC input script `cac.in` is formatted and the input script commands used to define a CAC simulation.

CACS reads the entire `cac.in` and then performs a simulation with all the settings. Thus, the sequence of commands does not matter.

A line with the "#" character in the beginning is treated as a comment and discarded.

Many input script errors are detected and an Error or Warning message is printed.

Below is a list of all CACS commands, grouped by category.

Simulation box:

[boundary](boundary.md), [box](box.md), [ele_size](ele_size.md), [grain_dir](grain_dir.md), [grain_mat](grain_mat.md), [grain_move](grain_move.md), [grain_num](grain_num.md), [grain_uc](grain_uc.md), [uc_num](uc_num.md), [modify_num](modify_num.md), [modify\_#](modify\_#.md), [zigzag](zigzag.md)

Materials:

[bd_group](bd_group.md), [lattice](lattice.md), [mass](mass.md), [potential](potential.md)

Settings:

[cal_num](cal_num.md), [cal\_#](cal\_#.md), [constrain](constrain.md), [simulator](simulator.md), [dump_num](dump_num.md), [ensemble](ensemble.md), [force_dir](force_dir.md), [group](group.md), [group\_#](group\_#.md), [limit](limit.md), [mass_mat](mass_mat.md), [neighbor](neighbor.md), [temperature](temperature.md)

Actions:

[deform](deform.md), [dynamics](dynamics.md), [minimize](minimize.md), [refine](refine.md), [restart](restart.md), [run](run.md)

Miscellanies:

[convert](convert.md), [debug](debug.md)