from DomainHeuristic import DomainHeuristic
from functools import partial
from magicNums import *


# TODO THIS IS BUG RIDDEN> Please fix this classes.
class LeastConstrainingValue(DomainHeuristic):


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

    def __constraint_score(self, variable, value, current_assignment):
        """
        Return the constraint score this value gets.
        The constraint score is the amount of possible remaining assignments.
        :param value: The tested value
        :param remaining_assignments: dictionary of constraints as keys and the possible remaining assignments
        :return:
        """

        # variable_possibilities = dict()

        current_assignment[variable.get_name()] = value
        constraints = variable.get_constraints()

        score = 0
        for constraint in constraints:
                score += constraint.get_number_of_constraints(current_assignment)

        return score



        #         if var not in variable_possibilities:  # at the beggining a var has all possibilies
        #             variable_possibilities[var] = variable.get_possible_domain()
        #         elif len(variable_possibilities[var]) == 0:  # we already ruled true and false out then continue
        #             continue
        #
        #         # Flags to check if in the assignment for the current constraint, there is an assignment with true/false
        #         # for this var
        #         true_flag = False
        #         false_flag = False
        #
        #         for assignment in remaining_assignments[constraint]:
        #             # if in this assignment variable isn't the value then it's not a possibility to start with.
        #             if constraint.get_variable_pos(variable.get_name()) != value:
        #                 continue
        #
        #             if assignment[constraint.get_variable_pos(var)] == DOMAIN_TRUE_VAL:  # Found True
        #                 true_flag = True
        #             if assignment[constraint.get_variable_pos(var)] == DOMAIN_FALSE_VAL:  # Found False
        #                 false_flag = True
        #
        #         # No assignment with True/False has been found thus this constraint can't be assigned by it
        #         # therefore the current variable var, doesn't have this value in it's possibilities.
        #         if not true_flag:
        #             variable_possibilities[var].remove(DOMAIN_TRUE_VAL)
        #         if not false_flag:
        #             variable_possibilities[var].remove(DOMAIN_FALSE_VAL)
        #
        #
        # for constraint in remaining_assignments:
        #     for var in constraint.get_variables():
        #         score += len(variable_possibilities[var])
        #
        # return score

    def sort_by_second(self, t):
        return - t[1] # The minus is on purpuse. we want the largest first.

    # TODO THIS isn't documented good enough, i have no idea which constraint to give you, furthermore one var have
    #                                                                                            many constraints.
    def get_value(self, variable, current_assignment):
        """
        Selects the value for the variable that is least constricting to neighboring variables.
        :param variable: the variable that needs assignment
        :param current_assignment: The current assignment.(This is needed in order to know what possible assignments are
        no longer relevant)
        :return: variable's assignment that is least constricting to it's neighboring variables.
        """

        constraints = variable.get_constraints()

        remaining_assignments = dict()
        for constraint in constraints:
            # get_remaining_constraints returns the remaining possible assignments that satisfy the constraint.
            remaining_assignments[constraint] = constraint.collect_possible_assignments(current_assignment)

        l = list()

        for value in variable.get_possible_domain():
            cur = self.__constraint_score(variable, value, remaining_assignments)
            l.append((value, cur))

        l.sort(key=self.sort_by_second)
        return [*map(lambda x: x[0], l)]
