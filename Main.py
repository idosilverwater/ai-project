from WorkerCSP.WorkersCSP import create_workers_csp
from Solver.BackTrack import *
from Solver.WalkSat import *
import argparse
from magicNums import *

# domain_heuristics = [MIN_CONFLICT, LEAST_CONSTRAINING_VAL]
# variable_heuristics = [MIN_REMAINING_VAL, DEGREE]
algorithms = {BACKTRACK: Backtrack, WALKSAT: WalkSat}
parser = argparse.ArgumentParser(description="CSP solver.")

parser.add_argument('filename', type=str, help='Problem filename')

problem_type = parser.add_mutually_exclusive_group()
problem_type.add_argument('-w', help="Worker Satisfication Problem", action='store_true')

parser.add_argument('--no-soft', help='With/out soft constraints', action='store_true')

algorithm = parser.add_mutually_exclusive_group()
algorithm.add_argument('--bt', help='Solve using BackTrack algorithm', action='store_true')
algorithm.add_argument('--ws', help='Solve using WalkSAT algorithm', action='store_true')
algorithm.add_argument('--lws', help='Solve using LogicalWalkSAT WalkSAT varient algorithm', action='store_true')

domain_heuristic = parser.add_mutually_exclusive_group()
domain_heuristic.add_argument('--mc',
                              help="Use the Minimum Conflict domain heuristic. only when using the Backtrack algoroithm",
                              action='store_true')
domain_heuristic.add_argument('--lc',
                              help="Use the Least Constraining Value domain heuristic. only when using the Backtrack algoroithm",
                              action='store_true')

variable_heuristic = parser.add_mutually_exclusive_group()
domain_heuristic.add_argument('--mr',
                              help="Use the Minimum Remaining Val variable heuristic. only when using the Backtrack algoroithm",
                              action='store_true')
domain_heuristic.add_argument('--deg',
                              help="Use the Degree variable heuristic. only when using the Backtrack algoroithm",
                              action='store_true')


def welcome():
    print("Welcome to the CSP solver problem.")
    print("Let's see if we can solve your problem")


def seven_days_a_week(number):
    if number == 0:
        return "sunday"
    elif number == 1:
        return "monday"
    elif number == 2:
        return "tuesday"
    elif number == 3:
        return "wednesday"
    elif number == 4:
        return "thursday"
    elif number == 5:
        return "friday"
    elif number == 6:
        return "saturday"
    else:
        return str(number)


def print_by_days(assignment):
    """
    Works only for the bakery problem.
    meant to present the workers that work in each shift nicely.
    :param assignment: a dictionary of workers, and if they work or not on a certain shift.
    """
    all_shifts = [[] for i in range(magicNums.DAYS_IN_WEEK)]
    for day_list in all_shifts:
        for i in range(magicNums.SHIFTS_IN_DAY):
            day_list.append([])

    num_days_var_works = {}
    for key in assignment:
        name_vals = key.split(" ")
        name = name_vals[0]
        if name not in num_days_var_works:
            num_days_var_works[name] = 0
        if assignment[key] == magicNums.DOMAIN_TRUE_VAL:
            all_shifts[int(name_vals[1])][int(name_vals[2])].append(name)
            num_days_var_works[name] += 1

    print()
    print("Printing shifts:")
    print("----------------")
    for i, day in enumerate(all_shifts):
        print("%s workers are: " % seven_days_a_week(i))
        print(day)
        print("-----------------")

    print()
    print("Shifts per worker: ")
    print("-----------------")
    for name in num_days_var_works:
        print("%s if working %s shifts" % (name, num_days_var_works[name]))
        print("-----------------")


def worker_solve(filename, algo, softs, variable_heuristic, domain_heuristic):
    csp = create_workers_csp(filename, softs, variable_heuristic, domain_heuristic)
    algorithm = algorithms[algo](csp)
    if algorithm.solve():
        print("Satisfiable")
        print_by_days(algorithm.get_assignment())
    else:
        print("Unsatisfiable")
    print("Done")


if __name__ == "__main__":
    welcome()
    args = parser.parse_args()

    print(12123123)
    print(args)

    if not (args.lc or args.mc or args.lws or args.mr) and args.bt:
        parser.error('Heurisitics are only to be used with the Backtrack algorithm.\nJust play by the rules! punk.')

    if args.w:
        if args.bt == BACKTRACK:
            if args.mc:
                domain_heuristic = MIN_CONFLICT
            elif args.lc:
                domain_heuristic = LEAST_CONSTRAINING_VAL
            if args.mr:
                variable_heuristic = MIN_REMAINING_VAL
            elif args.deg:
                variable_heuristic = DEGREE
            worker_solve(args.filename, BACKTRACK, args.no_soft, variable_heuristic, domain_heuristic)
        elif args.ws:
            worker_solve(args.filename, WALKSAT, args.no_soft, None, None)
