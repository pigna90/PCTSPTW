import os
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

##
# Adapts an AFG instance for
# Prize-collecting Traveling Salesman Problem with Time Windows (PCTSPTW)
# - Swaps time windows and distances matrix
# - Adds a random prize from 1 to 100(int) for each nodes except node 0
# - Substitutes the first row with non zero values
# - Adds a random number from 1 to 10(float) to each elements
# under the diagonal of distances matrix
##
# Params:
# old_instance - path to AFG instance file
# new_instance - path to new instance
# m_min, m_max - random values range for first row
# p_min, p_max - random values range for prize
##
def convert_AFG_instance(old_instance,new_instance,m_min=0,m_max=5,p_min=1,p_max=100):
	fp = open(old_instance)

	# Removing new instances if they exist
	try:
		os.remove(new_instance)
	except OSError:
		pass

	fp_out = open(new_instance,"a")

	# Reading each line from file and save them into a list
	lines = [line for i,line in enumerate(fp)]
	fp.close()

	# Selecting from the first line the number of nodes
	nodes = int(lines[0].split("\n")[0])
	# Writing the number of nodes into a new instance file
	fp_out.write("%s\n" % nodes)

	# Swapping the distances matrix with time windows
	lines = [lines[0]] + lines[nodes+1:nodes*2+1] + lines[1:nodes+1]

	# Selecting time series intervals and write them on a new instance
	# by adding a prize for each node
	for i in range(1,nodes+1):
		line_old = lines[i].split()
		fp_out.write("%s,%s %s\n" % (line_old[0],line_old[1].split("\n")[0],random.randint(1,100)))

	# Read first column and add a random number, write it as
	# first row of the matrix
	fp_out.write("0 ")
	for i in range(nodes+2,nodes*2+1):
		line = list(map(int,lines[i].split()))
		fp_out.write("%s " % (line[0] + random.randint(m_min,m_max)))
	fp_out.write("\n")

	# Writing the rest of the matrix from second row
	for i in lines[nodes+2:nodes*2+1]:
		fp_out.write(i)

##
# Adapts a TSPTW Langevin instance for
# Prize-collecting Traveling Salesman Problem with Time Windows (PCTSPTW)
# - Adds a random prize from 1 to 100(int) for each nodes except node 0
# - Moves node 0 from last line to first line
# - Makes distances matrix asimmetric
# - Adds a random number from 1 to 10(float) to each elements
# under the diagonal of distances matrix
##
# Params:
# old_instance - path to Langevin instance file
# new_instance - path to new instance
# m_min, m_max - random values range for asimmetric matrix
# p_min, p_max - random values range for prize
##
def convert_Lang_instance(old_instance,new_instance,m_min=0,m_max=5,p_min=1,p_max=100):
	fp = open(old_instance)

	# Removing new_instance if exist
	try:
		os.remove(new_instance)
	except OSError:
		pass

	fp_out = open(new_instance,"a")

	# Reading each line from file and save it into a list
	lines = [line for i,line in enumerate(fp)]
	fp.close()

	# Selecting from the first line the number of nodes
	nodes = int(lines[0].split("\n")[0])
	# Writing the number of nodes into a new instance file
	fp_out.write("%s\n" % nodes)

	# Selecting starting node from nodes+1 line (before matrix)
	# and write it on the first line with a prize equal to 0
	line_old = lines[nodes].split()
	fp_out.write("%s,%s %s\n" % (line_old[0],line_old[1].split("\n")[0],0))

	# Selecting and writing of time series intervals and writing on new
	# instance by adding a prize for each node
	for i in range(1,nodes):
		line_old = lines[i].split()
		fp_out.write("%s,%s %s\n" % (line_old[0],line_old[1].split("\n")[0],random.randint(1,100)))

	# Selecting distances matrix and writing into a new instance
	# file by adding a random value to each elements
	# under the diagonal
	for i in range(nodes+1,nodes+nodes+1):
		line = list(map(float,lines[i].split()))
		for r in range(0,i-(nodes+1)):
			line[r] = round(line[r] + (random.uniform(m_min,m_max)),1)
		for e in line:
			fp_out.write("%s " % e)
		fp_out.write("\n")

	fp_out.close()

##
# For every instance file in dir_in generates an instance
# with the same name in dir_out
##
# Params:
# dir_in - path to old instances directory
# dir_out - path to directory for new instances
##
def generate_instances(inst_name="Lang",dir_in="data/Langevin Instances/",dir_out="data/Instances_Lang/"):
	instances_list = os.listdir(dir_in)
	for inst in instances_list:
		if inst_name == "Lang":
			convert_Lang_instance(dir_in+inst, dir_out+inst)
		elif inst_name == "AFG":
			convert_AFG_instance(dir_in+inst, dir_out+inst)

##
# This function returns a dictionary contains the information
# for each instance:
# - Number of nodes
# - Time windows for each node
# - Price for each node
# - Matrix of distances
# Params:
##
# path - path of the file that contains the instance
##
def instance_loader(path):
	dictionary = {}
	# array contains all text file
	array = []
	# dictionary a contains the begin of the time windows for each node
	a = {}
	#dictionary b contains the close of the time windows for each node
	b = {}
	#dictionary p contains the price for each node
	p = {}

	count = 0
	i = 1
	array = open(path).read().splitlines()

	# variable n contains the number of nodes
	n = int(array[0])

	while(count < n):
		price = array[i].split()
		time = price[0].split(",")

		a.update({count : int(time[0])})
		b.update({count : int(time[1])})
		p.update({count : float(price[1])})

		count = count + 1
		i = i + 1

	i = n + 1

	# Creating matrix m filled with zeros
	m = np.zeros(shape=(n,n))

	# Populating of each row of matrix
	for j in range(0, n):
		temp = array[i].split()
		m[j] = temp
		i = i + 1

	dictionary = {"n": n, "a": a, "b": b, "p": p, "m": m}

	return dictionary

##
# Plots execution time results that has been saved on csv
##
# Params:
# timesPath - executsion times for two solvers
# graphPath - result graph name
##
def gurobi_cbc_times(timesPath,graphPath):
	df = pd.read_csv(timesPath)
	maxTime = max(max(df["GUROBI"]),max(df["CBC"]))
	# Normal graph
	df.plot(style="-o",xlim=1,ylim=(-10,maxTime+20),grid=True)
	plt.title("GUROBI VS CBC")
	plt.ylabel("Seconds")
	plt.xlabel("Instance")
	plt.savefig(graphPath, bbox_inches='tight')
	# Logarithmic scale y graph
	df.plot(style="-o",logy=True,xlim=1,ylim=(-10,maxTime+100),grid=True)
	plt.title("GUROBI VS CBC - Logy scale")
	plt.ylabel("Seconds")
	plt.xlabel("Instance")
	plt.savefig(graphPath+"_log.png", bbox_inches='tight')

	plt.close()
