# Algorithm

Due to the similarity between CAC and atomistic simulations regarding lattice structure and force/energy calculations, the CAC algorithm adopts common atomistic techniques. Newton's third law is employed in the atomistic domain to promote efficiency in calculating the force, pair potential, local electron density, and stress. The short-range neighbor search adopts a combined Verlet list and link-cell methods. There are, however, two major issues regarding the imposition of periodic boundary conditions (PBCs) in CAC simulations with coarse-graining that do not exist in standard atomistic simulations.

For more information, read chapter 3 of [Shuozhi Xu's Ph.D. dissertation](https://smartech.gatech.edu/handle/1853/56314).