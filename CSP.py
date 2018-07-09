from Constraints import *


class CSP:
    """
    main CSP handler. should be main authority for handling variables, domains and constraints.
    """

    # TODO determine what input the constructor should have.
    def __init__(self, domain, variables, soft_constraints):
        self.variables = {}  # the dictionary holds name=string: Variable instance.
        self.all_constraints = Constraints()  # TODO.
        self.visible_constraints = Constraints()
        self.domain_dictionary = {}  # holds name: frozenSet OfValues.
        self.variable_heuristic = None  # TODO.
        self.constraint_heurstic = None  # should choose the next constraint to add.
        self.domain_heuristic = None  # TODO.
        self._forward_checking_flag = None  # TODO.
        self.build_CSP(domain, variables, soft_constraints)

    def build_CSP(self, domain, variables, constraints):  # TODO implement
        """
        should build the csp constraints and whatnot...
        :return:
        """

        pass

    def make_visible(self):
        """
        makes all constraints visible.
        :return: None
        """
        pass

    def order_domain_values(self, variable_name):
        """
        Should return some list of values to follow.
        :param variable_name: the name of the variable to get it's domain value from.
        :return: a list of values to assign.
        """
        pass

    def select_unassigned_variable(self):
        """
        uses heuristic to choose a variable.
        :return: full variable.
        """
        pass

    def is_consistent(self, variable_name, value):
        """
        checks if this value can be assigned.
        :param variable_name: the name of the variable.
        :param value: value to try and assign to the variable.
        :return: True if it's okay, False otherwise.
        """
        pass

    def add_constraint(self):
        """
        add constraint to the visible constraint list.
        :return: True if it addded, False otherwise ( can return false if nothing to add).
        """
        pass

    def unassign_variable(self, variable_name, value):
        """
        does necessary updates to the csp object if the value should be un assigned.
        :param variable_name:
        :param value:
        :return:
        """
        pass
