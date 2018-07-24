from Solver import Solver


class Backtrack(Solver):
    """
    a solver class, applies backtrack solving algorithm when solve class is initialized.
    """

    def __init__(self, csp):
        """
        excepts a csp problem initialized.
        """
        super(Backtrack, self).__init__(csp)

    def backtrack(self):
        """
        backtrack algorithm for the given csp problem.
        :return: True if assignment is possible. False otherwise
        """
        if self.is_assignment_complete():
            if self.assignment_legit():
                return True
            return False
        var_name = self.csp.select_unassigned_variable()
        for value in self.csp.order_domain_values(var_name):
            if self.csp.is_consistent(var_name, value):
                self.assign_value(var_name, value)
                if not self.backtrack():
                    self.remove_value(var_name)
        return False

    def __reset_assignment(self):
        """
        resets the current assignment.
        :return: None
        """
        self.assignment = self.assignment.fromkeys(self.assignment, None)

    def solve(self):
        """
        tries and solve for the csp problem while adding more and more constraints to the problem.
        :return: False if there isn't a solution, True otherwise.
        """
        res = self.backtrack()  # TODO check if it does backtrack only on hard constraints here.
        if not res:
            return False

        while res and self.csp.add_constraint():  # while we can still add constraints - continues
            self.__reset_assignment()
            res = self.backtrack()
        return True


# class for light check ups.
class DummyCsp:
    def __init__(self):
        self.variables = ["J1", "J2", "Lels", "LOls"]

    def select_unassigned_variable(self):
        return 'Lels'


# TESTS:
if __name__ == '__main__':
    lels = DummyCsp()
    b = Backtrack(lels)
    b.solve()
    pass
