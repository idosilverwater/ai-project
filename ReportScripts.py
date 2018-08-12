###########
# Imports #
###########
import WorkerCSP.WorkersCSP


#########################
# BackTrack VS. WalkSAT #
#########################

def generate_input_file(n):
    """
    This one generates an example with n variables. Problems tend to be harder when n is high.
    :param n: The number of variables in the example.
    :return: A name(string) of a txt file representing an input to a CSP problem.
    """
    pass


def soft_constraints_test(domain_heuristic, variable_heuristic, no_soft=1, range=(1,20)):
    """
    This test checks how many soft constraints BT satisfies VS. how many Walk-SAT does as a function of the number of
    variables in the problem.
    :param no_soft: if True -> there will be no soft constraints.
    :param variable_heuristic: an init function of a variable heuristic class.
    :param domain_heuristic: an init function of a domain heuristic class.
    :param range: A tuple (x,y) when x is the lowest number of variables we use to test the problems and y is the highest.
    """
    lowest, highest = range[0], range[1]
    for i in range(lowest, highest):
        file_name = generate_input_file(i)
        csp = WorkerCSP.WorkersCSP.create_workers_csp(file_name, no_soft, variable_heuristic, domain_heuristic)


def hard_constraints_test(file_name, domain_heuristic, variable_heuristic, no_soft=1):
    """
    This test checks how many hard constraints BT satisfies VS. how many Walk-SAT does.
    :param file_name: file that contains the problem
    :param no_soft: if True -> there will be no soft constraints.
    :param variable_heuristic: an init function of a variable heuristic class.
    :param domain_heuristic: an init function of a domain heuristic class.
    """
    pass


###################
# BackTrack Tests #
###################
def least_constraining_value():
    pass


def degree():
    pass


def minimum_conflict():
    pass


def minimum_remaining_value():
    pass


def compare_heuristics():
    """
    Test how different heuristics influence the performance of BackTrack.
    """


def forward_checking_test():
    """
    Tests how much fc influences on the performance of BackTrack.
    """


#################
# WalkSAT Tests #
#################

def success_rates(max_flips):
    """
    Checks in if the algorithm succeed as a function of the number of attempts that the algorithm make.
    """


################
# Super - Test #
################

# This is where I generate all of the interesting results :)

def overall_test():  # TODO: Add to documentation what type of file I return.
    """
    This method generates all of the tests results.
    :return: A file contains the results.
    """
