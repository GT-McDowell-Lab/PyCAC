## Compilation and execution

### MPI

The PyCAC code is fully parallelized with Message Passing Interface (MPI). Some functions in MPI-3 standard is provided. It works with [Open MPI](https://www.open-mpi.org) version 2.1, [Intel MPI](https://software.intel.com/en-us/intel-mpi-library) version 5.1, [MPICH](https://www.mpich.org) version 3.3, and [MVAPICH2](http://mvapich.cse.ohio-state.edu) version 2.3.

### Compiler

Some intrinsic functions in Fortran 2003 is employed in the code, so compilers that fully support Fortran 2013 are preferred. For example, [GNU Fortran](https://gcc.gnu.org/fortran) version 7.0 and [Intel Fortran](https://software.intel.com/en-us/fortran-compilers) version 17.0 work with the PyCAC code.

### Module

In compilation, the first step is to create a static library `libcac.a` from the 54 module files `*_module.f90` in the `module` directory. There are five types of module files:

	*_comm_module.f90

There is only one `*_comm_module.f90` file: `precision_comm_module.f90`. It controls the [precision](precision.md) of integer and real numbers.

	*_para_module.f90
	
There are 24 `*_para_module.f90` files. They define single value variables that can be used globally.

	*_array_module.f90

There are 23 `*_array_module.f90` files. They define arrays that can be used globally. With a few exceptions, the `*_para_module.f90` and `*_array_module.f90` files come in pairs.

	*_function_module.f90

There are 5 `*_function_module.f90` files. They define interatomic potential formulations, arithmetic/linear algerala calculations, unit conversion, etc.

	*_tab_module.f90

There is only one `	*_tab_module.f90` file: `eam_tab_module.f90`. It contains algorithms that extract EAM potential-based values from numerical tables. 

Note that these module files should be compiled in this order, e.g., see the `install.sh` file, in creating the static library `libcac.a`. Otherwise, an error may be reported.

### Subroutine

Then, an executale, named `CAC`, is compiled using one main program (`main.f90`) plus 173 subroutines (`*.f90`) in the `src` directory and linked with the static library.

In execution, the executable `CAC`, the input file [`cac.in`](../chapter5/README.md), and the [potential files](../chapter3/input.md) are moved into the same directory. It follows that

	mpirun -np num_of_proc ./CAC < cac.in
	
where `num_of_proc` is the number of processors to be used.

The users may run the PyCAC code on the [MATerials Innovation Network (MATIN)](https://matin.gatech.edu) at Georgia Tech when it is ready.
