from WorkerCSP.WorkersCSP import create_workers_csp
from BackTrackHeuristics.Degree import *
from Solver.BackTrack import *
from BackTrackHeuristics.LeastConstrainingValue import *
import magicNums
import sys
import argparse
import time
from Report import Printer

if __name__ == '__main__':
    print("Creating CSP")
    csp = create_workers_csp("ReportScriptFiles/TestFiles/Test1", False,
                             magicNums.DEGREE, magicNums.LEAST_CONSTRAINING_VAL,
                             magicNums.NAME_SOFT_CONSTRAINT_HEURISTIC, True, 2)
    csp.shuffle()
    pr = Printer()
    algorithm = Backtrack(csp, 30)
    print("Starting")
    a = time.time()
    solve_results = algorithm.solve()
    res = algorithm.get_assignment()
    if solve_results == magicNums.SUCCESS:
        res_message = "Satisfiable"
        pr.print_by_days(res)
    elif solve_results == magicNums.TIMEOUT:
        res_message = "Time out exceed."
        print(res)
    else:
        res_message = "Unsatisfiable"
    print(res_message)
    print("Runtime is concluded after %s seconds. " % (time.time() - a))
