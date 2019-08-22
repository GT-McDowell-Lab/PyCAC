# Algorithm

A framework for mixed atomistic/continuum modeling, the CAC algorithm adopts common atomistic modeling and finite element techniques. In the atomistic domain, Newton’s third law is employed to promote efficiency in calculating the force, pair potential, local electron density, and stress. The short-range neighbor search employs a combined cell list and Verlet list method. In the coarse-grained domain, the Garlekin method and Gaussian quadrature are employed to solve the [governing equations](../chapter-2/atomistic-field-theory.md).

There are, however, several issues in CAC simulations with coarse-graining that do not exist in standard atomistic and finite element method simulations.

For more information, read chapter 3 of [Shuozhi Xu's Ph.D. dissertation](https://smartech.gatech.edu/handle/1853/56314).