class Constraint:
    """
    Constraint is a tuple of the form: ((v_1, v_2,..., v_n), possible values)
    (v_1, v_2,..., v_n)  are variables.
    """

    def __init__(self, variables, possible_values, softness = 1):
        """
        Builds a new constraint object.
        :param variables: a set of variables.
        :param possible_values: a set of sets, each set describes a legal
        assignment to the variables.
        :param softness: 1 if soft constraint, o.w. 0.
        """
        self.variables = None
        self.possible_values = None
        self.is_soft = None
        pass
