# Results download

Start the main GUI application
```
$ python -m pycac -j
```
Select *Download Project Results* and proceed to the next panel. Choose the desired download location for project results. 
Choose one or more *Project Name(s)* to download. Note that only jobs submitted through PyCAC will appear in the dropdown options; however one can specify a known cluster directory by selecting *Other*

###VTK to dump conversion
To save space on the cluster, the CAC simulator only produces VTK files. One can elect to convert these VTK to [LAMMPS-style dump files](http://lammps.sandia.gov/doc/dump.html) that can be visualized by atomistic model viewers and/or [read by LAMMPS](http://lammps.sandia.gov/doc/read_dump.html) directly to carry out equivalent fully-resolved atomistic simulations. By default, the convertor will use the VTK file boundaries, but custom boundaries can be defined. Please see the [fortran convertor](../chapter6/analyzer.md) if built-in conversion fails.