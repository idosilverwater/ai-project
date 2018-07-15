from WorkersCSP import *  # TODO(Noy): Remove later


class Degree:
    """
    This class represents Degree Heuristic.
    """

    def __init__(self, variables, constraints):
        """
        Creates a new degree heuristic object.
        :param variables: A list of variable objects.
        :param constraints: Al ist of constraints objects.
        """
        self.__variables = variables
        self.__constraints = constraints
        self.__variables_by_neighbors = self.__init_var_by_neighbors()

    def __init_var_by_neighbors(self):
        """
        Initializes a list of tuples: (variable name, number of neighbors)
        :return: A list of tuples as described.
        """
        variables_by_neighbors = []
        for variable in self.__variables:
            number_of_neighbors = len(variable.get_neighbores())
            name = variable.get_name()
            variables_by_neighbors.append((name, number_of_neighbors))
        return variables_by_neighbors

    def sort_variables(self):
        """ Selects the variable that influences more variables first"""
        comparator = lambda x, y: x[1] > y[1]
        self._variables_by_neighbors = sorted(self.__variables_by_neighbors,
                                              comparator)
        return [*map(lambda x: x[0], self.__variables_by_neighbors)]


#########
# TESTS #
#########
csp = create_workers_csp("examples\example1.csp")
d = Degree(csp.variables, csp.constraints)
print(d.sort_variables())
