## Atomic field theory

The theoretical foundation of the CAC method is the atomistic field theory (AFT) [1,2], which is an extension of the Irving Kirkwood (IK)'s non-equilibrium statistical mechanical formulation of "_the hydrodynamics equations for a single component, single phase system_" [3] to a two-level structural description of crystalline materials. It employs the two-level structural description of all crystals in solid state physics, i.e., the well known equation of "crystal structure = lattice + basis" [4]. As a result of the bottom-up atomistic formulation, all the essential atomistic information of the material, including the crystal structure and the interaction between atoms, are built in the formulation. The result is a concurrent atomistic-continuum representation of balance laws for both atomic and continuum regions in the following form [1,2]

$$\frac{\mathrm{d} \rho^\alpha}{\mathrm{d} t} + \rho^\alpha (\nabla_\mathbf{x} \cdot \mathbf{v} + \nabla_{\mathbf{y}^\alpha} \cdot \Delta \mathbf{v}^\alpha) = 0$$

$$\rho^\alpha \frac{\mathrm{d}}{\mathrm{d} t} (\mathbf{v} + \Delta \mathbf{v}^\alpha) = \nabla_\mathbf{x} \cdot \mathbf{t}^\alpha + \nabla_{\mathbf{y}^\alpha} \cdot \mathbf{\tau}^\alpha + \mathbf{f}_\mathrm{ext}^\alpha$$

$$\rho^\alpha \frac{\mathrm{d} e^\alpha}{\mathrm{d} t} = \nabla_\mathbf{x} \cdot \mathbf{q}^\alpha + \nabla_{\mathbf{y}^\alpha} \cdot \mathbf{j}^\alpha + \mathbf{t}^\alpha : \nabla_\mathbf{x} (\mathbf{v} + \Delta \mathbf{v}^\alpha) + \mathbf{\tau}^\alpha : \nabla_{\mathbf{y}^\alpha} (\mathbf{v} + \Delta \mathbf{v}^\alpha)$$

In AFT, a crystalline material is viewed as a continuous collection of lattice points; embedded within each point is a unit cell with a group of discrete atoms, as shown in the figure below. In this way, the micromorphic theory is connected with molecular dynamics and is expanded to the atomic scale. Here, the local density function is continuous at the level of the unit cell, but discrete in terms of the discrete atoms inside the unit cell. AFT was originally designed with polyatomic crystalline materials in mind, but can also be applied to monatomic crystals.

<figure><img src='fig/cheny.png'><figcaption>Macro- and micro-motions of a material particle P in (a) micromorphic theory and (b) AFT. Left in (a) and (b) is the reference state at time 0 while right is the deformation state at time $$t$$. $$\mathbf{X}$$ and $$\mathbf{x}$$ are the positions of the mass center of the unit cell, $$\Xi$$ and $$\xi$$ are internal positions, $$\mathbf{Y}$$ and $$\mathrm{y}^\alpha$$ are positions of atom $$\alpha$$ with respect to $$\mathrm{X}$$ and $$\mathrm{x}$$, respectively, $$N_\alpha$$ is the number of atoms in a unit cell.</figcaption></figure>

<br>
### The CAC governing equations for conservative systems 

In Eulerian coordinates, the governing equations of the CAC method for a monatomic crystal are

$$\frac{\partial \rho}{\partial t} + \nabla_\mathbf{r} \cdot (\rho\mathbf{v}) = 0$$

$$\frac{\partial (\rho\mathbf{v})}{\partial t} - \nabla_\mathbf{r} \cdot (\mathbf{t} - \rho\mathbf{v} \otimes \mathbf{v}) - \mathbf{f}_\mathrm{ext} = \mathbf{0}$$

$$\frac{\partial (\rho e)}{\partial t} - \nabla_\mathbf{r} \cdot (\mathbf{	q} + \mathbf{t} \cdot \mathbf{v} - \rho e \mathbf{v}) - \mathbf{f}_\mathrm{ext} \cdot \mathbf{v} = 0$$

where $$\rho$$ is the microscopic local mass density, $$t$$ is the time, $$\mathbf{r}$$ is the physical space coordinates, $$\mathbf{v}$$ is the local velocity field, $$\mathbf{f}_\mathrm{ext}$$ is the external body force field, $$\mathbf{t}$$ is the 2$$^\mathrm{nd}$$ rank momentum flux tensor, $$e$$ is the energy, and $$\mathbf{q}$$ is the heat flux. Assuming that the temperature gradient is negligible and there is no external force density, the governing equations in CAC are reduced to

$$\rho \ddot{\mathbf{r}} - \mathbf{f}_\mathrm{int} = \mathbf{0}$$

where $$\mathbf{f}_\mathrm{int}$$ is the internal force density and the superposed dots denote the material time second derivative. This governing equation is solved directly in dynamic CAC while is used to derive the equivalent nodal force/energy in quasistatic CAC.

### CAC and the equilibrium ensembles

### References

1. Youping Chen, James Lee. [Atomistic formulation of a multiscale theory for nano/micro physics](http://dx.doi.org/10.1080/14786430500362595), _Philos. Mag._ 85 (2005) 4095-4126
2. Youping Chen. [Reformulation of microscopic balance equations for multiscale materials modeling](http://dx.doi.org/10.1063/1.3103887), _J. Chem. Phys._ 130 (2009) 134706

