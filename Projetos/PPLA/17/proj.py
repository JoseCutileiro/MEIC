'''
from minizinc import Instance, Model, Solver

# Load n-Queens model from file
nqueens = Model("./nqueens.mzn")
# Find the MiniZinc solver configuration for Gecode
gecode = Solver.lookup("gecode")
# Create an Instance of the n-Queens model for Gecode
instance = Instance(gecode, nqueens)
# Assign 4 to n
instance["n"] = 4
result = instance.solve()
# Output the array q
print(result["q"])

# Python program to read
# json file
'''
from minizinc import Instance, Model, Solver
from load_instance_data import *
import sys

# Criate instance
PTP = Model("./ptp.mzn")
gecode = Solver.lookup("gecode")
instance = Instance(gecode, PTP)

# Select a instance to solve
instance_file = 'instances/custom/custom_2.json'
instance_file = sys.argv[1]
# Load instance data
load_instance_data(instance,instance_file)


result = instance.solve()

json_res = create_solution_json(result,instance)

f = open(sys.argv[2],"w")
f.write(json.dumps(json_res,indent=2))
f.close()

# print(result)
# print(instance["category_set"])

#print(json.dumps(json_res,indent=2))