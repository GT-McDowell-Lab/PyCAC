## lattice periodicity length

The length of periodicity of the lattice is the minimum distance at which the lattice repeats itself. For example, the lattice constant $$a_0$$ in cubic crystal systems is the lattice periodicity length along the $$\left<100\right>$$ directions.

Once the crystallographic orientations are set, e.g., the $$x$$ axis in the first grain has an orientation of $$[abc]$$, the lattice will repeat itself at every $$\sqrt{a^2 + b^2 + c^2}a_0$$ distant along the $$x$$ direction. However, this distant may not be the smallest lattice periodicity length. For example, when $$[abc] = [112]$$, $$\sqrt{a^2 + b^2 + c^2}a_0 = \sqrt{6}a_0$$, yet the smallest lattice periodicity length $$l_0 = (\sqrt{6}/2)a_0$$.

So how is $$l_0$$ calculated for any given $$[abc]$$? First, one calculates $$l = a^2 + b^2 + c^2$$. Second, one divides $$l$$ by 2, then by 2 again, and so on, until the result is not divisable by 2. For example, if $$l = 24$$, one gets $$24/2 = 12$$, then $$12/2 = 6$$, then $$6/2 = 3$$, then $$3$$ is not divisible by 2. During this process, $$l$$ and its quotients are divided by 2 for 3 times, then one get an integer $$\Delta = 3$$. Finally, $$l_0 = (\sqrt{l}/\Delta)a_0$$. Repeating this process for the remaining orientations results in the lattice periodicity length vector $$\vec{l}_0$$.

Since each grain has its own crystallographic orientations, each grain has its own $$\vec{l}_0$$. The length vector along each direction that is the largest in magnitude among all grains is the lattice periodicity length for the simulation cell, $$\vec{l'}_0$$. The largest component in the $$\vec{l'}_0$$ vector is the maximum lattice periodicity length for the simulation cell, $$l'_\mathrm{max}$$.

$$\vec{l'}_0$$ and $$l'_\mathrm{max}$$ are the length units in four [commands](../chapter5/README.md): [fix](../chapter5/fix.md), [grain_dir](../chapter5/grain_dir.md), [group](../chapter5/group.md), and [modify](../chapter5/modify.md). A question usually arises regarding how the lengths in these four commands are usually determined. For example, to build a stationary [edge dislocation](../chapter7/example1/dislocation.md), one needs to determine the position of the dislocation, i.e., using the `modify_centroid_x`, `modify_centroid_y`, and `modify_centroid_z` variables in the [modify](../chapter5/modify.md) command. In the <a href="../chapter7/example1/edge.in" target="_blank">input file</a>, there is one line

	modify modify_1 dislocation 1 3 13. 39. 17.333 90. 0.33

in which `plane_axis` = _3_ means that the slip plane is normal to the _z_ direction. As a result, the `modify_centroid_z` decides the _z_-coordinate of the intersection between the slip plane and the _z_ axis. Since there is only one dislocation, one usually wants to let the slip plane be within the mid-_z_ plane, but how is the value of `modify_centroid_z`, which equals _17.333_ here, determined?

In the <a href="../chapter7/example1/edge.log" target="_blank">log file</a>, there are four lines:

	The boundaries of grain 1 prior to modification are (Angstrom)
	x from  -0.639047753497337 to 132.282884973949876 length is 132.921932727447228
	y from -35.788576073151468 to  88.180085128608013 length is 123.968661201759488
	z from  -1.043560611560248 to  97.051130224507631 length is  98.094690836067883

where the last number `98.094690836067883` is the edge length of the simulation cell along the _z_ direction, prior to modification. Note that it is important to use the edge lengths of the grain `prior to modification` instead of those under `The box boundaries/lengths are (Angstrom)` because the former are used to build dislocations in the code. Another two lines in the log file are

	The lattice_space_max are
	x  2.556191013989356 y  4.427452710080598 z  6.261363669361488

where the last number `6.261363669361488` is the maximum lattice periodicity length for the simulation cell along the _z_ direction, $$l'_\mathrm{max}$$, which is indeed the length unit of `modify_centroid_z`. Thus, if one wants to let the slip plane be within the mid-_z_ plane, the value of `modify_centroid_z` is

	modify_centroid_z = 98.094690836067883 / 6.261363669361488 / 2 = 17.333