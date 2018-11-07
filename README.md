# Prize-Collecting Traveling Salesman Problem with Time Windows (PCTSPTW)

This project has been made for educational purposes during the lecture of Model-Driven Decision Methods a.a 2015/16 (University Of Pisa). The goal is to implement a Linear Programming Model with [PuLP] and solve it with at least two different solvers: [CBC] and [GUROBI] (Accademic License) (feel free to use whatever you want/need!). At last  optimize one of these in order to improve time performance.

I wrote a simple report (in Italian) as description of the work I've done. If you need it please contact me.


## Requirements

* **Python 3.x**
* **PuLP** - as Python module
* **Pandas** - as Python module
* **Numpy** - as Python module
* [CBC]
* [GUROBI]

## Files and directories description
A brief description of project contents:

* **module. py** - implementation of PCTSPTW problem and solver call
* **instance_utility. py** - instances generators and other utility functions
* **data/** - contains all instances
* **src/** - source files

## Examples usage
Solve one instance using CBC with max_time=600s:

```sh
$ python3 src/model.py instance.dat CBC 600
```
Solve a set of instance using GUROBI with max_time=10s:
```sh
$ python3 src/model.py /path/to/instances_folder/ GUROBI 10
```

## Author
[Alessandro Romano]

[PuLP]:https://pythonhosted.org/PuLP/
[CBC]:https://projects.coin-or.org/Cbc
[GUROBI]:http://gurobi.com/
[Alessandro Romano]:mailto:alessandro.romano@linux.com
