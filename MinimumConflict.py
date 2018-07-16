import DomainHeuristic

# please notice that this doesn't need an init. the init is in it's parent class DomainHeuristic (ido)


class MinimumConflict(DomainHeuristic):

    def select_value(self, variable):
        """
        Selects a value out of variable's domain, that dissatisfies the least amount of constraints
        (that variable is a part of).
        :param variable: The variable we want to assign a value to.
        :return: A value for variable according to the heuristic
        """

        min_conflicted_value = variable.domain[0]
        min_conflicts = float('inf')
        for d in variable.domain:
            cur = len(variable.conflicted_constraints(d))
            if min_conflicts > cur:
                min_conflicted_value = d
                min_conflicts = cur

        return min_conflicted_value



