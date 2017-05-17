## Module

In PyCAC, global variables are defined by 54 module files `*_module.f90` in the `module` directory. There are five types of module files:

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

Note that these module files should be compiled in this order in creating the static library `libcac.a`. Otherwise, an error may be reported.


