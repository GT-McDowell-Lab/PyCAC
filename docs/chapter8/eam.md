## EAM potential

As mentioned [earlier](../chapter3/input.md), the EAM formulation for the potential energy is

$$E = \frac{1}{2}\sum_i\sum_{j \atop j\neq i} V_{ij}(r_{ij}) + \sum_i F(\bar{\rho}_i)$$

where $$V$$ is the pair potential, $$F$$ is the embedding potential, and $$\bar{\rho}$$ is the host electron density, i.e.,

$$\bar{\rho}_i = \sum_{j \atop j \neq i} \rho_{ij}(r_{ij})$$

where $$\rho_{ij}$$ is the local electron density contributed by atom $$j$$ at site $$i$$.

Let $$\mathbf{r}_{ji}$$ be the vector from atom $$j$$ to atom $$i$$ with norm $$r_{ji} (= r_{ij})$$, i.e.,

$$\mathbf{r}_{ji} = \mathbf{r}_i - \mathbf{r}_j$$

$$r_{ji} = \sqrt{(r_i^x - r_j^x)^2 + (r_i^y - r_j^y)^2 + (r_i^z - r_j^z)^2}$$

where

$$\mathbf{r}_j = r_j^x\mathbf{e}^x + r_j^y\mathbf{e}^y + r_j^z\mathbf{e}^z$$

Now, let's prove an important identity,

$$\frac{\partial r_{ji}}{\partial \mathbf{r}_j} = \frac{\partial r_{ji}}{\partial r_j^x} \mathbf{e}^x + \frac{\partial r_{ji}}{\partial r_j^y} \mathbf{e}^y + \frac{\partial r_{ji}}{\partial r_j^z} \mathbf{e}^z =  - \frac{r_{ji}^x}{r_{ji}} \mathbf{e}^x - \frac{r_{ji}^y}{r_{ji}} \mathbf{e}^y - \frac{r_{ji}^z}{r_{ji}} \mathbf{e}^z = -\frac{\mathbf{r}_{ji}}{r_{ji}}$$

which will be used in the force formulation derivation later.

The force on atom $$k$$ is

$$\mathbf{f}_k = -\frac{\partial E}{\partial \mathbf{r}_k} = -\frac{1}{2} \frac{\partial \sum_i \sum_{j \atop j \neq i}V_{ij}(r_{ij})}{\partial \mathbf{r}_k}-\frac{\partial \sum_i F(\bar{\rho}_i)}{\partial \mathbf{r}_k}$$

The first term in the force formulation is non-zero only when $$k$$ is either $$i$$ or $$j$$, thus it becomes

$$-\frac{1}{2} \left[\frac{\partial \sum_{j \atop j \neq k} V_{kj}(r_{kj})}{\partial \mathbf{r}_k}+\frac{\partial \sum_{i \atop k \neq i}V_{ik}(r_{ik})}{\partial \mathbf{r}_k}\right] = -\frac{1}{2} \left[\frac{\partial \sum_{j \atop j \neq k} V_{kj}(r_{kj})}{\partial r_{kj}}\frac{\partial r_{kj}}{\partial \mathbf{r}_k} - \frac{\partial \sum_{i \atop k \neq i}V_{ik}(r_{ik})}{\partial r_{ik}}\frac{\partial r_{ik}}{\partial \mathbf{r}_k}\right]$$

With the help of the identity, the term becomes

$$\frac{1}{2} \left[\frac{\partial \sum_{j \atop j \neq k} V_{kj}(r_{kj})}{\partial r_{kj}}\frac{\mathbf{r}_{kj}}{r_{kj}} - \frac{\partial \sum_{i \atop k \neq i}V_{ik}(r_{ik})}{\partial r_{ik}}\frac{\mathbf{r}_{ik}}{r_{ik}}\right]$$

where $$V_{kj}$$ and $$V_{ik}$$ are the pair potentials for the atomic pairs $$kj$$ and $$ik$$, respectively, while $$V_{kj} = V_{jk}$$ and $$V_{ik} = V_{ki}$$. Since $$V$$ is atom type-specific, $$V_{kj}$$ and $$V_{ik}$$ are likely not the same unless atom $$i$$ and $$j$$ are of the same type. Thus, if there are two types of atoms in the system, there will be three $$V$$, between type 1 and type 1, between type 2 and type 2, and between type 1 and type 2.

The second term in the force formulation can be written as

$$-\sum_i\frac{\partial F(\bar{\rho}_i)}{\partial \mathbf{r}_k} = -\sum_i\frac{\partial F(\bar{\rho}_i)}{\partial \bar{\rho}_i}\frac{\partial \bar{\rho}_i}{\partial \mathbf{r}_k} = -\sum_i\frac{\partial F(\bar{\rho}_i)}{\partial \bar{\rho}_i}\sum_{j \atop j \neq i}\frac{\partial \rho_{ij}(r_{ij})}{\partial \mathbf{r}_k} = -\sum_i\frac{\partial F(\bar{\rho}_i)}{\partial \bar{\rho}_i}\sum_{j \atop j \neq i}\frac{\partial \rho_{ij}(r_{ij})}{\partial r_{ij}}\frac{\partial r_{ij}}{\partial \mathbf{r}_k}$$

which is non-zero when $$k$$ is either $$i$$ or $$j$$, i.e., the term becomes

$$-\frac{\partial F(\bar{\rho}_k)}{\partial \bar{\rho}_k}\sum_{j \atop j \neq k}\frac{\partial \rho_{kj}(r_{kj})}{\partial r_{kj}}\frac{\partial r_{kj}}{\partial \mathbf{r}_k}-\sum_{i \atop i \neq k}\frac{\partial F(\bar{\rho}_i)}{\partial \bar{\rho}_i}\frac{\partial \rho_{ik}(r_{ik})}{\partial r_{ik}}\frac{\partial r_{ik}}{\partial \mathbf{r}_k}$$

Again, with the help of the identify, the term becomes

$$\frac{\partial F(\bar{\rho}_k)}{\partial \bar{\rho}_k}\sum_{j \atop j \neq k}\frac{\partial \rho_{kj}(r_{kj})}{\partial r_{kj}}\frac{\mathbf{r}_{kj}}{r_{kj}}-\sum_{i \atop i \neq k}\frac{\partial F(\bar{\rho}_i)}{\partial \bar{\rho}_i}\frac{\partial \rho_{ik}(r_{ik})}{\partial r_{ik}}\frac{\mathbf{r}_{ik}}{r_{ik}}$$

Note that $$\rho_{kj}$$ is the local electron density contributed by atom $$j$$ at site $$k$$. In general, $$\rho_{kj} \neq \rho_{jk}$$. This is different from the pair potential $$V$$, for which generally $$V_{kj} = V_{jk}$$. Also, generally $$\rho_{kj} \neq \rho_{ij}$$ unless atom $$k$$ and atom $$i$$ are of the same type. 

In [classical EAM](http://dx.doi.org/10.1103/PhysRevB.29.6443), $$\rho_{kj} = \rho_{ij}$$ even when atom $$k$$ and atom $$i$$ are of different type. If there are two types of atoms in the system, there are only two $$\rho$$, for the contribution from type 1 atom and for that from type 2 atom, regardless of which type of atomic site it contributes to. This is different from the pair potential $$V$$, which would have three expressions in this case. Extensions of $$\rho$$ to distinguish contributions at different types of atomic sites have been proposed, e.g., in the [Finnis-Sinclair potential](http://dx.doi.org/10.1080/01418618408244210).

Adding the two terms in the force formulation together yields

$$\mathbf{f}_k = \frac{1}{2} \left[\frac{\partial \sum_{j \atop j \neq k} V_{kj}(r_{kj})}{\partial r_{kj}}\frac{\mathbf{r}_{kj}}{r_{kj}}-\frac{\partial \sum_{i \atop k \neq i}V_{ik}(r_{ik})}{\partial r_{ik}}\frac{\mathbf{r}_{ik}}{r_{ik}}\right] + \frac{\partial F(\bar{\rho}_k)}{\partial \bar{\rho}_k}\sum_{j \atop j \neq k}\frac{\partial \rho_{kj}(r_{kj})}{\partial r_{kj}}\frac{\mathbf{r}_{kj}}{r_{kj}}-\sum_{i \atop i \neq k}\frac{\partial F(\bar{\rho}_i)}{\partial \bar{\rho}_i}\frac{\partial \rho_{ik}(r_{ik})}{\partial r_{ik}}\frac{\mathbf{r}_{ik}}{r_{ik}}$$

Since $$i$$ and $$j$$ are just dummy indices, it is safe to replace all $$i$$ with $$j$$. After that, with $$\mathbf{r}_{jk} = -\mathbf{r}_{kj}$$, $$r_{jk} = r_{kj}$$, $$V_{jk} = V_{kj}$$, and $$\rho_{jk} \neq \rho_{kj}$$, the force on atom $$k$$ becomes

$$\mathbf{f}_k = \sum_{j \atop j \neq k}\left[\frac{\partial V_{kj}(r_{kj})}{\partial r_{kj}}+\frac{\partial F(\bar{\rho}_k)}{\partial \bar{\rho}_k}\frac{\partial \rho_{kj}(r_{kj})}{\partial r_{kj}}+\frac{\partial F(\bar{\rho}_j)}{\partial \bar{\rho}_j}\frac{\partial \rho_{jk}(r_{kj})}{\partial r_{kj}}\right]\frac{\mathbf{r}_{kj}}{r_{kj}}$$

If there is only type of atoms in the system, $$\rho_{jk} = \rho_{kj}$$, and the force formulation is simplified to

$$\mathbf{f}_k = \sum_{j \atop j \neq k}\left[\frac{\partial V_{kj}(r_{kj})}{\partial r_{kj}}+\left(\frac{\partial F(\bar{\rho}_k)}{\partial \bar{\rho}_k}+\frac{\partial F(\bar{\rho}_j)}{\partial \bar{\rho}_j}\right)\frac{\partial \rho_{kj}(r_{kj})}{\partial r_{kj}}\right]\frac{\mathbf{r}_{kj}}{r_{kj}}$$

which is Equation 15 of [Xu et al.](http://dx.doi.org/10.1016/j.ijplas.2015.05.007) Note that the last two equations hold for both [classical EAM](http://dx.doi.org/10.1103/PhysRevB.29.6443) and [Finnis-Sinclair](http://dx.doi.org/10.1080/01418618408244210) potentials, because the relation between $$\rho_{kj}$$ and $$\rho_{ij}$$ is not used during the derivation.