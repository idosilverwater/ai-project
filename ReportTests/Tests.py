from WorkerCSP.WorkersCSP import create_workers_csp, parser
import time
from Solver.BackTrack import *
from magicNums import *
from Solver.WalkSat import *

BACKTRACK = 'b'
WALKSAT = 'w'

algorithms = {'b': Backtrack, 'w': WalkSat}

def random_shifts(amount, names):
    shifts = []

    count = 0
    while count <= amount:
        name = random.choice(names)
        day = random.randint(0, DAYS_IN_WEEK - 1)
        shift_in_day = random.randint(0, SHIFTS_IN_DAY - 1)
        shift = name + " " + str(day) + " " + str(shift_in_day)

        if shift not in shifts:
            shifts.append(shift)
            count += 1

    return shifts


def create_random_test(people_amount, preference_amount, no_work_shift_amount):
    lines = []

    lines.append("Domain:\n")
    lines.append("True\n")
    lines.append("False\n")

    names = list()
    lines.append("Names:\n")
    for i in range(people_amount):
        names.append(str(chr(i + 65)))
        lines.append(str(chr(i + 65)) + "\n")

    shifts = random_shifts(preference_amount + no_work_shift_amount, names)
    preferences = shifts[:preference_amount]
    no_work_shifts = shifts[preference_amount:]

    lines.append("Preferences:\n")
    for preference in preferences:
        lines.append(preference + "\n")

    lines.append("NonWorkShift:\n")
    for no_work_shift in no_work_shifts:
        lines.append(no_work_shift + "\n")

    return lines


def create_random_test_file(test_num, people_amount, preference_amount, no_work_shift_amount):
    with open('ReportTests/random_test' + str(test_num), 'w') as random_example:
        random_example.writelines(create_random_test(people_amount, preference_amount, no_work_shift_amount))

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
    # worker_solve("ReportTests/test1", WALKSAT, False, None, None)
    # worker_solve("ReportTests/test1", BACKTRACK, False, MIN_REMAINING_VAL, LEAST_CONSTRAINING_VAL)
    create_random_test_file(0, 10, 30, 30)
    t = time.time()
    worker_solve("ReportTests/random_test0", WALKSAT, False, None, None)
    print(time.time() - t)

