class SoftConstraintsHeuristic:

    def __init__(self, constraints, constraint):
        """

        :param constraints:
        """
        self.constraints = constraints
        self.constraint = constraint

    def update_constraints(self, constraints):
        self.constraints

    def constraint_level(self, constraint, assignments):
        """
        Constraint in this case is a variable (ex. "David 1 1") which says that david wants the second shift on monday
        :param cosntraint: constraint
        :return:
        """

        pos = self.constraint.get_variable_pos(constraint)

        count = 1

        for assignment in assignments:
            if assignment[pos] == False:
                count += 1

        return count

    def get_order_domain(self, remaining_constraints):
        """
        Selects a value out of variable's domain, that dissatisfies the least amount of constraints
        (that variable is a part of).

        remaining_constraints is the remaining possible assignments after the hard constraints.

        :param variable: The variable we want to assign a value to.
        :return: A value for variable according to the heuristic
        """

        # It's ok that it is ordering in ascending order, since the less constraint_level the better
        return self.constraints.sort(key=partial(self.constraint_level, assignments = remaining_constraints))
