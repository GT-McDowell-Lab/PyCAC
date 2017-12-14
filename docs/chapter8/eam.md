## EAM potential

As mentioned [earlier](../chapter3/input.md), the EAM formulation for the potential energy is

$$E = \frac{1}{2}\sum_i\sum_{j \atop j\neq i} V_{ij}(r_{ij}) + \sum_i F(\bar{\rho}_i)$$

where $$V$$ is the pair potential, $$F$$ is the embedding potential, and $$\bar{\rho}$$ is the host electron density, i.e.,

$$\bar{\rho}_i = \sum_{j \atop j \neq i} \rho_{ij}(r_{ij})$$

where $$\rho$$ is the local electron density. Also, we let $$\mathbf{r}_{kj}$$ be the vector from atom $$k$$ to atom $$j$$ with norm $$r_{kj}$$, i.e.,

$$\mathbf{r}_{kj} = \mathbf{r}_j - \mathbf{r}_k$$

The force on atom $$k$$ is

$$\mathbf{f}_k = -\frac{\partial E}{\partial \mathbf{r}_k} = -\frac{1}{2} \frac{\partial \sum_i \sum_{j \atop j \neq i}V_{ij}(r_{ij})}{\partial \mathbf{r}_k}-\frac{\partial \sum_i F(\bar{\rho}_i)}{\partial \mathbf{r}_k}$$

The first term in the force formulation is non-zero only when $$k$$ is either $$i$$ or $$j$$, thus

$$-\frac{1}{2} \frac{\partial \sum_i \sum_{j \atop j \neq i}V_{ij}(r_{ij})}{\partial \mathbf{r}_k} = -\frac{1}{2} \left[\frac{\partial \sum_{j \atop j \neq k} V_{kj}(r_{kj})}{\partial \mathbf{r}_k}+\frac{\partial \sum_{i \atop k \neq i}V_{ik}(r_{ik})}{\partial \mathbf{r}_k}\right] = \frac{1}{2} \left[\frac{\partial \sum_{j \atop j \neq k} V_{kj}(r_{kj})}{\partial r_{kj}}\frac{\mathbf{r}_{kj}}{r_{kj}} - \frac{\partial \sum_{i \atop k \neq i}V_{ik}(r_{ik})}{\partial r_{ik}}\frac{\mathbf{r}_{ik}}{r_{ik}}\right]$$

where $$V_{kj}$$ and $$V_{ik}$$ are the pair potentials for the atomic pairs $$kj$$ and $$ik$$, respectively. Since $$V$$ is atom type-specific, $$V_{kj}$$ and $$V_{ik}$$ are likely not the same unless atom $$i$$ and $$j$$ are of the same type. Thus, if there are two types of atoms in the system, there will be three $$V$$, between type 1 and type 1, between type 2 and type 2, and between type 1 and type 2.

The second term in the force formulation can be written as

$$-\frac{\partial \sum_i F(\bar{\rho}_i)}{\partial \mathbf{r}_k} = -\sum_i\frac{\partial F(\bar{\rho}_i)}{\partial \mathbf{r}_k} = -\sum_i\frac{\partial F(\bar{\rho}_i)}{\partial \bar{\rho}_i}\frac{\partial \bar{\rho}_i}{\partial \mathbf{r}_k} = -\sum_i\frac{\partial F(\bar{\rho}_i)}{\partial \bar{\rho}_i}\sum_{j \atop j \neq i}\frac{\partial \rho_{ij}(r_{ij})}{\partial \mathbf{r}_k}$$

which is non-zero when $$k$$ is either $$i$$ or $$j$$, i.e., the term becomes

$$-\frac{\partial F(\bar{\rho}_k)}{\partial \bar{\rho}_k}\sum_{j \atop j \neq k}\frac{\partial \rho_{kj}(r_{kj})}{\partial \mathbf{r}_k}-\sum_{i \atop i \neq k}\frac{\partial F(\bar{\rho}_i)}{\partial \bar{\rho}_i}\frac{\partial \rho_{ik}(r_{ik})}{\partial \mathbf{r}_k} = \frac{\partial F(\bar{\rho}_k)}{\partial \bar{\rho}_k}\sum_{j \atop j \neq k}\frac{\partial \rho_{kj}(r_{kj})}{\partial r_{kj}}\frac{\mathbf{r}_{kj}}{r_{kj}}-\sum_{i \atop i \neq k}\frac{\partial F(\bar{\rho}_i)}{\partial \bar{\rho}_i}\frac{\partial \rho_{ik}(r_{ik})}{\partial r_{ik}}\frac{\mathbf{r}_{ik}}{r_{ik}}$$

Note that in [classical EAM](http://dx.doi.org/10.1103/PhysRevB.29.6443), $$\rho_{kj}$$ and $$\rho_{ik}$$ are local electron densities for the types of atom $$k$$ and atom $$i$$, respectively. Unlike the pair potential $$V$$, there is no particular $$\rho$$ for an atomic pair $$ij$$ where $$i$$ and $$j$$ are different types of atoms. If there are two types of atoms in the system, there are only two $$\rho$$, between type 1 and type 1, and between type 2 and type 2, without the one between type 1 and type 2. Extensions of $$\rho$$ to cover type 1 and type 2 have been proposed, e.g., in the [Finnis-Sinclair potential](http://dx.doi.org/10.1080/01418618408244210).

Adding the two terms in the force formulation together yields

$$\mathbf{f}_k = \frac{1}{2} \left[\frac{\partial \sum_{j \atop j \neq k} V_{kj}(r_{kj})}{\partial r_{kj}}\frac{\mathbf{r}_{kj}}{r_{kj}}-\frac{\partial \sum_{i \atop k \neq i}V_{ik}(r_{ik})}{\partial r_{ik}}\frac{\mathbf{r}_{ik}}{r_{ik}}\right] + \frac{\partial F(\bar{\rho}_k)}{\partial \bar{\rho}_k}\sum_{j \atop j \neq k}\frac{\partial \rho_{kj}(r_{kj})}{\partial r_{kj}}\frac{\mathbf{r}_{kj}}{r_{kj}}-\sum_{i \atop i \neq k}\frac{\partial F(\bar{\rho}_i)}{\partial \bar{\rho}_i}\frac{\partial \rho_{ik}(r_{ik})}{\partial r_{ik}}\frac{\mathbf{r}_{ik}}{r_{ik}}$$

Since $$i$$ and $$j$$ are just dummy indices, also note that $$\mathbf{r}_{ij} = -\mathbf{r}_{ji}$$, $$r_{ij} = r_{ji}$$, $$V_{ij} = V_{ji}$$, and $$\rho_{ij} \neq \rho_{ji}$$, the force on atom $$k$$ becomes

$$\mathbf{f}_k = \sum_{j \atop j \neq k}\left[\frac{\partial V_{kj}(r_{kj})}{\partial r_{kj}}+\frac{\partial F(\bar{\rho}_k)}{\partial \bar{\rho}_k}\frac{\partial \rho_{kj}(r_{kj})}{\partial r_{kj}}+\frac{\partial F(\bar{\rho}_j)}{\partial \bar{\rho}_j}\frac{\partial \rho_{jk}(r_{kj})}{\partial r_{kj}}\right]\frac{\mathbf{r}_{kj}}{r_{kj}}$$

If there is only type of atoms in the system, $$\rho_{ij} = \rho_{ji}$$, and the force formulation is simplified to

$$\mathbf{f}_k = \sum_{j \atop j \neq k}\left[\frac{\partial V_{kj}(r_{kj})}{\partial r_{kj}}+\left(\frac{\partial F(\bar{\rho}_k)}{\partial \bar{\rho}_k}+\frac{\partial F(\bar{\rho}_j)}{\partial \bar{\rho}_j}\right)\frac{\partial \rho_{kj}(r_{kj})}{\partial r_{kj}}\right]\frac{\mathbf{r}_{kj}}{r_{kj}}$$

which is Equation 15 of [Xu et al.](http://dx.doi.org/10.1016/j.ijplas.2015.05.007).