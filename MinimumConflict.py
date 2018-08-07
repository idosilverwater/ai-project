import DomainHeuristic
from functools import  partial

class MinimumConflict(DomainHeuristic):

    def neighbor_conflict(self, value, variable, current_assignment, constraint):
        """
        This returns the amount of domain values that have been blocked off for the neighboring variables.
        :return:
        """

        variable_name = variable.get_name()
        variable_pos = variable.constraint.get_variable_pos(variable_name)
        current_assignment[variable_pos] = value

        return self.constraint.get_number_of_constraints(current_assignment)

    def get_value(self, variable, current_assignment, constraint):
        """
        Selects a value out of variable's domain, that dissatisfies the least amount of constraints
        (that variable is a part of).
        :param variable: The variable we want to assign a value to.
        :return: A value for variable according to the heuristic
        """
        order = self.variable.get_domain()
        return order.sort(key=partial(self.neighbor_conflict, variable=variable, current_assignment=current_assignment,
                                      constraint=constraint)) # TODO does this sort needs to be reversed?


def minimum_conflict_heuristic_factory(variables, constraints):
    return MinimumConflict(variables, constraints)
