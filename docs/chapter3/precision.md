## Arithmetic precision

To ensure the [processor-independent precision](http://fortranwiki.org/fortran/show/Real+precision), the working precision (`wp`) is defined in the `precision_comm_module.f90` [module file](module.md).

The default precision is 64-bit reals, the users can opt for 128-bit reals by modifying `wp`.