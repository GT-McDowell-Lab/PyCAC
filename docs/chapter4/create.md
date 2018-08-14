# PyCAC project creation

Once you have [installed PyCAC](installation.md), the application can be run from the install directory:
```
$ python -m pycac -j
```
From the launch window, select *Create Input File* to access the CAC job creator.
A [CAC input script](../chapter5/README.md) is generated, and a local project folder containing the [necessary files](../chapter3/input.md) to run a CAC job is created. Click *Next* once the appropriate fields are filled, and correct any errors indicated.
One can elect to set up [parametric study](parameterization.md) of select commands, and choose to only build the folder on the local machine for [direct runs](../chapter1/comp-and-exec.md), or submit the job to a performance computing cluster, e.g., those on [NSF XSEDE](http://www.xsede.org). 

### Security concerns
The open-source and highly-vetted Python implementation of the SSH2 protocol, [paramiko](https://pypi.org/project/paramiko/) is used to handle secure connections with the cluster.
