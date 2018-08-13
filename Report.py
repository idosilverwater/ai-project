###########
# Imports #
###########
import WorkerCSP.WorkersCSP
from ReportTests import Tests as ts
from magicNums import *
from Solver.BackTrack import Backtrack
import time

NUM_TESTS = 4
TEST_FILE_NAME = "Test"
TEST_FOLDER = "ReportScriptFiles"


def create_random_test_file(test_num, people_amount, preference_amount, no_work_shift_amount,
                            num_people_with_amnt_shifts):
    with open(TEST_FOLDER + "/" + TEST_FILE_NAME + str(test_num), 'w') as random_example:
        random_example.writelines(
            ts.create_random_test(people_amount, preference_amount, no_work_shift_amount, num_people_with_amnt_shifts))


def generate_test_files():
    pass  # TODO


class ReportGenerator:

    def __init__(self, file_names, v_heuristics, d_heuristics, s_heuristics):
        self.heuristics = self.__make_heuristics_pairs(v_heuristics, d_heuristics, s_heuristics)
        self.files = file_names

    def __make_heuristics_pairs(self, variable_heuristics, domain_heuristics, soft_heuristics):
        lst_of_pairs = []
        for v in variable_heuristics:
            for d in domain_heuristics:
                for s in soft_heuristics:
                    lst_of_pairs.append((v, d, s))
        return lst_of_pairs

    def __run_backtrack(self, csp_handler):
        report_assignment = True
        for timeout in [10, 20, 30]:  # gives at most 30 seconds for an added constraint.
            algorithm = Backtrack(csp_handler, timeout)
            running_time = time.time()
            res = algorithm.solve()
            running_time = time.time() - running_time
            if res is None:
                csp_handler.restore_csp_handler()  # Restore csp handler for a retry.
                # TODO should we add a shuffle - might give better results ?
                continue
            elif not res:
                report_assignment = False
            break  # we can break. it is either satisfiable or not at this point.
        return report_assignment, running_time, algorithm.get_assignment()

    @staticmethod
    def __backtrack_suffix(heuristic_triplet, running_time):
        return "_Backtrack_" + "_".join(heuristic_triplet) + str(int(running_time))

    def generate_backtrack_report(self):
        """
        Runs backtrack with all possible options on the files of this Report object.
        generates a dictionary of results: {testX_backtrack_V_D_S_runningTime: (assignment, Csp_handler.get_report() )}
        Where _V_D_S are: V - the kind of variable heuristic, D - the kind of domain heuristic, S - the kind of soft
            constraints heuristic.
            Can be processed later on and saved into a file via some way we define.
        """
        results = {}
        for file in self.files:
            for heuristic_triplet in self.heuristics:
                csp_handler = WorkerCSP.WorkersCSP.create_workers_csp(file, False, *heuristic_triplet, True, 2)

                report_assignment, running_time, curr_assignment = self.__run_backtrack(csp_handler)
                suffix = self.__backtrack_suffix(heuristic_triplet, running_time)

                if report_assignment:
                    results[file + suffix] = (curr_assignment, csp_handler.get_report(curr_assignment))
                else:
                    results[file + suffix] = None
                    break
        return results


################
def soft_heuristic_check():
    pass


def backtrack_heuristic_war(test_num):


# This is where I generate all of the interesting results :)
def back_track_tests():
    for i in range(NUM_TESTS):
        pass


def overall_test():  # TODO: Add to documentation what type of file I return.
    """
    This method generates all of the tests results.
    :return: A file contains the results.
    """

    params = [[0, 5, 4, 3, 1], [1, 5, 4, 3, 2]]

    for param_tuple in params:
        # creating file.
        create_random_test_file(*param_tuple)
        # running tests:
        # saving results.


if __name__ == '__main__':
    variable_heuristics = [DEGREE, MIN_REMAINING_VAL]
    domain_heuristics = [LEAST_CONSTRAINING_VAL, MIN_CONFLICT]
    soft_heuristics = [DEGREE_SOFT_CONSTRAINT_HEURISTIC_TYPE, MAX_ASSIGNMENT_SOFT_CONSTRAINT_HEURISTIC,
                       NAME_SOFT_CONSTRAINT_HEURISTIC]

    report = ReportGenerator(variable_heuristics, domain_heuristics, soft_heuristics)
    pass
# create_random_test_file(1, 5, 4, 3, 1)
