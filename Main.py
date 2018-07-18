from WorkersCSP import create_workers_csp
from Degree import *  # TODO(Noy): To remove.


if __name__ == "__main__":
   csp = create_workers_csp("examples/example1.csp")
   print(csp.constraints.get_all_constraints())


#########
# TESTS #
#########
csp = create_workers_csp("examples\example1.csp")
h = Degree(list(csp.variables.values()))
print(h.get_sorted_variables())