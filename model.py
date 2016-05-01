from pulp import *
import numpy as np
from instance_utility import *

def main():

	# Read instance from file
	ris = instance_loader("inst")
	
	NODES = [n for n in range(1,ris["n"])]
	# Origin and arrive (same node)
	d,o = [0],[0]
	# Prizes
	p = ris["p"]
	# Start time windows
	a = ris["a"]
	# Stop time windows
	b = ris["b"]
	# Archs's weight
	t = ris["m"]

	# Maximize problem
	prob = LpProblem("PCTSPTW",LpMaximize)

	# y as decision variable for PoI
	y = LpVariable.dicts("y", NODES, 0, 1, LpBinary)

	# T as visit time at specific node
	T = LpVariable.dicts("T", (d+NODES),None,None,LpInteger)

	# x as decision variable for an arch between two node
	x = LpVariable.dicts("x", [(i,j) for i in (d+NODES) for j in (d+NODES) if i!=j], 0, 1, LpBinary)

	# Objective function
	prob += lpSum(p[i]*y[i] for i in NODES)

	# Constraint (1)
	for i in NODES:
		prob += lpSum(x[(i,j)] for j in (d+NODES) if i!=j) == y[i]

	# Constraint (2)
	for j in NODES:
		prob += lpSum(x[(i,j)] for i in (o+NODES) if i!= j) == y[j]

	#for i in NODES:
	#	prob += T[0] <= T[i]

	# Constraint (3)
	prob += lpSum(x[(0,j)] for j in NODES) == 1

	# Constraint (4)
	prob += lpSum(x[(i,0)] for i in NODES) == 1

	# Constraint (5)
	for i in (NODES):
		for j in (o+NODES):
			if (i != j):
				prob += (T[i] + t[i][j] - T[j]) <= (max(b[i]+t[i][j]-a[j],0)*(1-x[(i,j)]))
				prob += x[(i,j)] >= 0

	# Constraint (6)
	for i in (d+NODES):
		prob += T[i] >= a[i]
		prob += T[i] <= b[i]

	prob.solve()

	# Print problem status
	print("Status solution: ",LpStatus[prob.status])
	print("--------")

	# Print PoI visited
	for i in NODES:
		if(value(y[i]) >= 1):
			print(y[i]," ",value(y[i]))
	print("--------")

	# Print archs used
	for i in d+NODES:
		for j in d+NODES:
			if(i!=j):
				if(value(x[(i,j)]) >= 1):
					print(x[(i,j)]," ",value(x[(i,j)]))
	print("--------")

	# Print T for used points
	for i in d+NODES:
		print(T[i]," ",value(T[i]))

if __name__ == "__main__":
	main()
