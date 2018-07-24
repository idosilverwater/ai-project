class Solver:
    def __init__(self, csp):
        """
        assignment and csp should only be touched by the inheriting classes.
        :param csp: a constructed csp problem object.
        """
        # Notice: these variables are protected values and are meant to be used by the derivative classes.
        self.csp = csp
        self.assignment = {}
        for var_name in csp.variables:
            self.assignment[var_name] = None

    #########################
    # public functions:
    #########################

    def solve(self):
        pass  # should be implemented by the inheriting solvers.

    def get_assignment(self):
        return self.assignment

    #########################
    # Protected functions Not to be used by other than derivative classes:
    #########################
    def remove_value(self, var):
        self.assignment[var] = None
        self.csp.un_assign_variable(var)

    def is_assignment_complete(self):
        """
        checks if there is an assignment to all variables.
        :return: True if there is.
        """
        for var_name in self.assignment:
            if self.assignment[var_name] is None:
                return False
        return True

    def assignment_legit(self):
        return self.csp.check_assignment(self.assignment)

    def assign_value(self, var, value):
        self.assignment[var] = value
        self.csp.assign_variable(var, value)
