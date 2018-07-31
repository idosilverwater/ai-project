class DomainHeuristic:
    """This class represents a domain heuristic"""

    def __init__(self, constraints, variables, variable):
        self.constraints = constraints
        self.variables = variables
        self.variable = variable

    def get_order_domain(self):
        """
        Selects a value for variable according to the heuristic.
        :param variable: The variable we want to assign a value to.
        :return: A value for variable according to the heuristic
        """
        pass
