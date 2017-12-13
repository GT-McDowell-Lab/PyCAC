## EAM potential

As mentioned [earlier](../chapter3/input.md) The EAM formulation for the potential energy is

$$E = \frac{1}{2}\sum_i\sum_{j\neq i} V(r^{ij}) + \sum_i F(\bar{\rho}^i)$$

where $$V$$ is the pair potential, $$F$$ is the embedding potential, and $$\bar{\rho}$$ is the host electron density, i.e.,

$$\bar{\rho}^i = \sum_{i \neq j} \rho^{ij}(r^{ij})$$

where $$\rho$$ is the local electron density.

The force is

$$\mathbf{f}_k = -\frac{\partial E}{\partial \mathbf{r}_k} = -\frac{1}{2} \frac{\partial \sum_i \sum_{j \atop j \neq i}V(r_{ij})}{\partial \mathbf{r}_k}-\frac{\partial \sum_i F(\bar{\rho}_i)}{\partial \mathbf{r}_k}$$

The first term in the force formulation is non-zero only when $$k$$ is either $$i$$ or $$j$$, thus

$$-\frac{1}{2} \frac{\partial \sum_i \sum_{j \atop j \neq i}V(r_{ij})}{\partial \mathbf{r}_k} = -\frac{1}{2} \left[\frac{\partial \sum_{j \atop j \neq k} V^{kj}(r_{kj})}{\partial \mathbf{r}_k}+\frac{\partial \sum_{i \atop k \neq i}V^{ik}(r_{ik})}{\partial \mathbf{r}_k}\right]$$

where $$V^{kj}$$ and $$V^{ik}$$ are the pair potentials for the atomic pairs $$kj$$ and $$ik$$, respectively. When the system contains more than one types of atoms, the two pair potentials $$V$$ are not necessarily the same. On the other hand, when the system contains only one type of atoms, $$i$$ and $$j$$ are just dummy indices, so the first term in the force formulation becomes

$$-\sum_{i \atop i \neq k}\frac{\partial V(r_{ik})}{\partial \mathbf{r}_k}$$

The second term in the force formulation can be written as

$$-\sum_i\frac{\partial F(\bar{\rho}_i)}{\partial \mathbf{r}_k} = -\sum_i\frac{\partial F(\bar{\rho}_i)}{\partial \bar{\rho}_i}\frac{\partial \bar{\rho}_i}{\partial \mathbf{r}_k} = -\sum_i\frac{\partial F(\bar{\rho}_i)}{\partial \bar{\rho}_i}\sum_{j \atop j \neq i}\frac{\partial \rho_{ij}(r_{ij})}{\partial \mathbf{r}_k}$$

which is non-zero when $$k$$ is either $$i$$ or $$j$$, i.e.,

$$-\sum_i\frac{\partial F(\bar{\rho}_i)}{\partial \bar{\rho}_i}\sum_{j \atop j \neq i}\frac{\partial \rho_{ij}(r_{ij})}{\partial \mathbf{r}_k} = -\frac{\partial F(\bar{\rho}_k)}{\partial \bar{\rho}_k}\sum_{j \atop j \neq k}\frac{\partial \rho_{kj}(r_{kj})}{\partial \mathbf{r}_k}-\sum_{i \atop i \neq k}\frac{\partial F(\bar{\rho}_i)}{\partial \bar{\rho}_i}\frac{\partial \rho_{ik}(r_{ik})}{\partial \mathbf{r}_k}$$

Again, when the system contains more than one types of atoms, the two local electron densities $$\rho$$ are not necessarily the same. On the other hand, when the system contains only one type of atoms, $$i$$ and $$j$$ are just dummy indices, so the second term in the force formulation becomes

$$-\sum_{i \atop i \neq k}\left(\frac{\partial F(\bar{\rho}_k)}{\partial \bar{\rho}_k}+\frac{\partial F(\bar{\rho}_i)}{\partial \bar{\rho}_i}\right)\frac{\partial \rho_{ik}(r_{ik})}{\partial \bvec{r}_k}$$