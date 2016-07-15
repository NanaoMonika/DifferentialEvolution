# Differential Evolution

Differential evolution (DE) is a high performance, easy to implement, and low complexity population-based
optimization algorithms [1].

## Objective
This repository provides Python implementation of Differential Evolution algorithm for global optimization in following schemes:

* Micro Differential Evolution [1]
* Micro Differential Evolution with Scalar Random Mutation Factor (MDESM) [1]
* Micro Differential Evolution with Vectorized Random Mutation Factor (MDEVM) [1]
* Ensemble Differential Evolution
* Ensemble Micro-Differential Evolution (EMDE)
* Opposition-based Differential Evolution (ODE) [2]
* Ensemble Opposition-based Differential Evolution

## Objective Functions
Basically you can use any objective funtions introduced by WCCI competitions or write your own objective functions. For demonstration purpose, I am using the Black-Box-Optimization-Benchmarking (BBOB), consisted of 24 benchmark functions [4].

## Execution Instructions

Exceution command template:

python script_name.py F D MutatScale MutSchMode NP MutSchIndx

where the options for keywords are:
* NP: population size (any integer number greater than 6)
* D: any integer number greater than 2
* F: integer function number
* MutSchMode: mutation scheme mode ('static','population') 
* MutatScale: mutation scale factor  ('Cte','Scalar','Vector')
* MutSchIndx: mutation scheme index (0,1,2,3,4,'null')

The mutation scheme index:
  - DE/rand/1: 0
  - DE/best/1: 1
  - DE/tbest/1: 2  
  - DE/rand/2: 3
  - DE/best/2: 4

Note: if MutSchMod='population' then use MutSchIndx='null'; because 'population' stands for the ensemble mutation scheme mode, where the mutation scheme is selected randomly for each individual of popualtion from the above list [3].

Example for EMDVM algorithm (mde.py) with N_{P}=6, D=100, ensemble ('population') mutatio scheme mode, 'Vector' mutation scale factor and 'null' mutation scheme index:

python mde.py 10 100 'Vector' 'population' 6 'null'

All the coes are executable on high performance computing systems such as Sharcnet.
If you found the codes useful, please cite corresponding papers suggested in the References section.

## References

[1] Salehinejad, H., Rahnamayan, S., Tizhoosh, H.R. and Chen, S.Y., 2014, July. Micro-differential evolution with vectorized random mutation factor. In 2014 IEEE Congress on Evolutionary Computation (CEC) (pp. 2055-2062). IEEE.

Link: http://rahnamayan.ca/assets/documents/Micro-Differential%20Evolution%20with%20Vectorized%20Random%20Mutation%20Factor.pdf

[2] Salehinejad, H., Rahnamayan, S. and Tizhoosh, H.R., 2014, July. Type-II opposition-based differential evolution. In 2014 IEEE Congress on Evolutionary Computation (CEC) (pp. 1768-1775). IEEE.

Link: http://rahnamayan.ca/assets/documents/Type-II%20Opposition-Based%20Differential%20Evolution.pdf


[3] Salehinejad, H., Rahnamayan, S., and Tizhoosh, H.R., 2016, Exploration Enhancement in Ensemble Micro-Differential Evolution. In 2016 IEEE Congress on Evolutionary Computation (CEC). IEEE.

[4] http://coco.gforge.inria.fr/

