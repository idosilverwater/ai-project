from BackTrackHeuristics.VariableHeuristic import *


# TODO need to update everything once  we add a constraint!!
class Degree(VariableHeuristic):
    """
    This class represents Degree Heuristic.
    """

    def __init__(self, variables):
        """
        Creates a new degree heuristic object.
        :param variables: A list of variable objects.
        """
        VariableHeuristic.__init__(self, variables)

    def init_sorted_variables(self):
        """
        Initializes a list of variables according to the heuristic - the
        variable with most neighbors is first and so on.
        """
        variables_by_neighbors = []  # A list of (var_name, |neighbors|)
        for variable in self.var_names:
            variables_by_neighbors.append(
                (self.variables[variable].get_name(), len(self.variables[variable].get_neighbors())))

        # In this part we sort the variables according to the heuristic:
        variables_by_neighbors = sorted(variables_by_neighbors, key=lambda tup: tup[1], reverse=True)
        # (J) Notice that there can be many variables with same neighbour, thus the order between them isn't determined.
        self.sorted_variables = [*map(lambda x: x[0], variables_by_neighbors)]

    def select_unassigned_variable(self):
        return self.sorted_variables
