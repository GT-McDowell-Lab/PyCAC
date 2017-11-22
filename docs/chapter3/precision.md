## Arithmetic precision

To ensure the [processor-independent precision](http://fortranwiki.org/fortran/show/Real+precision), the working precision (`wp`) is defined in the `precision_comm_module.f90` [module file](../chapter1/comp-and-exec.md).

The default precision is 64-bit real, the users can opt for 128-bit real by modifying `wp`.

The default size used for an integer is KIND = 4, meaning that any integer may have a signed value ranging from -2,147,483,648 to 2,147,483,647. In PyCAC, the maximum integer is usually the number of atoms (both the real atoms in the atomistic domain and the interpolated atoms in the coarse-grained domain). In the case that each element contains 2197 atoms, this limit suggests that there cannot be more than 977,461 elements in a fully coarse-grained simulation cell. If the user wants to study larger simulation cells, he/she needs to modify the source code.