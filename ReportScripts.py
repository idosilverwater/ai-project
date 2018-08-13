###########
# Imports #
###########
import WorkerCSP.WorkersCSP
from ReportTests import Tests as ts
from magicNums import *

NUM_TESTS = 4
TEST_FILE_NAME = "Test"
TEST_FOLDER = "ReportScriptFiles"


def create_random_test_file(test_num, people_amount, preference_amount, no_work_shift_amount,
                            num_people_with_amnt_shifts):
    with open(TEST_FOLDER + "/" + TEST_FILE_NAME + str(test_num), 'w') as random_example:
        random_example.writelines(
            ts.create_random_test(people_amount, preference_amount, no_work_shift_amount, num_people_with_amnt_shifts))


#########################
# BackTrack VS. WalkSAT #
#########################


# def generate_input_file(n, num_of_vars_wants_exac_shifts=2, amount_of_exac_shifts=3, num_of_preffered_days=4):
#     """
#     This one generates an example with n variables. Problems tend to be harder when n is high.
#     :param n: The number of variables in the example.
#     :return: A name(string) of a txt file representing an input to a CSP problem.
#     """
#     pass


def soft_constraints_test(domain_heuristic, variable_heuristic, no_soft=1, variables_num_range=(3, 10)):
    """
    This test checks how many soft constraints BT satisfies VS. how many Walk-SAT does as a function of the number of
    variables in the problem.
    :param no_soft: if True -> there will be no soft constraints.
    :param variable_heuristic: an init function of a variable heuristic class.
    :param domain_heuristic: an init function of a domain heuristic class.
    :param variables_num_range: A tuple (x,y) when x is the lowest number of variables we use to test the problems and y is the highest.
    """
    # lowest, highest = variables_num_range[0], variables_num_range[1]
    # for i in variables_num_range(lowest, highest):
    #     file_name = generate_input_file(i)
    #     csp = WorkerCSP.WorkersCSP.create_workers_csp(file_name, no_soft, variable_heuristic, domain_heuristic)


def hard_constraints_test(file_name, domain_heuristic, variable_heuristic, no_soft=1):
    """
    This test checks how many hard constraints BT satisfies VS. how many Walk-SAT does.
    :param file_name: file that contains the problem
    :param no_soft: if True -> there will be no soft constraints.
    :param variable_heuristic: an init function of a variable heuristic class.
    :param domain_heuristic: an init function of a domain heuristic class.
    """
    pass



# ###################
# # BackTrack Tests #
# ###################
# def least_constraining_value():
#     pass
#
#
# def degree():
#     pass
#
#
# def minimum_conflict():
#     pass
#
#
# def minimum_remaining_value():
#     pass
#
#
# def compare_heuristics():
#     """
#     Test how different heuristics influence the performance of BackTrack.
#     """
#     pass
#
#
# def forward_checking_test():
#     """
#     Tests how much fc influences on the performance of BackTrack.
#     """
#     pass
#
#
# #################
# # WalkSAT Tests #
# #################
#
# def success_rates(max_flips):
#     """
#     Checks in if the algorithm succeed as a function of the number of attempts that the algorithm make.
#     """
#     pass

def soft_heuristic_check():
    pass


def backtrack_heuristic_war(test_num):
    variable_heuristics = [DEGREE, MIN_REMAINING_VAL]
    domain_heuristics = [LEAST_CONSTRAINING_VAL, MIN_CONFLICT]
    lst_of_pairs = []
    for v in variable_heuristics:
        for d in domain_heuristics:
            lst_of_pairs.append((v, d))


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
    pass
# create_random_test_file(1, 5, 4, 3, 1)
