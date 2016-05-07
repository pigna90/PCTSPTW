from pulp import *
import numpy as np
from instance_utility import *
import sys

def main():

	# Read instance from file
	ris = instance_loader("inst")
	
	NODES = [n for n in range(1,ris["n"])]
	# Origin
	o = 0
	# Arrive
	d = len(NODES) + 1
	# Prizes
	p = ris["p"]
	p[d] = p[0]
	# Start time windows
	a = ris["a"]
	a[d] = a[0]
	# Stop time windows
	b = ris["b"]
	b[d] = b[0]
	# Archs's weight
	t = ris["m"]
	t = np.vstack((t,t[0]))
	t = np.concatenate((t,np.array([t[:,0]]).T),axis=1)

	# Maximize problem
	prob = LpProblem("PCTSPTW",LpMaximize)

	# y as decision variable for PoI
	y = LpVariable.dicts("y", NODES, 0, 1, LpBinary)

	# T as visit time at specific node
	T = LpVariable.dicts("T", ([o]+NODES+[d]),None,None,LpInteger)

	# x as decision variable for an arch between two node
	x = LpVariable.dicts("x", [(i,j)
		for i in ([o]+NODES)
		for j in (NODES+[d])
		if i!=j], 0, 1, LpBinary)

	## Print archs used
	#for i in [o]+NODES:
		#for j in [d]+NODES:
			#if(i!=j):
				#if(value(x[(i,j)]) != 1):
					#print(x[(i,j)]," ",value(x[(i,j)]))
	#quit()
	# Objective function
	prob += lpSum(p[i]*y[i] for i in NODES)

	# Constraint (1)
	for i in NODES:
		prob += lpSum(x[(i,j)] for j in ([d]+NODES) if i!=j) == y[i]

	# Constraint (2)
	for j in NODES:
		prob += lpSum(x[(i,j)] for i in ([o]+NODES) if i!= j) == y[j]

	# Constraint (3)
	prob += lpSum(x[(o,j)] for j in NODES) == 1

	# Constraint (4)
	prob += lpSum(x[(i,d)] for i in NODES) == 1

	# Constraint (5)
	for i in ([o]+NODES):
		for j in ([d]+NODES):
			if (i != j):
				prob += (T[i] + t[i][j] - T[j]) <= (max(b[i]+t[i][j]-a[j],0)*(1-x[(i,j)]))
				prob += x[(i,j)] >= 0

	# Constraint (6)
	for i in ([o]+NODES+[d]):
		prob += T[i] >= a[i]
		prob += T[i] <= b[i]

	prob.solve()

	# Print problem status
	print("Status solution: ",LpStatus[prob.status])
	print("--------")

	# Print PoI visited
	print("PoI visited")
	for i in NODES:
		if(value(y[i]) >= 1):
			print("y_" + str(i),"=",1)
	print("--------")

	edges = []
	# Print archs used
	for i in [o]+NODES:
		for j in [d]+NODES:
			if(i!=j):
				if(value(x[(i,j)]) >= 1):
					if j!=d:
						print("x(" + str(i) + "_" + str(j) + ") =",1)
						edges.append((i,j))
					else:
						print("x(" + str(i) + "_" + str(o) + ") =",1)
						edges.append((i,o))
	print("--------")

	# Print path
	path = []
	node = 0
	for i in range(1,len(edges)):
		for j in edges:
			if node == j[0]:
				path.append(node)
				node = j[1]
				edges.remove(j)
	path.append(0)

	print(path)
	print(*path,sep="->")
	

if __name__ == "__main__":
	main()
