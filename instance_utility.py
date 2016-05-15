import os
import random
import numpy as np

##
# Adapt a TSPTW Langevin instance for
# Prize-collecting Traveling Salesman Problem with Time Windows (PCTSPTW)
# - Add a random prize from 1 to 100(int) for each nodes except node 0
# - Move node 0 on the first line
# - Make distances matrix asimmetric
# - Add a random number from 1 to 10(float) to each elements
# under the diagonal of distances matrix
# NB: Instance with more than one time window that start
# from 0 aren't valid
##
# Params:
# old_instance - path to Langevin instance file
# new_instance - path to new instance
# m_min, m_max - random values range for asimmetric matrix
# p_min, p_max - random values range for prize
##
def create_instance(old_instance,new_instance,m_min=0,m_max=5,p_min=1,p_max=100):
	fp = open(old_instance)

	# Remove new_instance if exist
	try:
		os.remove(new_instance)
	except OSError:
		pass
	
	fp_out = open(new_instance,"a")

	# Read every line from file and save into a list
	lines = [line for i,line in enumerate(fp)]
	fp.close()

	# Select from the first line the number of nodes
	nodes = int(lines[0].split("\n")[0])
	# Write the number of nodes into a new instance file
	fp_out.write("%s\n" % nodes)

	# Search starting node selecting time window that start from 0
	# and write it like first node with value prize to 0
	for i in range(1,nodes+1):
		line_old = lines[i].split()
		if(line_old[0] == "0"):
			fp_out.write("%s,%s %s\n" % (line_old[0],line_old[1].split("\n")[0],0))

	# Select and write time series intervals and write on new instance
	# adding prize for each node
	for i in range(1,nodes+1):
		line_old = lines[i].split()
		if(line_old[0] != "0"):
			fp_out.write("%s,%s %s\n" % (line_old[0],line_old[1].split("\n")[0],random.randint(1,100)))

	# Select distances matrix and write it into new instance
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

# This function return a dictionary contain the information
# for each instance:
# - Number of nodes
# - Time windows for each node
# - Price for each node
# - Matrix of distances
# Params:
##
# path - path of the file that contain the instance
##
def instance_loader(path):
	
	dictionary = {}
	# array contain all text file 
	array = []
	# dictionary a contain the begin of the time windows for each node
	a = {}
	#dictionary b contain the close of the time windows for each node
	b = {}
	#dictionary p contain the price for each node
	p = {}
	
	count = 0
	i = 1
	array = open(path).read().splitlines()  

	# variable n contain the number of nodes
	n = int(array[0])
	
	while(count < n):
		
		price = array[i].split(" ")
		time = price[0].split(",")
		
		a.update({count : int(time[0])})
		b.update({count : int(time[1])})
		p.update({count : float(price[1])})
		
		count = count + 1
		i = i + 1
	
	
	i = n + 1
	
	# create a matrix m of zero
	m = np.zeros(shape=(n,n))
	
	# populate each row of matrix 
	for j in range(0, n):
		temp = array[i].split()
		m[j] = temp
		i = i + 1
	
	dictionary = {"n": n, "a": a, "b": b, "p": p, "m": m}
		
	return dictionary

##
# For every instance file in dir_in generate an instance
# with same name in dir_out
##
# Params:
# dir_in - path to Langeving instances directory
# dir_out - path to directory for new instances
##
def generate_instances(dir_in="Langevin Instances/",dir_out="Instances/"):
	langevine_list = os.listdir(dir_in)
	for inst in langevine_list:
		create_instance(dir_in+inst, dir_out+inst)
	
if __name__ == "__main__":
	generate_instances()
