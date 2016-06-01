# Prize-Collecting Traveling Salesman Problem with Time Windows (PCTSPTW)

This project is designed for educational purposes as project of the corse of Model-Driven Decision Methods a.a 2015/16 (University Of Pisa). The goal is implement a Linear Programming Model with [PuLP] and solve it with at least two different solvers, like [CBC] and [GUROBI] (Accademic License) in this case (feel free to use whatever you want/need). At last  optimize one of theese in order to improve performance.


### Tech
This is what you need before running: 

* **Python 3.x**
* **PuLP** - as Python module
* **Pandas** - as Python module
* **Numpy** - as Python module
* [CBC]
* [GUROBI]

### Files and directories description
A brief description of project contents:

* **module. py** - implementation of PCTSPTW problem and solver call
* **instance_utility. py** - instances generators and other utility functions
* **data/** - contain all instances

### Examples usage
Solve one instance using CBC with max time 600s:

```sh
$ python3 model.py instance.dat CBC 600
```
Solve a set of instance using GUROBI with max time 10s:
```sh
$ python3 model.py /path/to/instances_folder/ GUROBI 10
```

### Contact
[Alessandro Romano]

[PuLP]:https://pythonhosted.org/PuLP/
[CBC]:https://projects.coin-or.org/Cbc
[GUROBI]:http://gurobi.com/
[Alessandro Romano]:mailto:alessandro.romano@linux.com
