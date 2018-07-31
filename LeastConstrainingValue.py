from DomainHeuristic import DomainHeuristic
from functools import partial


class LeastConstrainingValue(DomainHeuristic):

    def get_num_of_possible_domain_for_assignment(self, remaining_assignments):
        d = dict()
        for key in remaining_assignments[0]:
            d[key] = set()
        for assignment in remaining_assignments:
            for key in assignment:
                d[key].add(assignment[d])
        for key in d:
            d[key] = len(d[key])

        return d

    def neighbor_conflict(self, value, variable, current_assignment, constraints):
        """
        This returns the amount of domain values that have been blocked off for the neighboring variables.
        :return:
        """

        remaining_assignments1 = self.constraint.get_remaining_constraints(current_assignment)
        amounts1 = self.get_num_of_possible_domain_for_assignment(remaining_assignments1)

        variable_name = variable.get_name()
        variable_pos = variable.constraint.get_variable_pos(variable_name)
        current_assignment[variable_pos] = value

        remaining_assignments2 = self.constraint.get_remaining_constraints(current_assignment)
        amounts2 = self.get_num_of_possible_domain_for_assignment(remaining_assignments2)

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

        order = self.variable.get_domain()
        return order.sort(key=partial(self.neighbor_conflict, variable=variable, current_assignment=current_assignment,
                                      constraint=constraint))
