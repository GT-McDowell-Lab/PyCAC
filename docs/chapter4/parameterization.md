# Parameteric study

PyCAC facilitates parametric study of select variables in CAC simulations. From the job submission window, click **+** to add a new parameterization, and select the desired [command](../chapter5/README.md) and available values from the dropdown menus. Fill in desired parameters for *Increase* and *Number of Steps*. 

### Single-value parameters
As an example, if we choose to parameterize the command [`grain_dir`](../chapter5/grain_dir) `overlap`, with *Increase = 5.0* and *Number of Steps = 10"*. 

Initially the command in the input file reads:
```
grain_dir 2 0.0
```
10 *additional* simulation folders will be created, increasing the base value of overlap to **5.0** from **0.0**. The lines in the corresponding input scripts would change as follows:
```
grain_dir 2 0.5
grain_dir 2 1.0
...
grain_dir 2 5.0
```
### Vector-value parameters
If the command to be parameterized is vector-valued, for example in grain orientations defined in [`grain_mat`](../chapter5/grain_mat.md), then *Increase* should similarly be a vector *[di, dj, dk]*. The text field will indicate if this special format is required. 

### Multiple parameterizations
Multiple parameterizations in one project can be declared. If the number of steps are N and M for the first and second parameterizations, respectively, (N+1)x(M+1) *total* simulations will be generated. 

