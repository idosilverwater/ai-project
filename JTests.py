from WorkerCSP.WorkersCSP import create_workers_csp
from BackTrackHeuristics.Degree import *
from Solver.BackTrack import *
from BackTrackHeuristics.LeastConstrainingValue import *
import magicNums
import sys
import argparse
import time


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
        return "%s day" % str(number)


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


if __name__ == '__main__':
    print("Creating CSP")
    csp = create_workers_csp("examples/example2.csp", False, magicNums.DEGREE, magicNums.MIN_CONFLICT,
                             magicNums.DEGREE_SOFT_CONSTRAINT_HEURISTIC_TYPE, True, 2)
    algorithm = Backtrack(csp, 10)
    print("Starting")
    a = time.time()
    solve_results = algorithm.solve()
    res = algorithm.get_assignment()
    if solve_results:
        res_message = "Satisfiable"
        print_by_days(res)
    elif solve_results is None:
        res_message = "Time out exceed."
        print(res)
    else:
        res_message = "Unsatisfiable"
    print(res_message)
    print("Runtime is concluded after %s seconds. " % (time.time() - a))
