from WorkersCSP import create_workers_csp
from Degree import *  # TODO(Noy): To remove.
from BackTrack import *
from LeastConstrainingValue import *
import sys

algorithms = {'b': Backtrack()}

if __name__ == "__main__":

    if len(sys.argv) == 1: # If no arguments are given we are in test mode
        # csp = create_workers_csp("examples/example1.csp")
        # print(csp.constraints.get_all_constraints())

        #########
        # TESTS #
        #########
        # csp = create_workers_csp("examples\example1.csp")
        # h = Degree(list(csp.variables.values()))
        # print(h.get_sorted_variables())

        ##############
        # J check ups:
        ##############
        import time

        csp = create_workers_csp("examples/example2.csp")
        b = Backtrack(csp)
        if b.backtrack():
            print("True")
            print(b.get_assignment())
        else:
            print("False")
        print("Done")
        # print(csp.is_consistent('Sarah 6 1', 'True'))
        # assignment = {name: None for name in csp.variables.keys()}
        # for k in assignment:
        #     assignment[k] = 'False'
        # break
        # a = time.time()

        # csp.check_assignment(assignment)
        # print(time.time() - a)
        # print(c)
    elif len(sys.argv) == 4 and (sys.argv[2] == "-w"):
        filename = sys.argv[1]
        csp = create_workers_csp(filename)
        algorithm = algorithms[sys.argv[3][1]]
        if algorithm.backtrack(): # TODO need the calling for the function to be generic (instead of "backtrack" "run")
            print("Satisfiable")
            print(algorithm.get_assignment())
        else:
            print("Unsatisfiable")
        print("Done")
    elif len(sys.argv) == 2 and (sys.argv[1] == "--help" or sys.argv[1] == '-h'):
        print("help message, need to make it print man page")
    else:
        print("For goodness' sake, enter the right amount of arguments...")
