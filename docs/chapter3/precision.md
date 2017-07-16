## Arithmetic precision

To ensure the [processor-independent precision](http://fortranwiki.org/fortran/show/Real+precision), the working precision (`wp`) is defined in the `precision_comm_module.f90` [module file](../chapter1/comp-and-exec.md).

The default precision is 64-bit real, the users can opt for 128-bit real by modifying `wp`.