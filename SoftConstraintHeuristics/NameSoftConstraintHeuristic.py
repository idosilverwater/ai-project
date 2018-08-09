from SoftConstraintHeuristics.BaseSoftConstraintHeuristic import *
from functools import partial


class NameSoftConstraintHeuristic(BaseSoftConstraintsHeuristic):
    """
    counts the number of variables. and returns the soft constraint which holds the least amount of variables.
    """

    def __init__(self, hard_constraints, soft_constraints):
        """
        :param hard_constraints: a list of hard constraints
        :param soft_constraints: a list of soft constraints
        """
        super(NameSoftConstraintHeuristic, self).__init__(hard_constraints, soft_constraints)

    def constraint_level(self, soft_constraint):
        """
        Constraint in this case is a variable (ex. "David 1 1") which says that david wants the second shift on monday
        :param cosntraint: constraint
        :return:
        """
        return soft_constraint.is_soft, len(soft_constraint.get_variables())
