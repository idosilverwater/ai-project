from SoftConstraintHeuristics.BaseSoftConstraintHeuristic import *
import random


class RandomSoftHeuristic(BaseSoftConstraintsHeuristic):
    """
    Returns a random order.
    """

    def __init__(self, hard_constraints, soft_constraints):
        """
        :param hard_constraints: a list of hard constraints
        :param soft_constraints: a list of soft constraints
        """
        super(RandomSoftHeuristic, self).__init__(hard_constraints, soft_constraints)

    def get_adding_order(self):
        """
        Return order of constraint addition, first according to softness level (the lower the better)
        Second, according to the least amount of least conflict.
        :return:
        """
        # It's ok that it is ordering in ascending order, since the less constraint_level the better
        random.shuffle(self.soft_constraints)
        return self.soft_constraints
