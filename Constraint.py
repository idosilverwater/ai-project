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

    # TODO not tested.
    def check_assignment(self, assignment):
        """
        goes through all possible tuples of assignment and find if there is at least one that is okay.
        :param assignment: a dictionary of {var_name, value,....} value is None if variable is unassigned.
        :return: True is assignment is okay, or false other wise.
        """
        all_none = True
        for var_value in assignment.values():
            if var_value is not None:
                all_none = False
                break

        if all_none:  # TODO not sure if above and this check are necessary (all of above in this func can be deleted?)
            return True

        list_of_assignments = []
        for variable_name in assignment:
            pos = self.get_variable_pos(variable_name)
            var_value = assignment[variable_name]
            if pos != -1 and var_value is not None:
                for possible_assignment in self.possible_values:
                    if possible_assignment[pos] == var_value:
                        list_of_assignments.append(possible_assignment)

        for possible_assignment in list_of_assignments:
            counter = 0
            for variable_name in assignment:
                pos = self.get_variable_pos(variable_name)
                if pos != -1 and assignment[variable_name] is not None:
                    if assignment[variable_name] == possible_assignment[pos]:
                        counter += 1
                else:
                    counter += 1
            if counter == len(assignment):  # TODO need to test this, not sure about the len - 1 thingy.
                return True
        return False

    # TODO i think this is totally non relevant, and maybe should be removed.
    def is_value_legit(self, variable_name, value):
        """
        checks if the value can be assigned to this variable.
        """
        pos = self.get_variable_pos(variable_name)
        if pos != -1:
            for possible_values in self.possible_values:
                if possible_values[pos] == value:  # needs at least one possible value for this to be a legit one.
                    return True
            return False
        return True  # this constraint doesn't care..

    def get_variable_pos(self, var_name):
        return self.variables.index(var_name)

    def get_variables(self):
        return self.variables

    def get_possible_values(self):
        return self.possible_values
