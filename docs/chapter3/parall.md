## Parallelization

Among the three parallel algorithms commonly employed in atomistic simulations — atom decomposition (AD), force decomposition (FD), and spatial decomposition (SD), SD yields the best scalability and the smallest communication overhead between processors. Unlike AD and FD, the workload of each processor in SD, which is proportional to the number of interactions, is unfortunately not guaranteed to be the same. In CAC, the simulation cell has nonuniformly distributed integration points (in the coarse-grained domain) and atoms (in the atomistic domain), such that the workload is poorly balanced if one assigns each processor an equally-sized cubic domain as in full atomistics. This workload balance issue is not unique to CAC, but is also encountered by other concurrent multiscale modeling methods.

The PyCAC code employs the SD algorithm in which the load balance is optimized, as shown in the figure below which is adapted from Xu et al.

<figure><img src='fig/parallel.jpg'><figcaption>Parallel CAC simulation scheme. Procedures that do not exist in the [serial CAC simulation scheme](scheme.md) are
highlighted in yellow. Note that (i) in the serial scheme, the root processor does everything and (ii) the two procedures in the dashed box are conducted back and forth until the output begins.</figcaption></figure> 
<br>
For more information, read chapter 3 of [Shuozhi Xu's Ph.D. dissertation](https://smartech.gatech.edu/handle/1853/56314).