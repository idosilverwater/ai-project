from WorkersCSP import create_workers_csp, parser
from Degree import *  # TODO(Noy): To remove.
from BackTrack import *
from WalkSat import *
from LeastConstrainingValue import *

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



def worker_solve(filename, algo, preferences):
    csp = create_workers_csp(filename, preferences)
    algorithm = algorithms[algo](csp)
    if algorithm.solve(): # TODO need the calling for the function to be generic (instead of "backtrack" "run")
        print("Satisfiable")

        dic = algorithm.get_assignment()

        print(1, algorithm.get_num_satisfied())
        print(2, len(algorithm.constraints))

        for v in dic:
            print(v, ":", dic[v])
        make_csv(filename, dic)

    else:
        print("Unsatisfiable")
    print("Done")

if __name__ == "__main__":
    worker_solve("examples/example1.csp", WALKSAT, True)

