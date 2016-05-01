import os
import random

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

def main():
	#create_instance("Langevin Instances/N20ft204.dat","/tmp/prova.txt")
	
if __name__ == "__main__":
	main()
