# Differential Evolution

Differential evolution (DE) is a high performance, easy to implement, and low complexity population-based
optimization algorithms [1].

This repository provides Python implementation of Differential Evolution algorithm for global optimization in following schemes:

* Micro Differential Evolution (DE.py) [1]
* Micro Differential Evolution with Scalar Random Mutation Factor (MDESM) (DE.py) [1]
* Micro Differential Evolution with Vectorized Random Mutation Factor (MDEVM) (DE.py) [1]
* Ensemble Differential Evolution (DE.py) [3]
* Ensemble Micro-Differential Evolution (EMDE) (DE.py) [3]
* Opposition-based Differential Evolution (ODE) (ODE.py) [2]
* Ensemble Opposition-based Differential Evolution (ODE.py) []
* Center-basis Differential Evolution (CDE.py) []

## Objective Functions
Basically you can use any objective funtion or write your own objective functions. For demonstration purpose, I am using the Black-Box-Optimization-Benchmarking (BBOB), consisted of 24 benchmark functions [4].
If need help in using other objective functions, just post an issue 
## Execution Instructions

Exceution command:

python DE.py F D MutatScale MutSchMode NP MutSchIndx

where the options for keywords are:
* NP: population size (any integer number greater than 6; For micro version NP=6 is recommended [1])
* D: any integer number greater than 2
* F: integer function number
* MutSchMode: mutation scheme mode (For Single Mutation Scheme: 'static', For Ensemble Mutation Scheme: 'population') 
* MutatScale: mutation scale factor  (For F=0.5: 'Cte', For MDESM: 'Scalar', For MDEVM: 'Vector')
* MutSchIndx: mutation scheme index (For DE/rand/1:0; For DE/best/1:1; For DE/tbest/1:2; For DE/rand/2:3; For DE/best/2:4; For Ensemble:'null')

Note: if MutSchMod='population' then use MutSchIndx='null'; because 'population' stands for the ensemble mutation scheme mode, where the mutation scheme is selected randomly for each individual of popualtion from the above list [3].

### Example
For example if we would run EMDVM (DE.py) with N_{P}=6, D=100, ensemble ('population') mutatio scheme mode, 'Vector' mutation scale factor and 'null' mutation scheme index the execution command will be:

python DE.py 10 100 'Vector' 'population' 6 'null'

### Excecution on high performance computing systems:
All the coes are executable on high performance computing systems such as Sharcnet. The shell script wrapper is provided in file wrapper.sh

### Note
If you find this page and codes useful, please cite the paeprs in the References section.

## References

[1] Salehinejad, H., Rahnamayan, S., Tizhoosh, H.R. and Chen, S.Y., 2014, July. Micro-differential evolution with vectorized random mutation factor. In 2014 IEEE Congress on Evolutionary Computation (CEC) (pp. 2055-2062). IEEE.

Link: http://rahnamayan.ca/assets/documents/Micro-Differential%20Evolution%20with%20Vectorized%20Random%20Mutation%20Factor.pdf

[2] Salehinejad, H., Rahnamayan, S. and Tizhoosh, H.R., 2014, July. Type-II opposition-based differential evolution. In 2014 IEEE Congress on Evolutionary Computation (CEC) (pp. 1768-1775). IEEE.

Link: http://rahnamayan.ca/assets/documents/Type-II%20Opposition-Based%20Differential%20Evolution.pdf


[3] Salehinejad, H., Rahnamayan, S., and Tizhoosh, H.R., 2016, Exploration Enhancement in Ensemble Micro-Differential Evolution. In 2016 IEEE Congress on Evolutionary Computation (CEC). IEEE.

[4] ODE paper to be added here

[5] center basis paper

[6] http://coco.gforge.inria.fr/

