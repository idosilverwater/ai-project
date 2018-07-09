from CSP import CSP

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
    names = new_lines[new_lines.index('Names:') + 1:new_lines.index('Constraints:')]
    constraints = new_lines[new_lines.index('Constraints:') + 1:]

    new_constraints = list()

    for constraint in constraints:
        new_constraints.append(constraint.split())

    return domain, names,  new_constraints

def create_workers_csp(filename):
    """
    gets filename of a workers csp kind and returns a an initialized CSP object

    :param filename: file that contains the problem
    :return:
    """

    with open(filename, 'r') as csp_file:
        lines = csp_file.readlines()

    domain, names, constraints = parser(lines)

    variables = list()
    for name in names:
        for d in range(7):
            for s in range(3):
                variables.append(str(name) + " " + str(d) + " " + str(s))

    return CSP(domain, variables, constraints)
