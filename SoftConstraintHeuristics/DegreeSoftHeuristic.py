from SoftConstraintHeuristics.BaseSoftConstraintHeuristic import *


class DegreeSoftConstraintsHeuristic(BaseSoftConstraintsHeuristic):
    """
    Counts the number of hard constraints neighbours this soft heuristic has and returns the
        one with the least neighbours.
    """

    def __init__(self, hard_constraints, soft_constraints):
        """
        :param hard_constraints: a list of hard constraints
        :param soft_constraints: a list of soft constraints
        """
        super(DegreeSoftConstraintsHeuristic, self).__init__(hard_constraints, soft_constraints)

    def constraint_level(self, soft_constraint):
        """
        Constraint in this case is a variable (ex. "David 1 1") which says that david wants the second shift on monday
        :param cosntraint: constraint
        :return:
        """
        count = 1

        for hard in self.hard_constraints:
            for variable in soft_constraint.get_variables():
                if variable in hard.get_variables():
                    count += 1

        return soft_constraint.is_soft, count
