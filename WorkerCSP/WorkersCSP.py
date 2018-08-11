from CSP.CspHandler import *
from WorkerCSP.Constraints import *
from BackTrackHeuristics.Degree import *
from BackTrackHeuristics.MinimumRemainingValue import *
from BackTrackHeuristics.LeastConstrainingValue import *
from BackTrackHeuristics.MinimumConflict import *
from magicNums import *


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


def create_workers_csp(filename, no_soft, variable_heuristic, domain_heuristic):
    """
    gets filename of a workers csp kind and returns a an initialized CSP object ready for the employee worker problem.

    :param filename: file that contains the problem
    :param no_soft: if True -> there will be no soft constraints.
    :param variable_heuristic: an init function of a variable heuristic class.
    :param domain_heuristic: an init function of a domain heuristic class.
    :return: a CSP to work with the employee worker problem constraints.
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

    # domain_heuristic is None: # For the case where WalkSAT is used. therefore we don't use heuristics.
    domain_factory = None
    if domain_heuristic == LEAST_CONSTRAINING_VAL:
        domain_factory = LeastConstrainingValue
    elif domain_heuristic == MIN_CONFLICT:
        domain_factory = MinimumConflict

    # if variable_heuristic is None: # For the case where WalkSAT is used. therefore we don't use heuristics.
    variable_factory = None
    if variable_heuristic == MIN_REMAINING_VAL:

        variable_factory = MinimumRemainingValue
    elif variable_heuristic == DEGREE:
        variable_factory = Degree

    constraints = Constraints(preferences, non_work_shift, variables, minimum_wanted_shifts)
    return CspHandler(domain, variables, constraints, variable_factory, domain_factory)
