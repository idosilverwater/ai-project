class Constraint:
    """
    Constraint is a tuple of the form: ((v_1, v_2,..., v_n), possible values)
    (v_1, v_2,..., v_n)  are variables.
    """

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

    def is_value_legit(self, variable_name, value):
        pass  # TODO should make it's checks if the value is okay with this

    def get_variables(self):
        return self.variables

    def get_possible_values(self):
        return self.possible_values
