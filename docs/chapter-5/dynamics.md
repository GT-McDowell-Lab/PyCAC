
### Syntax

	dynamics dyn_style energy_min_freq damping_coefficient

* `dyn_style` = _ld_ or _qd_ or _vv_

		ld is Langevin dynamics
		qd is quenched dynamics
		vv is Velocity Verlet

* `energy_min_freq` = positive integer

* `damping_coefficient` = positive real number

### Examples

	dynamics ld 300 1.
	dynamics qd 500 5.

### Description

This command sets the style of the dynamic run in CAC simulations.

When `dyn_style` = _ld_, the [Langevin dynamics](https://en.wikipedia.org/wiki/Langevin_dynamics) is performed, i.e.,

$$m \ddot{\mathbf{R}} = \mathbf{F} - \gamma m\dot{\mathbf{R}} + \Theta(t)$$

where $m$ is the normalized lumped mass or the atomic mass, $\mathbf{R}$ is the nodal/atomic position, $\mathbf{F}$ is the equivalent nodal/atomic force, $\gamma$ is the `damping_coefficient` in ps$^{-1}$, and $t$ is the time in ps. The Velocity Verlet form is employed to solve the equations of motion, as given in Eqs. 1-3 in [Xu et al., 2016](http://dx.doi.org/10.1016/j.ijsolstr.2016.03.030). The velocity $\dot{\mathbf{R}}$ is updated in `langevin_vel.f90`.

The _ld_ style is used to keep a constant temperature in CAC simulations by adding to the force $\mathbf{F}$ a time-dependent Gaussian random variable $\Theta(t)$ with zero mean and variance of $\sqrt{2m\gamma k_\mathrm{B} T/\Delta t}$, where $m$ is the atomic mass, $k_\mathrm{B}$ is the Boltzmann constant ($8.6173324\times 10^{-5} \mathrm{eV/K}$), $T$ is the temperature in K, and $\Delta t$ is the [`time_step`](run.md) in ps. The random variable is calculated and added to the force in `langevin_force.f90`. Note that when $T = 0$, the equation above reduces to

$$m \ddot{\mathbf{R}} = \mathbf{F} - \gamma m\dot{\mathbf{R}}$$

which is the equation of motion in damped molecular dynamics.

When `dyn_style` = _qd_, the quenched dynamics is performed, in which

* if the force and velocity point in opposite directions, the velocity is zeroed, i.e.,

$$\mathrm{if}\ \dot{\mathbf{R}} \cdot \mathbf{F} < 0, \dot{\mathbf{R}} = 0$$

* otherwise, the velocity is projected along the direction of the force, such that only the component of velocity parallel to the force vector is used, i.e.,

$$\mathrm{if}\ \dot{\mathbf{R}} \cdot \mathbf{F} \geq 0, \dot{\mathbf{R}} = \frac{(\dot{\mathbf{R}} \cdot \mathbf{F})\mathbf{F}}{|\mathbf{F}|^2}$$

Note that with the _qd_ style, which was first used in [Xu et al., 2016](http://dx.doi.org/10.1038/npjcompumats.2015.16), the temperature is considered 0 K or very nearly so.

When `dyn_style` = _vv_, a dynamic simulation following

$$m \ddot{\mathbf{R}} = \mathbf{F}$$

is performed using the Velocity Verlet scheme.

Note that the _vv_ style cannot be used to keep a constant [temperature](temperature.md) and the _qd_ style cannot be used to keep a finite [temperature](temperature.md). When [`boolean`](temperature.md) = _t_, if the _vv_ style is chosen and if, for a finite [temperature](temperature.md), the _qd_ style is chosen, the user will get a warning message.

The `energy_min_freq` is the frequency with which the energy minimization is performed during a dynamic run. This is relevant only if [`simulator_style`](simulator.md) = _hybrid_.

### Related commands

[run](run.md) and [simulator](simulator.md).

### Related files

`dynamics_init.f90`, `dynamics.f90`, `langevin_dynamics.f90`, `quenched_dynamics.f90`, `hybrid.f90`, among many

### Default

	dynamics vv 500 1.
