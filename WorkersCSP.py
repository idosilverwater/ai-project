from CSP import CSP
from Constraints import *
from magicNums import *
from Degree import *
from MinimumRemainingValue import *
from LeastConstrainingValue import *
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
    non_work_shift = new_lines[new_lines.index('NonWorkShift:') + 1:]

    new_preferences = list()

    for preference in preferences:
        new_preferences.append(preference.split())
    # if non_work_shift[0] == '':
    #     non_work_shift = []
    # if preference[0] == '':
    #     preference = []
    return domain, names, new_preferences, non_work_shift


# TODO preference is not needed, for that we have has add constraints, and make_visible.
def create_workers_csp(filename, preferences_include, variable_heuristic, domain_heuristic):
    """
    gets filename of a workers csp kind and returns a an initialized CSP object

    :param filename: file that contains the problem
    :return:
    """

    with open(filename, 'r') as csp_file:
        lines = csp_file.readlines()

    domain, names, preferences, non_work_shift = parser(lines)

    domain = [domain] * (len(names) * 7 * 3)

    variables = list()
    for name in names:
        for d in range(DAYS_IN_WEEK):
            for s in range(SHIFTS_IN_DAY):
                variables.append(str(name) + magicNums.SEPARATOR + str(d) + magicNums.SEPARATOR + str(s))

    if not preferences_include:
        preferences = list()



    if domain_heuristic == None: # For the case where WalkSAT is used. therefore we don't use heuristics.
        domain_factory = None
    elif domain_heuristic == LEAST_CONSTRAINING_VAL:
        domain_factory = LeastConstrainingValue
    elif domain_heuristic == MIN_CONFLICT:
        domain_factory = MinimumConflict

    if variable_heuristic == None: # For the case where WalkSAT is used. therefore we don't use heuristics.
        variable_factory = None
    elif variable_heuristic == MIN_REMAINING_VAL:
        variable_factory = MinimumRemainingValue
    elif variable_heuristic == DEGREE:
        variable_factory = Degree


    constraints = Constraints(preferences, non_work_shift, variables)
    # TODO create_workers_csp should receive which factory to give to the CSP class.
    return CSP(domain, variables, constraints, variable_factory, domain_factory)
