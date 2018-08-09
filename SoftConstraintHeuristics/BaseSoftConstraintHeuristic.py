from functools import partial


class BaseSoftConstraintsHeuristic:

    def __init__(self, hard_constraints, soft_constraints):
        """
        :param hard_constraints: a list of hard constraints
        :param soft_constraints: a list of soft constraints
        """
        self.hard_constraints = hard_constraints
        self.soft_constraints = soft_constraints

    def constraint_level(self, soft_constraint):
        """
        Constraint in this case is a variable (ex. "David 1 1") which says that david wants the second shift on monday
        :param cosntraint: constraint
        :return:
        """
        pass  # TODO implement in deriving classes.

    def get_adding_order(self):
        """
        Return order of constraint addition, first according to softness level (the lower the better)
        Second, according to the least amount of least conflict.
        :return:
        """

        # It's ok that it is ordering in ascending order, since the less constraint_level the better
        self.soft_constraints.sort(key=self.constraint_level)
        return self.soft_constraints
