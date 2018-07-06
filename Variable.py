class Variable:
    """
    Represent variable and saves relevant information inside it.
    """

    def __init__(self, name, domain_values):
        """
        :param name: name of the variable
        :param domain_values: a frozenSet containing possible values. values should be imutable.
        """
        # basic attributes:
        self.name = name
        self.domain = domain_values
        self.possible_domain = domain_values
        self.neighboursNames = []  # TODO add them.
        # forward checking relevant attributes:
        self.affected_variables = []  # remembers the variables that were affected by forward checking.
        self.affecting_value = None  # remember the value to return in the end of forward checking restoration.

    def forwad_checking_restore_self(self):
        """
        declares the variable as non affecting anybody, should be called when forward checking is done.
        :return: None.
        """
        self.affected_variables = []
        self.affecting_value = None
