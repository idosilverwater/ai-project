from VariableHeuristic import *


class Degree(VariableHeuristic):
    """
    This class represents degree heuristic.
    """

    def __init__(self, variables, constraints):
        VariableHeuristic.__init__(self, variables, constraints)
        self.__variables_by_neighbors = self.__init_var_by_neighbors()

    def __init_var_by_neighbors(self):
        """
        Initializes a list of tuples: (variable name, number of neighbors)
        :return: A list of tuples as described.
        """
        variables_by_neighbors = []
        for variable in self.variables:
            number_of_neighbors = len(variable.get_neighbores())
            name = variable.get_name()
            variables_by_neighbors.append((name, number_of_neighbors))
        return variables_by_neighbors

    def sort_variables(self):
        """ Selects the variable that influences more variables firs"""
        comperator = lambda x, y: x[1] > y[1]
        self._variables_by_neighbors = sorted(self.__variables_by_neighbors, comperator)
        return [*map(lambda x: x[0], self.__variables_by_neighbors)]
