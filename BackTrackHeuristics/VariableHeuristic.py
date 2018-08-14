import random


class VariableHeuristic:
    """This class represents a domain heuristic"""

    def __init__(self, variables):
        """Defines a new heuristic"""
        self.variables = variables
        self.sorted_variables = []
        self.var_names = list(self.variables)
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

    def re_initialize_sort(self, variables):
        self.variables = variables
        self.sorted_variables = []
        self.var_names = list(self.variables)
        self.init_sorted_variables()

    def shuffle(self):
        """
        Offers a shuffle on the position of elements, will affect a stable sort.
        :return:
        """
        random.shuffle(self.var_names)
        self.init_sorted_variables()
