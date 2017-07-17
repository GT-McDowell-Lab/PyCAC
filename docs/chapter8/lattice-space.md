## lattice periodicity length

The length of periodicity of the lattice, i.e., the minimum distance at which the lattice repeats itself. For example, the lattice constant $$a_0$$ in cubic crystal systems, is the lattice periodicity length along the $$\left<100\right>$$ directions.

Once the crystallographic orientations are set, e.g., the $$x$$ axis in the first grain has an orientation of $$[abc]$$, the lattice will repeat itself at every $$\sqrt{a^2 + b^2 + c^2}a_0$$ distant along the $$x$$ direction. However, this distant may not be the smallest lattice periodicity length. For example, when $$[abc] = [112]$$, $$\sqrt{a^2 + b^2 + c^2}a_0 = \sqrt{6}a_0$$, yet the smallest lattice periodicity length $$l_0 = (\sqrt{6}/2)a_0$$.

So how is $$l_0$$ calculated for any given $$[abc]$$? First, one calculates $$l = a^2 + b^2 + c^2$$. Second, one divides $$l$$ by 2, then by 2 again, and so on, until the result is not divisable by 2. For example, if $$l = 24$$, one gets $$24/2 = 12$$, then $$12/2 = 6$$, then $$6/2 = 3$$, then $$3$$ is not divisible by 2. During this process, $$l$$ and its quotients are divided by 2 for 3 times, then one get an integer $$\Delta = 3$$. Finally, $$l_0 = (sqrt{l}/\Delta)a_0$$.

is the distant unit in some [`cac.in` commands](../chapter5/README.md), including [bd_group](../chapter5/bd_group.md), [grain_dir](../chapter5/grain_dir.md), [group](../chapter5/group.md), and [modify](../chapter5/modify.md).

	