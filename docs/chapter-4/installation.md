# Installing PyCAC


## Python version requirement
The PyCAC Graphical user interface (GUI) is written and tested on [Python 3.6.5](https://www.python.org/downloads/release/python-365/), but is compatible with newer versions when available. 

To check the installed version on your system, from the command line:
```
$ python --version
```

## Download and install

PyCAC may be installed directly from [PyPi](https://pypi.org/project/pycac/) using pip:
```
$ pip install pycac
```
If you downloaded a PyCAC release from the [GitHub](https://github.com/GT-McDowell-Lab/PyCAC/tree/master/gui/dist), replacing `V.v.v` with the version number indicated in the filenames:
```
$ pip install pycac-V.v.v-none-any.whl
OR
$ pip install pycac-V.v.v.tar.gz
```

## Configure 

Once installed, PyCAC needs to be configured to communicate with the compute cluster. This will also install the CAC simulator to the cluster:
```
$ python -m pycac --configure
```
Please ensure that the correct workload manager is selected in this step. PyCAC may now be used to [create](create.md) new CAC jobs. 