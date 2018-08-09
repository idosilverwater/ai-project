from WorkerCSP.WorkersCSP import create_workers_csp, parser
from Solver.BackTrack import *
from Solver.WalkSat import *

BACKTRACK = 'b'
WALKSAT = 'w'

algorithms = {'b': Backtrack, 'w': WalkSat}


def make_csv(filename, assignment):
    with open(filename, 'r') as csp_file:
        lines = csp_file.readlines()

    domain, names, preferences, non_work_shift = parser(lines)

    f = open('test.csv', 'w')

    for i in range(magicNums.SHIFTS_IN_DAY):
        line = ""
        for j in range(magicNums.DAYS_IN_WEEK):
            for name in names:
                if assignment[name + " " + str(j) + " " + str(i)] == magicNums.DOMAIN_TRUE_VAL:
                    line += name + " & "
            line += ","
        line = line[:-1]
        if i != magicNums.SHIFTS_IN_DAY - 1:
            line += '\n'
        f.writelines(line)

    print('sdf')
    f.close()


def worker_solve(filename, algo, softs, variable_heuristic, domain_heuristic):
    csp = create_workers_csp(filename, softs, variable_heuristic, domain_heuristic)
    algorithm = algorithms[algo](csp)
    if algorithm.solve():
        print("Satisfiable")
        dic = algorithm.get_assignment()
        for key in dic:
            print(key + " : " + dic[key])
        make_csv(filename, dic)
    else:
        print("Unsatisfiable")
    print("Done")


if __name__ == "__main__":
    worker_solve("examples/all_can't_work_in_the_same_shift", WALKSAT, False, None, None)
