class VariableHeuristic:
    """This class represents a domain heuristic"""

    def __init__(self, variables):
        """Defines a new heuristic"""
        self.variables = variables
        self.sorted_variables = []
        self.init_sorted_variables()

    def init_sorted_variables(self):
        """
        Initializes a list of variables according to the heuristic - the
        variable with most neighbors is first and so on.
        """
        self.sorted_variables = []

    def get_sorted_variables(self):
        """ Returns a list of sorted variables names"""
        return self.sorted_variables
