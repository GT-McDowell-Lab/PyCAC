## PyCAC

PyCAC, the concurrent atomistic-continuum (CAC) simulation environment, is a software suite that allows users to run CAC simulations and analyze data.

It is developed by the group of [Prof. David L. McDowell ](http://www.me.gatech.edu/faculty/mcdowell) at the Georgia Institute of Technology, in collaboration with the group of [Prof. Youping Chen](http://web.mae.ufl.edu/chenlab/) at the University of Florida and the group of [Prof. Liming Xiong](http://www.aere.iastate.edu/lmxiong/) at the Iowa State University. The code development was sponsored by

* National Science Foundation
	- Georgia Institute of Technology, CMMI-1232878
	- University of Florida, CMMI-1233113
	- Iowa State University, CMMI-1536925
* Department of Energy, Office of Basic Energy Sciences
	- University of Florida, DE-SC0006539

### Compilation

./install.sh

### Execution

./run.sh

There is only one input script (`cg2at.in`) in the `input` directory; for more input scripts, users are referred to [some example problems](http://www.pycac.org/chapter7/). It is important to employ the correct interatomic potential in the `potentials` directory, depending on the input script to be run.

### License

Copyright (c) 2017-2018 Georgia Institute of Technology. All Rights Reserved.

NO public distribution

### Note

This source code is provided as is, with no warranties or representations of accuracy or suitability for any application, and with no expectation of user support. Some information is provided in the [PyCAC user's manual](http://www.pycac.org). Please note the citation requests for any derivative works based on application of this source code:

[http://www.pycac.org/chapter1/ack-and-cite.html](http://www.pycac.org/chapter1/ack-and-cite.html)