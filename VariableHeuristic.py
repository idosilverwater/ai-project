class VariableHeuristic:
    """This class represents a domain heuristic"""

    def __init__(self, variables, constraints):
        """Defines a new heuristic"""
        self.variables = variables
        self.constraints = constraints

    def select_variable(self):
        """
        Selects a variable according to the heuristic.
        :return: A variable object.
        """
