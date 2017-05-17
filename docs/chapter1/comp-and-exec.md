## Compilation and execution

The PyCAC code is fully parallelized with Message Passing Interface (MPI). Some functions in MPI-3 standard is provided. It works with [Open MPI](https://www.open-mpi.org) version 2.1, [Intel MPI](https://software.intel.com/en-us/intel-mpi-library) version 5.1, [MPICH](https://www.mpich.org) version 3.3, and [MVAPICH2](http://mvapich.cse.ohio-state.edu) version 2.3.

Some intrinsic functions in Fortran 2003 is employed in the code, so compilers that fully support Fortran 2013 are preferred. For example, [GNU Fortran](https://gcc.gnu.org/fortran) version 7.0 and [Intel Fortran](https://software.intel.com/en-us/fortran-compilers) version 17.0 work with the PyCAC code.

In compilation, the first step is to create a static library `libcac.a` from [module files](../chapter3/module.md). Then, an executale, named `CAC`, is compiled using the [main/subroutine files](../chapter3/subroutine.md) and linked with the static library. Please read `install.sh` for more details.

In execution, the executable `CAC`, the input file `cac.in`, and the [potential files](../chapter3/io.md) are moved into the same directory. It follows that

	mpirun -np num_of_proc ./CAC < cac.in
	
where `num_of_proc` is the number of processors to be used.

The users may run the PyCAC code on the [MATerials Innovation Network (MATIN)](https://matin.gatech.edu) at Georgia Tech when it is ready.
