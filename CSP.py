from Constraints import *


class CSP:
    """
    main CSP handler. should be main authority for handling variables, domains and constraints.
    """
    # TODO determine what input the constructor should have.
    def __init__(self, variables):
        self.variables = {}  # the dictionary holds name=string: Variable instance.
        self.all_constraints = Constraints()  # TODO.
        self.visible_constraints = Constraints()
        self.domain_dictionary = {}  # holds name: frozenSet OfValues.
        self.variable_heuristic = None  # TODO.
        self.constraint_heurstic = None  # should choose the next constraint to add.
        self.domain_heuristic = None  # TODO.
        self._forward_checking_flag = None  # TODO.
        self.build_CSP()

    def build_CSP(self):  # TODO implement
        """
        should build the csp constraints and whatnot...
        :return:
        """
        pass


