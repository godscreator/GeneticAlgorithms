# Genetic Algorithms
Collection of genetic algorithms.
***
## Getting Started

### Import 
```Python
from Genetic.SingleObjectiveAlgorithms import *
```
```Python
from Genetic.MultiObjectiveAlgorithms import *
```

***
First, inherit from _'Gene'_ and implement its abstract methods. As shown below,

```Python
# we need to find maximum value of x^2 for x between -1000 and 1000.
# solution/gene is x and fitness is x^2.
# mutate is randomly add between -5 and 5.
# and crossover is points at a third and two-third from parents.

class X(Gene):
    
    @classmethod
    def create_random(cls):
        return X(random.randint(-1000,1000))
    
    def __init__(self, x):
        self.x = x
    
    def mutate(self):
        self.x += random.randint(-5,5)
    
    @staticmethod
    def crossover(parent_a, parent_b):
        return X((parent_a.x+parent_b.x*2)//3),X((parent_a.x*2+parent_b.x)//3)
    
    def calculate_fitness(self):
        return pow(self.x,2)
```
Next is 'GenePool'. Gene pool initializes and generates next generation of genes.
```Python
pool = GenePool(X, population_size, mutation_rate=0.05, crossover_rate=1, select_func=Selection.get_tournament(tournament_size=5))
pool.initialize_population()
while gen_count<max_gen_count:
    next_gen = pool.get_population()
```
***
## Examples
### TSP (single objective)
#### solving 
![Alt text](Example_TSP/assets/travelling_salesman_solved_sample.png?raw=true "Solving Sample image")
#### solved
![Alt text](Example_TSP/assets/travelling_salesman_solving_sample.png?raw=true "Solved Sample image")

### Schaffer's Study (multi objective)
#### solving 
![Alt text](Example_Schaffers_Study/assets/schaffers_solving_sample.png?raw=true "Solving Sample image")
#### solved (notice the formation of pareto front)
![Alt text](Example_Schaffers_Study/assets/schaffers_solved_sample.png?raw=true "Solved Sample image")