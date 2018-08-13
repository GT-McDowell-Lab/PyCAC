# Installing PyCAC

The PyCAC Graphical user interface (GUI) is written and tested on Python 3.6.4. 

To check the installed version on your system, from the command line:
```
$ python --version
```

If you downloaded PyCAC from the [GitHub](https://github.com/GT-McDowell-Lab/PyCAC):
```
$ python -m pip install path_to_package
```
Alternatively, PyCAC may be installed directly from PyPi:
```
$ python -m pip install pycac
```

Once installed, PyCAC needs to be configured to communicate with the compute cluster. This will also install the CAC simulator to the cluster:
```
$ python pycac --configure
```
Please ensure that the correct workload manager and job queue are selected in this step. 