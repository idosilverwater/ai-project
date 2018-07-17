from WorkersCSP import *  # TODO(Noy): Remove later
from VariableHeuristic import *


class Degree(VariableHeuristic):
    """
    This class represents Degree Heuristic.
    """

    def __init__(self, variables, constraints):
        """
        Creates a new degree heuristic object.
        :param variables: A list of variable objects.
        :param constraints: Al ist of constraints objects.
        """
        VariableHeuristic.__init__(self, variables, constraints)

    def init_sorted_variables(self):
        """
        Initializes a list of variables according to the heuristic - the
        variable with most neighbors is first and so on.
        """
        variables_by_neighbors = []  # A list of (var_name, |neighbors|)
        for variable in self.variables:
            number_of_neighbors = len(variable.get_neighbors())
            name = variable.get_name()
            variables_by_neighbors.append((name, number_of_neighbors))

        # In this part we sort the variables according to the heuristic:
        variables_by_neighbors.sort(key=lambda tup: tup[1])
        self.sorted_variables = [*map(lambda x: x[0], variables_by_neighbors)]
