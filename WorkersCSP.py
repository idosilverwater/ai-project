from CSP import CSP
from Constraints import *
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
    preferences = new_lines[new_lines.index('Preferences:') + 1:]

    new_preferences = list()

    for preference in preferences:
        new_preferences.append(preference.split())

    return domain, names,  new_preferences

def create_workers_csp(filename):
    """
    gets filename of a workers csp kind and returns a an initialized CSP object

    :param filename: file that contains the problem
    :return:
    """

    with open(filename, 'r') as csp_file:
        lines = csp_file.readlines()

    domain, names, preferences = parser(lines)

    domain = [domain] * (len(names) * 7 * 3)



    variables = list()
    for name in names:
        for d in range(7):
            for s in range(3):
                variables.append(str(name) + " " + str(d) + " " + str(s))

    constraints = Constraints(preferences, variables)

    return CSP(domain, variables, constraints)
