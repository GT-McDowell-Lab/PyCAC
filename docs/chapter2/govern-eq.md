## Governing equations of the CAC method

In Eulerian coordinates, the governing equations of the CAC method for a monoatomic crystal are

$$\frac{\partial \rho}{\partial t} + \nabla_\mathbf{r} \cdot (\rho\mathbf{v}) = 0$$

$$\frac{\partial (\rho\mathbf{v})}{\partial t} - \nabla_\mathbf{r} \cdot (\mathbf{t} - \rho\mathbf{v} \otimes \mathbf{v}) - \mathbf{f}_\mathrm{ext} = \mathbf{0}$$

$$\frac{\partial (\rho e)}{\partial t} - \nabla_\mathbf{r} \cdot (\mathbf{	q} + \mathbf{t} \cdot \mathbf{v} - \rho e \mathbf{v}) - \mathbf{f}_\mathrm{ext} \cdot \mathbf{v} = 0$$

where $$\rho$$ is the microscopic local mass density, $$t$$ is the time, $$\mathbf{r}$$ i sthe physical space coordinates, $$\mathbf{v}$$ is the local velocity field, $$\mathbf{f}_\mathrm{ext}$$ is the external body force field, $$\mathbf{t}$$ is the 2$$^\mathrm{nd}$$ rank momentum flux tensor, $$e$$ is the energy, and $$\mathbf{q}$$ is the heat flux. Assuming that the temperature gradient is negligible and there is no external force density, the governing equations in CAC is reduced to

$$\rho \ddot{\mathbf{r}} - \mathbf{f}_\mathrm{int} = \mathrm{0}$$

where $$\mathbf{f}_\mathrm{int}$$ is the internal force density and the superposed dots denote the material time second derivative.