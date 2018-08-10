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

    f = open(filename + '.csv', 'w')

    first_line = ","
    for j in range(magicNums.DAYS_IN_WEEK):
        first_line += str(j) + ","
    f.writelines(first_line[:-1] + "\n")

    for i in range(magicNums.SHIFTS_IN_DAY):
        line = str(i) + ","
        for j in range(magicNums.DAYS_IN_WEEK):
            for name in names:
                if assignment[name + " " + str(j) + " " + str(i)] == magicNums.DOMAIN_TRUE_VAL:
                    line += name + " & "
            line = line[:-3]
            line += ","
        line = line[:-1]
        if i != magicNums.SHIFTS_IN_DAY - 1:
            line += '\n'
        f.writelines(line)

    f.close()


def worker_solve(filename, algo, softs, variable_heuristic, domain_heuristic):
    csp = create_workers_csp(filename, softs, variable_heuristic, domain_heuristic)
    algorithm = algorithms[algo](csp)
    if algorithm.solve():
        print("Satisfiable")
        dic = algorithm.get_assignment()
        # for key in dic:
        #     print(key + " : " + dic[key])
        make_csv(filename, dic)
    else:
        print("Unsatisfiable")
    print("Done")


if __name__ == "__main__":
    worker_solve("ReportTests/walkSAT", WALKSAT, False, None, None, )
