# Existing project upload

Start the main GUI application
```
$ python pycac -j
```
Select *Submit Job* and find the project folder to upload. This should follow the format folder created using the [job creation tool](create.md), consisting of a project folder, and self-contained sub-folders of individual runs as follows:
```
    |-projectname/
    |-----|Run1/
    |-----|----|input.in
    |-----|----|potential files (*.tab or *.lj)
    |-----|----|restart files(optional)
    |-----|Run2/
    ....
```
The existing values will be validated, and one can adjust the values if desired. Job submission and parameterization proceeds as in the [job creation mode](create.md)

Note that any parameterizations defined here will create simulation subdirectories *in addition* to the ones existing in the project folder. 