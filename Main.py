from WorkerCSP.WorkersCSP import create_workers_csp
from Solver.BackTrack import *
from Solver.WalkSat import *
import argparse
from magicNums import *
from Report import Printer

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

soft_heuristic = parser.add_mutually_exclusive_group()
soft_heuristic.add_argument('--sma',
                            help="Use the Soft Max Assignment heuristic for the soft constraint heuristic",
                            action='store_true')
soft_heuristic.add_argument('--sn',
                            help="Use the Soft Name heuristic for the soft constraint heuristic",
                            action='store_true')
soft_heuristic.add_argument('--sd',
                            help="Use the Soft Degree heuristic for the soft constraint heuristic",
                            action='store_true')

parser.add_argument('--bt-t', help="The maximum amount a backtrack session is allowed to run. Default timeout is 30",
                    default=30.0, nargs=1,
                    type=float)
parser.add_argument('--bt-forward-check', help="Use forward checking in backtrack", action='store_true')

parser.add_argument('--max-flips', help="Max flips in the WalkSAT algorithm", default=50, nargs=1, type=int)
parser.add_argument('--walksat-alpha',
                    help="In the WalkSAT algorithm exploration with alpha, exploitation with 1-alpha", default=0.5,
                    nargs=1, type=float)

parser.add_argument('--mws', help="Max amount of workers per shift", default=2, nargs=1,
                    type=int)


def welcome():
    print("Welcome to the CSP solver problem.")
    print("Let's see if we can solve your problem")


def worker_solve(filename, algo, softs, variable_heuristic, domain_heuristic, backtrack_timeout, forward_check,
                 max_flips, walksat_alpha, soft_constraint_heuristic_type, num_of_max_workers_in_shifts):
    csp = create_workers_csp(filename, softs, variable_heuristic, domain_heuristic, soft_constraint_heuristic_type,
                             forward_check, num_of_max_workers_in_shifts)
    algorithm = None
    if algo == WALKSAT:
        algorithm = algorithms[algo](csp, max_flips=max_flips, random_value=walksat_alpha)
    elif algo == BACKTRACK:
        algorithm = algorithms[algo](csp, timeout=backtrack_timeout)
    else:
        print("ERROR.")
        exit(-1)
    print(type(algorithm))
    res = algorithm.solve()
    out_file = None  # TODO add an option to add file or not, if it's None will print into stdout.
    printer = Printer(out_file)
    if res == magicNums.SUCCESS:
        print("Satisfiable")
        printer.print_by_days(algorithm.get_assignment())
    elif res == magicNums.TIMEOUT:
        print("Timeout on the last constraint. Printing ")
        printer.print_by_days(algorithm.get_assignment())
    elif res == magicNums.TIMEOUT_HARD_CONSTRAINT:
        print("Timeout one Hard constraints, did not achieve any assignment. "
              "Please try again, or use a different solver.")
    else:
        print("Unsatisfiable")
    print("Done")


if __name__ == "__main__":
    welcome()
    args = parser.parse_args()
    print(args)

    if not (args.bt or args.ws or args.lws):
        parser.error('Must input an algorithm')

    if not (
            args.lc or args.mc or args.lws or args.mr or args.bt_t or args.bt_forward_check or args.sma or args.sn or args.sd) and args.bt:
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
            if args.sma:
                soft_heuristic = MAX_ASSIGNMENT_SOFT_CONSTRAINT_HEURISTIC
            elif args.sn:
                soft_heuristic = NAME_SOFT_CONSTRAINT_HEURISTIC
            elif args.sd:
                soft_heuristic = DEGREE_SOFT_CONSTRAINT_HEURISTIC_TYPE
            worker_solve(args.filename, BACKTRACK, args.no_soft, variable_heuristic, domain_heuristic, args.bt_t,
                         args.bt_forward_check, None, None)
        elif args.ws:
            worker_solve(args.filename, WALKSAT, args.no_soft, None, None, None, None, args.max_flips[0],
                         args.walksat_alpha, soft_heuristic, args.mws[0])
