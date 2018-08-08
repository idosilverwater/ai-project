from functools import partial


class SoftConstraintsHeuristic:

    def __init__(self, soft_constraints):
        """
        :param soft_constraints:
        """
        self.soft_constraints = soft_constraints

    def update_constraints(self, soft_constraints):
        self.soft_constraints = soft_constraints

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

        return constraint.is_soft, count

    def get_adding_order(self, remaining_assignments):
        """
        Return order of constraint addition, first according to softness level (the lower the better)
        Second, according to the least amount of least conflict.
        :return:
        """

        # It's ok that it is ordering in ascending order, since the less constraint_level the better
        return self.soft_constraints.sort(key=partial(self.constraint_level, assignments=remaining_assignments))

