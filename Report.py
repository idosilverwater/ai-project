###########
# Imports #
###########
import WorkerCSP.WorkersCSP
from ReportTests import Tests as ts
from magicNums import *
from Solver.BackTrack import Backtrack
from Solver.WalkSat import WalkSat
import magicNums
import time

NUM_TESTS = 4
# folder names;
REPORT_FILES = "ReportScriptFiles"
TEST_FOLDER = REPORT_FILES + "/" + "TestFiles"
RESULTS_FOLDER = REPORT_FILES + "/" + "ResultFiles"
# file prefix names.
TEST_FILE_NAME = "Test"
RESULTS_FILE_BACKTRACK = "_BACKTRACK_RESULTS"
RESULTS_FILE_WALKSAT = "_WALKSAT_RESULTS"


def create_random_test_file(test_num, people_amount, preference_amount, no_work_shift_amount,
                            num_people_with_amount_shifts):
    with open(TEST_FOLDER + "/" + TEST_FILE_NAME + str(test_num), 'w') as random_example:
        random_example.writelines(
            ts.create_random_test(people_amount, preference_amount, no_work_shift_amount,
                                  num_people_with_amount_shifts))


def generate_test_files():
    create_random_test_file(1, 4, 5, 3, 2)
    create_random_test_file(2, 6, 5, 3, 2)


class Printer:
    """
    Printer class, provides an easy way to print assignments and make reports.
    """

    def __init__(self, file_name=None):
        self.days_of_the_week = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
        self.file_name = file_name

    def seven_days_a_week(self, number):
        if 0 <= number < len(self.days_of_the_week):
            return self.days_of_the_week[number]
        return "%s day" % str(number)

    def set_new_file(self, file_name):
        self.file_name = file_name

    def print(self, msg):
        print(msg, file=self.file_name)

    def print_by_days(self, assignment):
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

        print(file=self.file_name)
        print("Printing shifts:", file=self.file_name)
        print("----------------", file=self.file_name)
        for i, day in enumerate(all_shifts):
            print("%s workers are: " % self.seven_days_a_week(i), file=self.file_name)
            print(day, file=self.file_name)
            print("-----------------", file=self.file_name)

        print(file=self.file_name)
        print("Shifts per worker: ", file=self.file_name)
        print("-----------------", file=self.file_name)
        for name in num_days_var_works:
            print("%s is working %s shifts" % (name, num_days_var_works[name]), file=self.file_name)
            print("-----------------", file=self.file_name)

    def print_result_of_file(self, result_name, results, max_amount_of_workers_per_shift):
        """
        generates a report.
        :param result_name: the name of the report, should look like a filename where the filename is of the format:
            _Backtrack_ (or _Walksat_), Variable heuristic, domain heuristic, soft heuristic,
        :param results:
        :param max_amount_of_workers_per_shift:
        :return:
        """

        self.print("Results of: %s" % result_name)
        if results is None:
            self.print("Couldn't satisfy.")
            self.__seperate_result()
            return

        # Printing stats:
        num_vars, constraints_report, running_time = len(results[0]), results[1], results[2]
        self.print("Number of vars: %s" % str(num_vars))
        self.print("Max amount of workers per shift: %s" % str(max_amount_of_workers_per_shift))
        self.print("running time: %s" % str(running_time))

        for constraint_type in constraints_report:  # dict of {type: [num of satisfied, num of constraints]}
            constraint_results = constraints_report[constraint_type]
            temp = constraint_type, constraint_results[0], constraint_results[1]
            self.print("Constraint type %s have %s satisfied from overall %s" % (temp[0], temp[1], temp[2]))
        # printing shifts : (Not sure if wanted here)
        self.print_by_days(results[0])
        self.__seperate_result()

    def __seperate_result(self):
        self.print("*****************")
        self.print('')
        self.print('')

    def report_time_out(self, result_name):
        self.print("Results of: %s" % result_name)
        self.print("TIMEOUT reached.")
        self.__seperate_result()


class ReportGenerator:
    TIMEOUTE = -3

    def __init__(self, file_names, v_heuristics, d_heuristics, s_heuristics, max_workers_in_shift=2):
        self.heuristics = self.__make_heuristics_pairs(v_heuristics, d_heuristics, s_heuristics)
        self.files = file_names
        self.printer = Printer()
        self.max_amount_of_workers_in_shift = max_workers_in_shift

    def __make_heuristics_pairs(self, variable_heuristics, domain_heuristics, soft_heuristics):
        lst_of_pairs = []
        for v in variable_heuristics:
            for d in domain_heuristics:
                for s in soft_heuristics:
                    lst_of_pairs.append((v, d, s))
        return lst_of_pairs

    def __run_backtrack(self, csp_handler):
        report_assignment = True
        prev_best_assignment = None
        prev_running_time = 0
        best_num_constraint = 0
        for timeout in [30, 30, 30]:  # gives at most 30 seconds for an added constraint.
            algorithm = Backtrack(csp_handler, timeout)
            running_time = time.time()
            res = algorithm.solve()
            running_time = time.time() - running_time
            if res == magicNums.TIMEOUT_HARD_CONSTRAINT:
                csp_handler.restore_csp_handler()  # Restore csp handler for a retry.
                csp_handler.shuffle()  # Shuffle the csp handler, might find a better path.
            elif res == magicNums.TIMEOUT:
                temp = algorithm.get_num_soft_constraints_added()
                if temp > best_num_constraint:
                    best_num_constraint = temp
                    prev_best_assignment = algorithm.get_assignment()
                    prev_running_time = running_time
                csp_handler.restore_csp_handler()  # Restore csp handler for a retry.
                csp_handler.shuffle()  # Shuffle the csp handler, might find a better path.
            elif res == magicNums.FAILED:
                report_assignment = False
                return magicNums.FAILED, running_time, algorithm.get_assignment()
            else:
                csp_handler.get_report(algorithm.get_assignment())
                return magicNums.SUCCESS, running_time, algorithm.get_assignment()

        if prev_best_assignment is not None:
            print("Return value even though failure later on..")
            return magicNums.SUCCESS, prev_running_time, prev_best_assignment

        print("time out reached.")
        return magicNums.TIMEOUT_HARD_CONSTRAINT, None, None
        # print("True or false reached.")
        # return report_assignment, running_time, algorithm.get_assignment()

    @staticmethod
    def __backtrack_suffix(heuristic_triplet):
        return "_Backtrack_ " + "  ".join(heuristic_triplet)

    def __backtrack_results(self, file_name, results):
        for heuristic_triplet in self.heuristics:
            csp_handler = WorkerCSP.WorkersCSP.create_workers_csp(file_name, False, *heuristic_triplet, True,
                                                                  self.max_amount_of_workers_in_shift)

            report_assignment, running_time, curr_assignment = self.__run_backtrack(csp_handler)
            suffix = self.__backtrack_suffix(heuristic_triplet)

            if report_assignment == magicNums.SUCCESS:
                results[file_name + suffix] = (
                    curr_assignment, csp_handler.get_report(curr_assignment), running_time)
            elif report_assignment == magicNums.TIMEOUT_HARD_CONSTRAINT:
                results[file_name + suffix] = magicNums.TIMEOUT_HARD_CONSTRAINT
            else:
                results[file_name + suffix] = None
                break

    def generate_backtrack_report(self):
        """
        Runs backtrack with all possible options on the files of this Report object.
        generates a dictionary of results: {testX_backtrack_V_D_S_runningTime: (assignment, Csp_handler.get_report() )}
        Where _V_D_S are: V - the kind of variable heuristic, D - the kind of domain heuristic, S - the kind of soft
            constraints heuristic.
            Can be processed later on and saved into a file via some way we define.
        """
        results = {}
        for file_name in self.files:
            self.__backtrack_results(file_name, results)
        return results

    def generate_walksat_report(self):
        results = {}
        for file_name in self.files:
            self.__walksat_results(file_name, results)
        return results

    def __walksat_results(self, file_name, results):
        # walkSat does not need heuristics, and does not need forward checking at all.
        csp_handler = WorkerCSP.WorkersCSP.create_workers_csp(file_name, False, None, None, None, False,
                                                              self.max_amount_of_workers_in_shift)
        for probability in [0]:
            for max_flips in [50]:
                algorithm = WalkSat(csp_handler, probability, max_flips)
                runtime = time.time()
                algorithm.solve()
                runtime = time.time() - runtime
                suffix = "probability use percent: %s %%. Max flips num: %s " % (probability * 100, max_flips)
                results[file_name + suffix] = (
                    algorithm.get_assignment(), csp_handler.get_report(algorithm.get_assignment()), runtime)

    def print_backtrack_results(self, result_file_path):
        results = self.generate_backtrack_report()
        self.__print_results(result_file_path, results)

    def __print_results(self, result_file_path, results):
        with open(result_file_path, 'w') as file:
            self.printer.set_new_file(file)
            for results_name in results:
                if results[results_name] == magicNums.TIMEOUT_HARD_CONSTRAINT:
                    self.printer.report_time_out(results_name)
                else:
                    self.printer.print_result_of_file(results_name, results[results_name],
                                                      self.max_amount_of_workers_in_shift)

    def print_walksat_results(self, result_file_path):
        results = self.generate_walksat_report()
        self.__print_results(result_file_path, results)


if __name__ == '__main__':
    # generate_test_files()
    # variable_heuristics = [DEGREE, MIN_REMAINING_VAL]
    # domain_heuristics = [LEAST_CONSTRAINING_VAL, MIN_CONFLICT]
    # soft_heuristics = [DEGREE_SOFT_CONSTRAINT_HEURISTIC_TYPE, MAX_ASSIGNMENT_SOFT_CONSTRAINT_HEURISTIC,
    #                    NAME_SOFT_CONSTRAINT_HE'URISTIC]

    # create_random_test_file(0, 5, 10, 7, 2)
    # create_random_test_file(1, 5, 15, 10, 3)
    # create_random_test_file(2, 5, 20, 13, 4)
    # create_random_test_file(3, 10, 10, 7, 2)
    # create_random_test_file(4, 10, 15, 10, 3)
    # create_random_test_file(5, 10, 20, 13, 4)
    # create_random_test_file(6, 15, 15, 7, 2)
    # create_random_test_file(7, 15, 20, 13, 3)
    # create_random_test_file(8, 4, 5, 3, 2)
    # create_random_test_file(9, 6, 5, 3, 2)
    # Choose the heuristic combinations to genrate report with.
    variable_heuristics = [MIN_REMAINING_VAL]
    domain_heuristics = [MIN_CONFLICT]
    soft_heuristics = [MAX_ASSIGNMENT_SOFT_CONSTRAINT_HEURISTIC]

    #    -------------------------------------
    # file_names = [TEST_FOLDER + "/" + TEST_FILE_NAME + str(i) for i in range(10)]
    # file_names = ["ReportTests" + "/" + "random_test" + str(i) for i in range(1)]

    # report = ReportGenerator(file_names, variable_heuristics, domain_heuristics, soft_heuristics)
    # report.print_walksat_results(RESULTS_FOLDER + "/" + RESULTS_FILE_WALKSAT)

    # # Back track 6-9 tests:
    file_names = [TEST_FOLDER + "/" + TEST_FILE_NAME + str(i) for i in range(5, 10)]
    report = ReportGenerator(file_names, variable_heuristics, domain_heuristics, soft_heuristics)
    report.print_backtrack_results(RESULTS_FOLDER + "/" + RESULTS_FILE_BACKTRACK)
