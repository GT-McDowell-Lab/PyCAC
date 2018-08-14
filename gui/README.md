## PyCAC

PyCAC, the concurrent atomistic-continuum (CAC) simulation environment, is a software suite that allows users to run CAC simulations and analyze data. It comprises a Python GUI for interaction with and creation of CAC simulation projects, and the CAC simulator itself.

It is developed by the group of [Prof. David L. McDowell ](http://www.me.gatech.edu/faculty/mcdowell) at the Georgia Institute of Technology, in collaboration with the group of [Prof. Youping Chen](http://web.mae.ufl.edu/chenlab/) at the University of Florida and the group of [Prof. Liming Xiong](http://www.aere.iastate.edu/lmxiong/) at the Iowa State University. The code development was sponsored by

* National Science Foundation
	- Georgia Institute of Technology, CMMI-1232878
	- University of Florida, CMMI-1233113
	- Iowa State University, CMMI-1536925
* Department of Energy, Office of Basic Energy Sciences
	- University of Florida, DE-SC0006539

### Installation/Configuration
The source code may be obtained from [GitHub](https://github.com/GT-McDowell-Lab/PyCAC/tree/master/gui) or [PyPi](https://pypi.org/project/pycac/)
PyCAC requires Python 3.6.4 or greater to run correctly. To check which version you have installed from the command line:
```
$ python --version
```
Then:

```
$ python -m pip install pycac
```
Once installed, PyCAC needs to be configured to communicate with your high performance computing (HPC) cluster. It will also install the CAC simulator package to the cluster. Please note that the PyCAC does NOT include the CAC simulator; the CAC simulator can be obtained with express permission from Prof. David L. McDowell. See [pycac.org](http://www.pycac.org/) for more.
```
$ python pycac --configure
```
Alternatively, if you already have CAC installed on the cluster, you may edit the appropriate fields in the provided `config_template.json` file. Please save this modified configuration file as `config.json` in your run folder. 

### Execution
Once PyCAC has been appropriately installed and configured:
```
$ python pycac --job
```
The graphical user interface will guide you through the project creation and simulation steps. 

#### More Information

* One functionality of PyCAC is the generation of input scripts to the CAC simulator. For sample input scripts, users are referred to [some example problems](http://www.pycac.org/chapter7/). 
* It is important to employ the correct interatomic potential, depending on the input script to be run. A number of interatomic potentials are provided in the `potentials` folder.  

### License

The GUI wrapper for CAC is released under the Apache Software License v2.0

The CAC simulator package must be requested separately, and is released under the following terms: 
Copyright (c) 2017-2018 Georgia Institute of Technology. All Rights Reserved.
NO public distribution.

### Note

This source code is provided as is, with no warranties or representations of accuracy or suitability for any application, and with no expectation of user support. Some information is provided in the [PyCAC user's manual](http://www.pycac.org). Please note the [citation requests](http://www.pycac.org/chapter1/ack-and-cite.html) for any derivative works based on application of this package.