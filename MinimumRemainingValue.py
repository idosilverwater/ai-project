from VariableHeuristic import *


class MinimumRemainingValue(VariableHeuristic):
    """
    This class represents Degree Heuristic.
    """

    def __init__(self, variables):
        VariableHeuristic.__init__(self, variables)

    def init_sorted_variables(self):
        """
        Initializes a list of variables according to the heuristic - the
        variable with least remaining values is first.
        """
        variables_by_values = []  # A list of (var_name, |domains|)
        for variable in self.variables:
            possible_values = len(variable.get_possible_domain())
            name = variable.get_name()
            variables_by_values.append((name, possible_values))

        # In this part we sort the variables according to the heuristic:
        variables_by_values.sort(key=lambda tup: tup[1])
        self.sorted_variables = [*map(lambda x: x[0], variables_by_values)]


def minimum_remaining_value_heuristic_factory(variables):
    return MinimumRemainingValue(variables)
