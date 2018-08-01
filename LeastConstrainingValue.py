from DomainHeuristic import DomainHeuristic
from functools import partial


class LeastConstrainingValue(DomainHeuristic):

    def get_num_of_possible_domain_for_assignment(self, assignments, variable):
        """
        This method given assignments, checks how many options variable's neighbors have for assignment.
        For example if the possible domain is {True, False}.
        The player could be left with both possibilities, or maybe with only 1.
        :param assignments:
        :param variable:
        :return:
        """
        d = dict()

        # We check only for the neighbors (the variable doesn't affect variables that are not in any constraints with
        #  them)
        for key in variable.get_neighbors():
            d[key] = set()

        for assignment in assignments:
            for key in variable.get_neighbors():
                d[key].add(assignment[d])

        for key in d:
            d[key] = len(d[key])

        return d

    def neighbor_conflict(self, value, variable, variable_pos, current_assignment, amounts1):
        """
        This returns the amount of domain values that have been blocked off for the neighboring variables.
        :return:
        """

        current_assignment[variable_pos] = value

        remaining_assignments2 = set(self.constraint.get_remaining_constraints(current_assignment))
        amounts2 = self.get_num_of_possible_domain_for_assignment(remaining_assignments2, variable)

        sum = 0
        for key in amounts1:
            sum += amounts1[key] - amounts2[key]

        return sum

    def get_order_domain(self, variable, current_assignment, constraint):
        """
        Selects the value for variable, that is least constricting to variables neighbors.
        neighbors being other variables that share at least one constraint with it.
        :param current_assignment: the current assignment
        :param variable: The variable we want to assign a value to.
        :return: A value for variable according to the heuristic
        """

        remaining_assignments1 = set(self.constraint.get_remaining_constraints(current_assignment))
        amounts1 = self.get_num_of_possible_domain_for_assignment(remaining_assignments1)

        variable_name = variable.get_name()
        variable_pos = variable.constraint.get_variable_pos(variable_name)

        order = self.variable.get_domain()
        return order.sort(key=partial(self.neighbor_conflict, variable=variable, variable_pos=variable_pos,
                                      current_assignment=current_assignment, amounts1=amounts1))
