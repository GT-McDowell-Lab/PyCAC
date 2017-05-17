## PyCAC features and non-features

The PyCAC code can simulate thermo/mechanical problems in pure face-centered cubic (FCC) and body-centered cubic (BCC) metals using the Lennard-Jones (LJ) and embedded-atom method (EAM) potentials. In the coarse-grained domain, rhombohedral elements are employed to accommondate dislocations in 9 out of 12 sets of $$\{111\}\left<110\right>$$ slip systems in an FCC lattice, as well as 6 out of 12 sets of $$\{110\}\left<111\right>$$ slip systems in a BCC lattice.

While the CAC method is applicable to thermo/mechanical problems in almost all crystalline materials, the current PyCAC code cannot simulate:

* dislocations in 12 sets of $$\{112\}\left<111\right>$$-type and 24 sets of $$\{123\}\left<111\right>$$-type slip systems in a BCC lattice;
* crystal structures other than FCC and BCC, e.g., simple cubic, diamond cubic, hexagonal close-packed;
* interatomic potentials other than LJ and EAM, e.g., Stillinger-Weber potential, Tersoff potential, modified EAM (MEAM) potential;
* multicomponent or multiphase materials, e.g., alloys, intermetallics;
* polyatomic crystalline materials, i.e., ceramic, mineral;
* adaptive mesh refinement.