import DomainHeuristic
import sys

# please notice that this doesn't need an init. the init is in it's parent class DomainHeuristic (ido)


class LeastConstrainingValue(DomainHeuristic):

    def neighbor_constriction(self, variable, value):
        """
        This returns the amount of domain values that have been blocked off for the neighboring variables.
        :return:
        """

        # TODO finish this

        neighbors = variable.get_neighbors()

        count = 0

        for neighbor in neighbors:

            neighbor.get_constraints()


        return count





    def select_value(self, variable):
        """
        Selects the value for variable, that is least constricting to variables neighbors.
        neighbors being other variables that share at least one constraint with it.
        :param variable: The variable we want to assign a value to.
        :return: A value for variable according to the heuristic
        """

        min_constraining_value = variable.domain[0]
        min_constrain = float('inf')

        for d in variable.domain:
            cur = self.neighbor_constriction(variable, d)
            if min_conflicts > cur:
                min_conflicted_value = d
                min_conflicts = cur

        return min_conflicted_value


