from WorkersCSP import create_workers_csp
from Degree import *
from BackTrack import *
from LeastConstrainingValue import *
import sys
import argparse

parser = argparse.ArgumentParser(description="CSP solver.")

parser.add_argument('filename', type=str, help='Problem filename')
parser.add_argument('-prob-type', type=str, default='w', nargs=1, help='Problem type')
parser.add_argument('--no-soft', help='With/out soft constraints', action='store_true')
parser.add_argument('--algo', default='b', type=str, nargs=1, help='Algorithm to be used by the solver')

algorithms = {'b': Backtrack}


def welcome():
    print("Welcome to the CSP solver problem.")
    print("Let's see if we can solve your problem")


def worker_solve(filename, problem_type, algo, preferences):
    # filename = sys.argv[1] # TODO why is this needed?
    csp = create_workers_csp(filename, preferences)
    algorithm = algorithms[algo](csp)

    if algorithm.backtrack():  # TODO need the calling for the function to be generic. (J): Call backtrack.solve(), this was just my own test.
        print("Satisfiable")
        dic = algorithm.get_assignment()
        for key in dic:
            print(key + " : " + dic[key])
    else:
        print("Unsatisfiable")
    print("Done")


if __name__ == "__main__":

    welcome()

    if len(sys.argv) == 1:  # If no arguments are given we are in test mode
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

        worker_solve("examples/example2.csp", None, 'b', False)

        # print(csp.is_consistent('Sarah 6 1', 'True'))
        # assignment = {name: None for name in csp.variables.keys()}
        # for k in assignment:
        #     assignment[k] = 'False'
        # break
        # a = time.time()

        # csp.check_assignment(assignment)
        # print(time.time() - a)
        # print(c)
    else:
        args = parser.parse_args()
        print(args)
        worker_solve(args.filename, args.prob_type[0], args.algo[0], args.no_soft)
