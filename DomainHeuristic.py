
class DomainHeuristic:
    """This class represents a domain heuristic"""

    def __init__(self, variables, constraints):
        """Defines a new heuristic"""
        self.variables = variables
        self.constraints = constraints

    def select_value(self, variable):
        """
        Selects a value for variable according to the heuristic.
        :param variable: The variable we want to assign a value to.
        :return: A value for variable according to the heuristic
        """
        pass
