## PyCAC features and non-features

The PyCAC code can simulate thermo/mechanical problems in pure face-centered cubic (FCC) and body-centered cubic (BCC) metals using the Lennard-Jones (LJ) and embedded-atom method (EAM) potentials. In the coarse-grained domain, rhombohedral elements are employed to accommondate 9 out of 12 sets of $$\{111\}\left<110\right>$$ slip systems in an FCC lattice, as well as 6 of 12 sets of $$\{110\}\left<111\right>$$ slip systems in a BCC lattice.

While the CAC method is applicable to thermo/mechanical problems in almost all crystalline materials, the current PyCAC code cannot simulate:

* 12 sets of $$\{112\}\left<111\right>$$ and 24 sets
of $$\{123\}\left<111\right>$$ slip systems in a BCC lattice;
* 

