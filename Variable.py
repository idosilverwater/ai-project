class Variable:
    """
    Represent variable and saves relevant information inside it.
    """

    def __init__(self, name, domain_values, constraints):
        """
        :param name: name of the variable
        :param domain_values: a frozenSet containing possible values. values should be imutable.
        :param constraints: list of constraints objects the variable is in them.
        """
        # basic attributes:
        self.name = name
        self.domain = domain_values
        self.constraints = constraints
        self.possible_domain = self.domain  # will get smaller or larger in time.

        # forward checking relevant attributes:
        self.affected_variables = []  # remembers the variables that were affected by forward checking.
        self.affecting_value = None  # remember the value to return in the end of forward checking restoration.

        self.neighbours_names = set()

    def set_neighbours(self, set_of_neighbours):
        self.neighbours_names = set_of_neighbours

    def add_neighbours(self, set_of_neighbours):
        for neighbour in set_of_neighbours:
            self.neighbours_names.add(neighbour)

    def forward_checking_restore_self(self):
        """
        declares the variable as non affecting anybody, should be called when forward checking is done.
        :return: None.
        """
        self.affected_variables = []
        self.affecting_value = None

    def check_value_assignment(self, value):
        # TODO : should check all constraints if this value is legit. (intersection of constraints).
        pass

    #
    # todo very much like check_value_assignment. I think maybe we need only this one... (ido)
    #
    def conflicted_constraints(self, value):
        """"""
        pass

    #####################
    # Getters & Setters #
    #####################

    def get_neighbors(self):
        return self.neighbours_names

    def get_constraints(self):
        return self.constraints

    def get_possible_domain(self):
        return self.possible_domain

    def get_name(self):
        return self.name
