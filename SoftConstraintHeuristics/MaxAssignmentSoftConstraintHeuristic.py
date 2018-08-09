from SoftConstraintHeuristics.BaseSoftConstraintHeuristic import *


class MaxAssignmentSoftConstraintHeuristic(BaseSoftConstraintsHeuristic):
    """
    Soft heuristic constraint that chooses based on the amount of possible assignment a constraint posses:
            if it has many we will choose it first.
    """

    def __init__(self, hard_constraints, soft_constraints):
        """
        :param hard_constraints: a list of hard constraints
        :param soft_constraints: a list of soft constraints
        """
        super(MaxAssignmentSoftConstraintHeuristic, self).__init__(hard_constraints, soft_constraints)

    def constraint_level(self, soft_constraint):
        return soft_constraint.is_soft, len(soft_constraint.get_possible_values())
