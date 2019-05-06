## Atomistic field theory

The theoretical foundation of the CAC method is the atomistic field theory (AFT) [1,2], which is an extension of the Irving Kirkwood (IK)'s non-equilibrium statistical mechanical formulation of "_the hydrodynamics equations for a single component, single phase system_" [3] to a two-level structural description of crystalline materials. It employs the two-level structural description of all crystals in solid state physics, i.e., the well known equation of "crystal structure = lattice + basis" [4]. As a result of the bottom-up atomistic formulation, all the essential atomistic information of the material, including the crystal structure and the interaction between atoms, are built in the formulation. A schematic of micromorphic theory and AFT is given below.

<figure><img src='fig/cheny.png'><figcaption>Macro- and micro-motions of a material particle P in (a) micromorphic theory and (b) AFT. Left in (a) and (b) is the reference state at time 0 while right is the deformation state at time $$t$$. $$\mathbf{X}$$ and $$\mathbf{x}$$ are the positions of the mass center of the unit cell, $$\Xi$$ and $$\xi$$ are internal positions, $$\mathbf{Y}$$ and $$\mathbf{y}^\alpha$$ are positions of atom $$\alpha$$ with respect to $$\mathbf{X}$$ and $$\mathbf{x}$$, respectively, $$N_a$$ is the number of atoms in a unit cell.</figcaption></figure>

### The governing equations for conservative systems 

The result is a concurrent atomistic-continuum representation of balance laws for both atomistic and continuum coarse-grained domains in the following form [1,2]:

$$\frac{\mathrm{d} \rho^\alpha}{\mathrm{d} t} + \rho^\alpha (\nabla_\mathbf{x} \cdot \mathbf{v} + \nabla_{\mathbf{y}^\alpha} \cdot \Delta \mathbf{v}^\alpha) = 0$$

$$\rho^\alpha \frac{\mathrm{d}}{\mathrm{d} t} (\mathbf{v} + \Delta \mathbf{v}^\alpha) = \nabla_\mathbf{x} \cdot \mathbf{t}^\alpha + \nabla_{\mathbf{y}^\alpha} \cdot \mathbf{\tau}^\alpha + \mathbf{f}_\mathrm{ext}^\alpha$$

$$\rho^\alpha \frac{\mathrm{d} e^\alpha}{\mathrm{d} t} = \nabla_\mathbf{x} \cdot \mathbf{q}^\alpha + \nabla_{\mathbf{y}^\alpha} \cdot \mathbf{j}^\alpha + \mathbf{t}^\alpha : \nabla_\mathbf{x} (\mathbf{v} + \Delta \mathbf{v}^\alpha) + \mathbf{\tau}^\alpha : \nabla_{\mathbf{y}^\alpha} (\mathbf{v} + \Delta \mathbf{v}^\alpha)$$

where $$\mathbf{x}$$ is the physical space coordinate; $$\mathbf{y}^\alpha (\alpha = 1, 2, \ldots, N_a$$ with $$N_a$$ being the total number of atoms in a unit cell) are the internal variables describing the position of atom $$\alpha$$ relative to the mass center of the lattice cell located at $$\mathbf{x}$$; $$\rho^\alpha$$, $$\rho^\alpha(\mathbf{v} + \Delta \mathbf{v}^\alpha)$$, and $$\rho^\alpha e^\alpha$$ are the local densities of mass, linear momentum and total energy, respectively; $$\mathbf{v} + \Delta \mathbf{v}^\alpha$$ is the atomic-level velocity and $$\mathbf{v}$$ is the velocity field; $$\mathbf{f}_\mathrm{ext}^\alpha$$ is the external force field; $$\mathbf{t}^\alpha$$ and $$\mathbf{q}^\alpha$$ are the stress and heat flux due to the homogeneous deformation of lattice, respectively; $$\mathbf{\tau}^\alpha$$ and $$\mathbf{j}^\alpha$$ are the stress and heat flux due to the reorganizations of atoms within the lattice cells, respectively.

For monatomic crystals, which [PyCAC can simulate](../chapter1/pycac-feature.md), $$\mathbf{y}^\alpha = \mathbf{0}$$ and $$N_a = 1$$; the governing equations reduce to

$$\frac{\mathrm{d} \rho}{\mathrm{d} t} + \rho \nabla_\mathbf{x} \cdot \mathbf{v} = 0$$

$$\rho \frac{\mathrm{d} \mathbf{v}}{\mathrm{d} t} = \nabla_\mathbf{x} \cdot \mathbf{t} + \mathbf{f}_\mathrm{ext}$$

$$\rho \frac{\mathrm{d} e}{\mathrm{d} t} = \nabla_\mathbf{x} \cdot \mathbf{q} + \mathbf{t} : \nabla_\mathbf{x} \mathbf{v}$$.

For conservative systems, i.e., a system in the absence of an internal source that generates or dissipates energy, the AFT energy equation is equivalent to the AFT linear momentum equation. Because of its [current features](../chapter1/pycac-feature.md), only the first two governing equations are explicitly implemented into PyCAC.  Employing the classical definition of kinetic temperature, which is proportional to the kinetic part of the atomistic stress, the linear momentum equations can be expressed in a form that involves the internal force density $$\mathbf{f}_\mathrm{int}^\alpha$$ and temperature $$T$$ [5-7],

$$\rho^\alpha \ddot{\mathbf{u}}^\alpha + \frac{\gamma^\alpha k_\mathrm{B}}{\Delta V} \nabla_\mathbf{x} T = \mathbf{f}_\mathrm{int}^\alpha + \mathbf{f}_\mathrm{ext}^\alpha, \quad \alpha = 1, 2, \ldots, N_a$$

where $$\mathbf{u}^\alpha$$ is the displacement of the $$\alpha$$th atom at point $$\mathbf{x}$$; the superposed dots denote the material time derivative; $$\Delta V$$ is the volume of the finite-sized material particle (the primitive unit cell for crystalline materials) at $$\mathbf{x}$$; $$k_\mathrm{B}$$ is the Boltzmann constant; $$\gamma^\alpha = \rho^\alpha / \sum^{N_a}_{\alpha = 1} \rho^\alpha$$, and $$\mathbf{f}_\mathrm{int}^\alpha$$ is the internal force density and is a nonlinear nonlocal function of relative atomic displacements. 

$$\int_{\Omega(\mathbf{x})} \Phi_\xi(\mathbf{x}) (\rho^\alpha \ddot{\mathbf{u}}^\alpha(\mathbf{x}) + \mathbf{f}_\mathrm{T}^\alpha(\mathbf{x}) - \mathbf{f}_\mathrm{int}^\alpha(\mathbf{x}) - \mathbf{f}_\mathrm{ext}^\alpha(\mathbf{x})) \mathrm{d} \mathbf{x} = 0$$

where $$\Omega(\mathbf{x})$$ is the simulation domain; the integrals can be evaluated using numerical integration methods such as Gaussian quadrature, leading to a set of discretized governing equations with the finite element nodal displacements as the unknowns to be solved. Note that in PyCAC, the $$\mathbf{f}_\mathrm{T}^\alpha(\mathbf{x})$$ term has not yet been implemented as (i) the effect on mechanical properties in a constant temperature field is small and (ii) work is underway to compare different descriptions of temperature in the coarse-grained domain.

The accuracy, efficiency, and stability of the CAC simulator are then determined by the two approximations: the shape function and the numerical integration. Simulation results can be displayed in terms of finite elements, which can also be mapped back to atomic positions and be used to plot the atomic trajectories. With the only constitutive relation being the nonlocal atomic force-displacement relation, continuity between elements in the usual finite element method is not required. Consequently, nucleation and propagation of dislocations and/or cracks can be simulated via sliding and separation between finite elements.

### AFT and the equilibrium ensembles

The local densities defined in the Irving and Kirkwood formulations are ensemble averaged point functions. The ensemble averaging was described by Irving and Kirkwood as "_repeating the observations many times_" [3]. In the early version of the AFT formulation [1], the local densities were also defined as ensemble averages and hence the governing equations were written in terms of ensemble-averaged local densities. In the later version of the AFT formulation [2],   the local densities are instantaneous quantities, according to argument by Evan and Morris [8], who wrote "_$$\ldots$$ the reason for considering instantaneous expressions is two-fold. The fluxes are based upon conservation laws and these laws are valid instantaneously for every member of the ensemble. They do not require ensemble averaging to be true. Secondly, most computer simulation involves calculating system properties from a single system trajectory. Ensemble averaging is almost never used because it is relatively expensive in computer time_".

### References

1. Youping Chen, James Lee. [Atomistic formulation of a multiscale theory for nano/micro physics](http://dx.doi.org/10.1080/14786430500362595), _Philos. Mag._ 85 (2005) 4095-4126
2. Youping Chen. [Reformulation of microscopic balance equations for multiscale materials modeling](http://dx.doi.org/10.1063/1.3103887), _J. Chem. Phys._ 130 (2009) 134706
3. J.H. Irving, Jhon G. Kirkwood. [The statistical mechanical theory of transport processes. IV. The equations of hydrodynamics](http://dx.doi.org/10.1063/1.1747782), _J. Chem. Phys._ 18 (1950) 817-829
10. Xiang Chen, Adrian Diaz, Liming Xiong, David L. McDowell, Youping Chen. [Passing waves from atomistic to continuum](http://dx.doi.org/10.1016/j.jcp.2017.10.038), _J. Comput. Phys._ 354 (2018) 393-402