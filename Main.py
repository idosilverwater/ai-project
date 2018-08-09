from WorkerCSP.WorkersCSP import create_workers_csp
from Solver.BackTrack import *
from Solver.WalkSat import *
import argparse
from magicNums import *

domain_heuristics = [MIN_CONFLICT, LEAST_CONSTRAINING_VAL]
variable_heuristics = [MIN_REMAINING_VAL, DEGREE]
algorithms = {BACKTRACK: Backtrack, WALKSAT: WalkSat}
parser = argparse.ArgumentParser(description="CSP solver.")

parser.add_argument('filename', type=str, help='Problem filename')

problem_type = parser.add_mutually_exclusive_group(required=True)
problem_type.add_argument('-w', help="Worker Satisfication Problem", action='store_true')

parser.add_argument('--no-soft', help='With/out soft constraints', action='store_true')

algorithm = parser.add_mutually_exclusive_group(required=True)
algorithm.add_argument('--bt', help='Solve using BackTrack algorithm')
algorithm.add_argument('--ws', help='Solve using WalkSAT algorithm')
algorithm.add_argument('--lws', help='Solve using LogicalWalkSAT WalkSAT varient algorithm')


domain_heuristic = parser.add_mutually_exclusive_group()
parser.add_argument('--domain-heuristic', choices=domain_heuristics, default='', type=str, nargs=1,
                    help='Domain heuristic to be used by the solver')
parser.add_argument('--variable-heuristic', choices=variable_heuristics, default='', type=str, nargs=1,
                    help='Variable heuristic to be used by the solver')


def welcome():
    print("Welcome to the CSP solver problem.")
    print("Let's see if we can solve your problem")


def worker_solve(filename, algo, softs, variable_heuristic, domain_heuristic):
    csp = create_workers_csp(filename, softs, variable_heuristic, domain_heuristic)
    algorithm = algorithms[algo](csp)
    if algorithm.solve():
        print("Satisfiable")
        dic = algorithm.get_assignment()
        for key in dic:
            print(key + " : " + dic[key])
    else:
        print("Unsatisfiable")
    print("Done")


if __name__ == "__main__":
    welcome()
    args = parser.parse_args()
    if (args.domain_heuristic[0] or args.variable_heuristic[0]) and args.algo[0] != BACKTRACK:
        parser.error('Heurisitics are only to be used with the Backtrack algorithm.\nJust play by the rules! punk.')

    if args.prob_type[0] == WORKER_PROB:
        if args.algo[0] == BACKTRACK:
            worker_solve(args.filename, args.algo[0], args.no_soft, args.variable_heuristic[0],
                         args.domain_heuristic[0])
        elif args.algo[0] == WALKSAT:
            print('no soft', args.no_soft)
            worker_solve(args.filename, args.algo[0], args.no_soft, None, None)
