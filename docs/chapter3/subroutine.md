## Subroutine

In PyCAC, there are one main program (`main.f90`) and 173 subroutines (`*.f90`) in the `src` directory. Error messages are issued when

	call mpi_abort(mpi_comm_world, 1, ierr)

is triggered; the program is stopped immediately.