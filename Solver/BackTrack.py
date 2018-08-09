from Solver.BaseSolver import *


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
        # Base case:
        if self.is_assignment_complete():
            if self.assignment_legit():
                return True
            return False
        # Body of recursion:
        var_name = None
        for var in self.csp.select_unassigned_variable():  # choose the variable that isn't assigned.
            if self.assignment[var] is None:
                var_name = var
                break

        assert (var_name is not None)  # TODO remove after tests. (sanity check)

        for value in self.csp.order_domain_values(var_name):
            if self.csp.is_consistent(var_name, value):
                self.assign_value(var_name, value)
                res = self.backtrack()
                if not res:
                    self.remove_value(var_name)
                else:
                    return True
        return False

    def solve(self):
        """
        tries and solve for the csp problem while adding more and more constraints to the problem.
        :return: False if there isn't a solution, True otherwise.
        """
        res = self.backtrack()  # try to satisfy hard constraints.
        if not res:
            return False

        while res and self.csp.add_constraint():  # while we can still add constraints - continues
            print("Adding constraint")
            self.reset_assignment()
            res = self.backtrack()
        return True
