## EAM potential

As mentioned [earlier](../chapter3/input.md) The EAM formulation for the potential energy is

$$E = \frac{1}{2}\sum_i\sum_{j\neq i} V(r^{ij}) + \sum_i F(\bar{\rho}^i)$$

where $$V$$ is the pair potential, $$F$$ is the embedding potential, and $$\bar{\rho}$$ is the host electron density, i.e.,

$$\bar{\rho}^i = \sum_{i \neq j} \rho^{ij}(r^{ij})$$

where $$\rho$$ is the local electron density.

The force is

$$\mathbf{f}_k = -\frac{\partial E}{\partial \mathbf{r}_k} = -\frac{1}{2} \frac{\partial \sum_i \sum_{j \atop j \neq i}V(r_{ij})}{\partial \mathbf{r}_k}-\frac{\partial \sum_i F(\bar{\rho}_i)}{\partial \mathbf{r}_k}$$

The first term in the force formulation is non-zero only when $$k$$ is either $$i$$ or $$j$$, thus

$$-\frac{1}{2} \frac{\partial \sum_i \sum_{j \atop j \neq i}V(r_{ij})}{\partial \mathbf{r}_k} = -\frac{1}{2} \left[\frac{\partial \sum_{j \atop j \neq k} V^j(r_{kj})}{\partial \mathbf{r}_k}+\frac{\partial \sum_{i \atop k \neq i}V^k(r_{ik})}{\partial \mathbf{r}_k}\right]$$


