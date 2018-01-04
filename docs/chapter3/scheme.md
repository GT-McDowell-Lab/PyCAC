## Scheme

A flowchart of the CAC simulation scheme based on [spatial decomposition](parall.md) is presented below:

![cac-scheme](fig/main.jpg)

where there are three types of CAC simulations: dynamics, quasistatics, and hybrid, specified by the [simulator](../chapter5/simulator.md).

In CAC simulations, the elements/nodes/atoms information can either be created from scratch (`model_setup.f90`) or read from the `cac_in.restart` file (`read_restart.f90`), depending on the parameters in the [restart](../chapter5/restart.md) command.

The dynamic CAC scheme is

![dynamic-scheme](fig/dynamics.jpg)

The quasistatic CAC scheme is

![static-scheme](fig/statics.jpg)

The hybrid CAC scheme is

![static-scheme](fig/hybrid.jpg)

All these four figures are adapted from Xu et al. More information of the dynamic and quasistatic CAC can be found in the [`dynamics`](../chapter5/dynamics.md) and [`minimize`](../chapter5/minimize.md) commands, respectively.