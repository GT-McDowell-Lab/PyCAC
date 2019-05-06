## lattice periodicity length

The length of periodicity of the lattice is the minimum distance at which the lattice repeats itself. For example, the lattice constant $$a_0$$ in cubic crystal systems is the lattice periodicity length along the $$\left<100\right>$$ directions.

Once the crystallographic orientations are set, e.g., the $$x$$ axis in the first grain has an orientation of $$[abc]$$, the lattice will repeat itself at every $$\sqrt{a^2 + b^2 + c^2}a_0$$ distance along the $$x$$ direction. In the simple cubic system, this distance is likely the smallest lattice periodicity length. But in the face-centered cubic (FCC) and body-centered cubic (BCC) systems, this may not be the case. For example, in FCC, when $$[abc] = [112]$$, $$\sqrt{a^2 + b^2 + c^2}a_0 = \sqrt{6}a_0$$, yet the smallest lattice periodicity length $$l_0 = (\sqrt{6}/2)a_0$$. Another example is in BCC, when $$[abc] = [111]$$, $$\sqrt{a^2 + b^2 + c^2}a_0 = \sqrt{3}a_0$$, yet $$l_0 = (\sqrt{3}/2)a_0$$.

Since each grain has its own crystallographic orientations, each grain has its own $$\vec{l}_0$$. The length vector along each direction that is the largest in magnitude among all grains is the lattice periodicity length for the simulation cell, $$\vec{l'}_0$$. The largest component in the $$\vec{l'}_0$$ vector is the maximum lattice periodicity length for the simulation cell, $$l'_\mathrm{max}$$.

$$\vec{l'}_0$$ and $$l'_\mathrm{max}$$ are the length units in four [commands](../chapter5/README.md): [fix](../chapter5/fix.md), [grain_dir](../chapter5/grain_dir.md), [group](../chapter5/group.md), and [modify](../chapter5/modify.md). A question arises regarding how the lengths in these four commands are usually determined. For example, to build a [stationary edge dislocation](../chapter7/example1/dislocation.md), one needs to determine the position of the dislocation, i.e., using the `modify_centroid_x`, `modify_centroid_y`, and `modify_centroid_z` variables in the [modify](../chapter5/modify.md) command. In the <a href="../chapter7/example1/edge.in" target="_blank">input file</a>, there is one line

	modify modify_1 dislocation 1 3 13. 39. 17.333 90. 0.33

in which `plane_axis` = _3_ means that the slip plane is normal to the _z_ direction. As a result, the `modify_centroid_z` decides the _z_-coordinate of the intersection between the slip plane and the _z_ axis. Since there is only one dislocation, one usually wants to let the slip plane be within the mid-_z_ plane, but how is the value of `modify_centroid_z`, which equals _17.333_ here, determined?

In the <a href="../chapter7/example1/edge.log" target="_blank">log file</a>, there are four lines:

	The boundaries of grain 1 prior to modification are (Angstrom)
	x from  -0.413351394094665 to 128.552283563439630 length is 128.965634957534292
	y from  -0.715945615951370 to 222.659086560878961 length is 223.375032176830331
	z from -29.228357377724798 to 213.951576004945480 length is 243.179933382670271

where the last number `243.179933382670271` is the edge length of the simulation cell along the _z_ direction, prior to modification. Note that it is important to use the edge lengths of the grain `prior to modification` instead of those under `The box boundaries/lengths are (Angstrom)` because the former are used to build dislocations in the code. Another two lines in the log file are

	The lattice_space_max are
	x  4.960216729135929 y  2.863782463805506 z  7.014805770653949

where the last number `7.014805770653949` is the maximum lattice periodicity length for the simulation cell along the _z_ direction, $$l'_\mathrm{max}$$, which is indeed the length unit of `modify_centroid_z`. Thus, if one wants to let the slip plane be within the mid-_z_ plane, the value of `modify_centroid_z` is

	243.179933382670271 / 7.014805770653949 / 2 = 17.333