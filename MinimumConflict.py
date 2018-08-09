from DomainHeuristic import *
from functools import partial


class MinimumConflict(DomainHeuristic):

    def __get_conflict_score(self, variable, value, current_assignment):
        """
        The conflict score of the value.
        Returns the amount of constraints that are not satisfiable with the assignment of value to variable.
        The lower the better
        :param value:
        :return:
        """

        current_assignment[variable.get_name()] = value
        constraints = variable.get_constraints()

        score = 0
        for constraint in constraints:
            if constraint.get_number_of_constraints(current_assignment) == 0:
                score += 1

        return score

    # def sort_by_second(self, t):
    #     return t[1]

    def get_value(self, variable, current_assignment):
        """
        Selects a value out of the variable's domain, that dissatisfies the least amount of constraints (that contain
        the variable).
        :param variable: The tested variable
        :param current_assignment: Current assignment of the variables.
        :return: The value that creates minimum conflict with constraints.
        """

        # min_conflict_value = variable.get_possible_domain()[0]
        # min_conflict_score = self.__get_conflict_score(variable, min_conflict_value, current_assignment)
        #
        # for value in variable.get_possible_domain():
        #     cur = self.__get_conflict_score(variable, value, current_assignment)
        #     if cur < min_conflict_score:
        #         min_conflict_score = cur
        #         min_conflict_value = value
        #
        # return min_conflict_value

        domain_and_score_list = list()

        for value in variable.get_possible_domain():
            cur = self.__get_conflict_score(variable, value, current_assignment)
            domain_and_score_list.append((value, cur))

        domain_and_score_list.sort(key=lambda t: t[1])

        return [*map(lambda x: x[0], domain_and_score_list)]  # TODO Ask ido if this is what is wanted to be returned.
