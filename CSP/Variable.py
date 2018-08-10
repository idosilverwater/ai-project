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
        self.domain = set(domain_values)  # this is in order for check inside the domain values.
        self.constraints = constraints
        self.possible_domain = self.domain.copy()  # will get smaller or larger in time.
        self.value = None
        self.__constraint_set_holder = set(self.constraints)
        # forward checking relevant attributes:
        # self.affected_variables = []  # remembers the variables that were affected by forward checking.
        self.affecting_value = None  # remember the value to return in the end of forward checking restoration.

        self.neighbours_names = set()

    def add_constraint(self, constraint):
        if constraint not in self.__constraint_set_holder:
            self.constraints.append(constraint)
            self.__constraint_set_holder.add(constraint)

    def set_neighbours(self, set_of_neighbours):
        self.neighbours_names = set_of_neighbours

    def add_neighbours(self, set_of_neighbours):
        for neighbour in set_of_neighbours:
            self.neighbours_names.add(neighbour)

    def is_value_legit(self, value):
        """
        checks if a given value is in the domain of this variable, and if the value is in the possible domain.
        :param value: any object.
        :return: True or False.
        """
        return value in self.domain and value in self.possible_domain

    def __repr__(self):
        return "#name: " + self.name + ",dom: " + str(self.domain) + ", pos domain: " + str(
            self.possible_domain) + ", value: " + str(self.value)

    def get_neighbors(self):
        """
        returns a set object of neighbours names.
        """
        return self.neighbours_names

    def get_constraints(self):
        """
        returns a list of constraints this variable is tied too.
        """
        return self.constraints

    def get_possible_domain(self):
        """
        returns the domain this varible can still use.
        """
        return self.possible_domain

    def get_name(self):
        return self.name

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def set_affecting_value(self, value):
        self.affecting_value = value

    def get_affecting_value(self):
        return self.affecting_value

    def get_domain(self):
        """
        returns the full domain and not the possible domain.
        :return:
        """
        return self.domain

    def remove_from_possible_domain(self, value):
        """
        Removes value from self.possible_domain
        """
        self.possible_domain -= {value}

    def set_possible_domain(self, new_domain):
        self.possible_domain = set(new_domain)
