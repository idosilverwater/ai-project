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
variable_heuristic.add_argument('--mr',
                                help="Use the Minimum Remaining Val variable heuristic. only when using the Backtrack algoroithm",
                                action='store_true')
variable_heuristic.add_argument('--deg',
                                help="Use the Degree variable heuristic. only when using the Backtrack algoroithm",
                                action='store_true')

# TODO (For Jonathan) in the next line change the help message to a correct one. and change the default time to what
# you see fit. this is the time constant you asked for the backtrack. also you can change the type to int
# if it is more correct.
parser.add_argument('--bt-t', help="This is the max time for backtrack iteration (in secs)", default=5.0, nargs=1,
                    type=float)
parser.add_argument('--bt-forward-check', help="Use forward checking in backtrack", action='store_true')

parser.add_argument('--max-flips', help="Max flips in the WalkSAT algorithm", default=50, nargs=1, type=int)
parser.add_argument('--walksat-alpha',
                    help="In the WalkSAT algorithm exploration with alpha, exploitation with 1-alpha", default=0.5,
                    nargs=1, type=float)


def welcome():
    print("Welcome to the CSP solver problem.")
    print("Let's see if we can solve your problem")


days_of_week = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]


def seven_days_a_week(number):
    if 0 <= number <= 6:
        return days_of_week[number]
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


def worker_solve(filename, algo, softs, variable_heuristic, domain_heuristic, backtrack_timeout, forward_check,
                 max_flips, walksat_alpha):
    csp = create_workers_csp(filename, softs, variable_heuristic, domain_heuristic, forward_check)
    if algo == WALKSAT:
        algorithm = algorithms[algo](csp, max_flips=max_flips, random_value=walksat_alpha)
    elif algo == BACKTRACK:
        algorithm = algorithms[algo](csp, timeout=backtrack_timeout)
    print(type(algorithm))
    if algorithm.solve():
        print("Satisfiable")
        print_by_days(algorithm.get_assignment())
    else:
        print("Unsatisfiable")
    print("Done")


if __name__ == "__main__":
    welcome()
    args = parser.parse_args()
    print(args)

    if not (args.lc or args.mc or args.lws or args.mr or args.bt_t or args.bt_forward_check) and args.bt:
        parser.error('Heuristics are only to be used with the Backtrack algorithm.\nJust play by the rules! punk.')

    if not (args.max_flips or args.walksat_alpha) and args.ws:
        parser.error("max_flip and walksat_alpha are to be used only in conjunction with WalkSAT! \n Come on... you "
                     "don't need a babysitter.")

    if args.w:
        if args.bt:
            if args.mc:
                domain_heuristic = MIN_CONFLICT
            elif args.lc:
                domain_heuristic = LEAST_CONSTRAINING_VAL
            if args.mr:
                variable_heuristic = MIN_REMAINING_VAL
            elif args.deg:
                variable_heuristic = DEGREE
            worker_solve(args.filename, BACKTRACK, args.no_soft, variable_heuristic, domain_heuristic, args.bt_t,
                         args.bt_forward_check, None, None)
        elif args.ws:
            worker_solve(args.filename, WALKSAT, args.no_soft, None, None, None, None, args.max_flips[0],
                         args.walksat_alpha)
