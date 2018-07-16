import DomainHeuristic
import sys

# please notice that this doesn't need an init. the init is in it's parent class DomainHeuristic (ido)


class LeastConstrainingValue(DomainHeuristic):

    def select_value(self, variable):
        """
        Selects the value for variable, that is least constricting to variables neighbors.
        neighbors being other variables that share at least one constraint with it.
        :param variable: The variable we want to assign a value to.
        :return: A value for variable according to the heuristic
        """
        min_conflicted_value = variable.domain[0]
        min_conflicts = float('inf')
        for d in variable.domain[1:]:
            cur = variable.conflicted_constraints(d)
            if min_conflicts > cur:
                min_conflicted_value = d
                min_conflicts = cur

        return min_conflicted_value


