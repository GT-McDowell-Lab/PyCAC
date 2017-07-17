## rank

In MPI, rank is a logical way of numbering processors. The processor 1 has rank 0, the processor 2 has rank 1, and so on. In the PyCAC code, the integer `root` is set to 0 in `processor_para_module.f90`. The processor 1, i.e., `root`, does heavy lifting 