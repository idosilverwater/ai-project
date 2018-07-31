class Constraint:
    def __init__(self, variables, possible_values, softness=1):
        """
        Builds a new constraint object.
        :param variables: a set of variable names, in a list. [name1, name2, name3]
        :param possible_values: a list of possible values: (assuming we have 2 variables)
                [[var_1_possible_val, var_2_possible_val], [var_1_possible_val, var_2_possible_val]...,]
                Which means a list of all possible combinations of values.
        assignment to the variables.
        :param softness: 1 if soft constraint, o.w. 0.
        """
        self.variables = variables
        self.possible_values = possible_values
        self.is_soft = softness
        self.set_of_variables = set(variables)

    # TODO not tested.
    def check_assignment(self, assignment):
        """
        goes through all possible tuples of assignment and find if there is at least one that is okay.
        :param assignment: a dictionary of {var_name, value,....} value is None if variable is unassigned.
        :return: True is assignment is okay, or false other wise.
        """
        # first, check if the variables relevant to this constraint are assigned. if not  we don't have a problem
        none_counter = 0
        for var_name in self.variables:
            if assignment[var_name] is None:
                none_counter += 1
        if none_counter == len(self.variables):
            return True
        # Gather all possible assignments that have the same value as of the values in the assignment.
        list_of_assignments = self.__collect_possible_assignments(assignment)

        for possible_assignment in list_of_assignments:
            counter = 0
            for variable_name in assignment:
                pos = self.get_variable_pos(variable_name)
                if pos != -1 and assignment[variable_name] is not None:
                    if assignment[variable_name] == possible_assignment[pos]:
                        counter += 1
                else:
                    counter += 1
            if counter == len(assignment):
                return True
        return False

    def __collect_possible_assignments(self, assignment):
        list_of_assignments = set()
        for variable_name in assignment:
            pos = self.get_variable_pos(variable_name)
            var_value = assignment[variable_name]
            if pos != -1 and var_value is not None:
                for possible_assignment in self.possible_values:
                    if possible_assignment[pos] == var_value:
                        list_of_assignments.add(tuple(possible_assignment))
        return list_of_assignments

    # TODO i think this is totally non relevant, and maybe should be removed.
    # def is_value_legit(self, variable_name, value):
    #     """
    #     checks if the value can be assigned to this variable.
    #     """
    #     pos = self.get_variable_pos(variable_name)
    #     if pos != -1:
    #         for possible_values in self.possible_values:
    #             if possible_values[pos] == value:  # needs at least one possible value for this to be a legit one.
    #                 return True
    #         return False
    #     return True  # this constraint doesn't care..

    def get_variable_pos(self, var_name):
        if var_name not in self.set_of_variables:
            return -1
        return self.variables.index(var_name)

    def get_variables(self):
        return self.variables

    def get_possible_values(self):
        return self.possible_values

    def get_number_of_constraints(self, assignment):
        """
        returns the number of possible assignments that are still present, given this assignmnet. (inclusive)
        :param assignment: a dictionary {var_name1: value,......}
        :return: an integer.
        """
        return len(self.__collect_possible_assignments(assignment))
