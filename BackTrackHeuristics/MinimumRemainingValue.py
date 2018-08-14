from BackTrackHeuristics.VariableHeuristic import *


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
        for variable in self.var_names:
            var_obj = self.variables[variable]
            variables_by_values.append((var_obj.get_name(), len(var_obj.get_possible_domain())))

        # In this part we sort the variables according to the heuristic:
        variables_by_values.sort(key=lambda tup: tup[1])
        self.sorted_variables = [*map(lambda x: x[0], variables_by_values)]

    def select_unassigned_variable(self):
        return self.sorted_variables
