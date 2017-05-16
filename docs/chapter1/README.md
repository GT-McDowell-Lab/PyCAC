# Introduction

The concurrent atomistic-continuum \(CAC\) method is a partitioned-domain multiscale modeling technique that is applicable to nano/micron scale thermo/mechanical problems in a wide range of monoatomic and polyatomic crystalline materials. A CAC simulation model, in general, partitions the simulation cell into two domains: atomistic and coarse-grained domains. Differing from most concurrent multiscale methods in the literature, CAC employs a unified atomistic-continuum integral formulation with elements that have discontinuities between them and the underlying interatomic potential as the only constitutive relation in the system. As such, CAC admits propagation of displacement discontinuities (dislocations and associated intrinsic stacking faults) through a lattice in both atomistic and coarse-grained domains.

Differing from most concurrent multiscale materials modeling methods in the literature, CAC

* describes certain lattice defects and their interactions using fully resolved atomistics;
* preserves the net Burgers vector and associated long range stress fields of curved, mixed character dislocations in a sufficiently large continuum domain in a fully 3D model;
* employs the same governing equations and interatomic potentials in both domains to avoid the usage of phenomenological parameters, essential remeshing operations and _ad hoc_ procedures for passing dislocation segments between atomistic and coarse-grained atomistic domains.