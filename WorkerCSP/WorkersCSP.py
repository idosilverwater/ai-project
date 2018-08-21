from CSP.CspHandler import *
from WorkerCSP.Constraints import *
from BackTrackHeuristics.Degree import *
from BackTrackHeuristics.MinimumRemainingValue import *
from BackTrackHeuristics.LeastConstrainingValue import *
from BackTrackHeuristics.MinimumConflict import *
from magicNums import *
from SoftConstraintHeuristics.MaxAssignmentSoftConstraintHeuristic import *
from SoftConstraintHeuristics.NameSoftConstraintHeuristic import *
from SoftConstraintHeuristics.RandomSoftHeuristic import *


# from MinimumConflict import *

def parser(lines):
    """
    parse the workers csp file lines into:
    list of domains
    list of names of workers
    and list of constraints
    :param lines:
    :return:
    """

    new_lines = list()
    for line in lines:
        new_lines.append(line[:-1])

    domain = new_lines[1:new_lines.index('Names:')]
    names = new_lines[new_lines.index('Names:') + 1:new_lines.index('Preferences:')]
    preferences = new_lines[new_lines.index('Preferences:') + 1:new_lines.index('NonWorkShift:')]
    non_work_shift = new_lines[new_lines.index('NonWorkShift:') + 1:new_lines.index("MinimumWantedShifts:")]
    list_of_wanted_shifts = new_lines[new_lines.index('MinimumWantedShifts:') + 1:]

    minimum_wanted_shifts = {name: int(value) for name, value in
                             map(str.split, list_of_wanted_shifts)}

    new_preferences = list()

    for preference in preferences:
        new_preferences.append(preference.split())

    return domain, names, new_preferences, non_work_shift, minimum_wanted_shifts


def __file_extractor(filename, no_soft):
    """
    Reads the file and return the information gathered from parsing it.
    """
    with open(filename, 'r') as csp_file:
        lines = csp_file.readlines()

    domain, names, preferences, non_work_shift, minimum_wanted_shifts = parser(lines)

    domain = [domain] * (len(names) * magicNums.DAYS_IN_WEEK * magicNums.SHIFTS_IN_DAY)

    variables = list()
    for name in names:
        for d in range(magicNums.DAYS_IN_WEEK):
            for s in range(magicNums.SHIFTS_IN_DAY):
                variables.append(str(name) + magicNums.VARIABLE_NAME_SHIFT_SEPARATOR + str(
                    d) + magicNums.VARIABLE_NAME_SHIFT_SEPARATOR + str(s))

    if no_soft:
        preferences = list()
    return variables, domain, preferences, non_work_shift, minimum_wanted_shifts


def __heuristic_chooser(variable_heuristic_type, domain_heuristic_type, soft_constraint_heuristic_type):
    """
    returns factories to use in Constraints, and CspHandler.
    """
    domain_factory = None
    if domain_heuristic_type == LEAST_CONSTRAINING_VAL:
        domain_factory = LeastConstrainingValue
    elif domain_heuristic_type == MIN_CONFLICT:
        domain_factory = MinimumConflict

    variable_factory = None
    if variable_heuristic_type == MIN_REMAINING_VAL:
        variable_factory = MinimumRemainingValue
    elif variable_heuristic_type == DEGREE:
        variable_factory = Degree

    # creating soft heuristic:
    soft_constraint_heuristic_factory = None
    if soft_constraint_heuristic_type == magicNums.DEGREE_SOFT_CONSTRAINT_HEURISTIC_TYPE:
        soft_constraint_heuristic_factory = DegreeSoftConstraintsHeuristic
    elif soft_constraint_heuristic_type == magicNums.MAX_ASSIGNMENT_SOFT_CONSTRAINT_HEURISTIC:
        soft_constraint_heuristic_factory = MaxAssignmentSoftConstraintHeuristic
    elif soft_constraint_heuristic_type == magicNums.NAME_SOFT_CONSTRAINT_HEURISTIC:
        soft_constraint_heuristic_factory = NameSoftConstraintHeuristic
    elif soft_constraint_heuristic_type == magicNums.RANDOM_SOFT_CONSTRAINT_HEURISTIC:
        soft_constraint_heuristic_factory = RandomSoftHeuristic

    return variable_factory, domain_factory, soft_constraint_heuristic_factory


def create_workers_csp(filename, no_soft, variable_heuristic, domain_heuristic,
                       soft_constraint_heuristic_type, forward_check=True, num_of_max_workers_in_shifts=2):
    """
    gets filename of a workers csp kind and returns a an initialized CSP object ready for the employee worker problem.

    :param filename: file that contains the problem
    :param no_soft: if True -> there will be no soft constraints.
    :param variable_heuristic: an init function of a variable heuristic class.
    :param domain_heuristic: an init function of a domain heuristic class.
    :param soft_constraint_heuristic_type: The type of soft constraint heuristic factory to create. Can choose between
        Degree, Max assignment and name heuristics.
    :param forward_check: True or false , determines if the CSP will employ  forward checking or not.
    :param num_of_max_workers_in_shifts: the amount of possible workers in a shift.
    :return: a CSP to work with the employee worker problem constraints.
    """
    # extracting information from the file.
    variables, domain, preferences, non_work_shift, minimum_wanted_shifts = __file_extractor(filename, no_soft)

    # choosing the heuristics:
    variable_factory, domain_factory, soft_constraint_heuristic = __heuristic_chooser(variable_heuristic,
                                                                                      domain_heuristic,
                                                                                      soft_constraint_heuristic_type)
    #
    constraints = Constraints(preferences, non_work_shift, variables, minimum_wanted_shifts, soft_constraint_heuristic,
                              num_of_max_workers_in_shifts)
    return CspHandler(domain, variables, constraints, variable_factory, domain_factory, forward_check)
