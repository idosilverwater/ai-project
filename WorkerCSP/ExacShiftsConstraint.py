from CSP import Constraint
import magicNums


class ExacShiftsConstraints(Constraint.Constraint):
    """
    A special type of soft constraint relevant to a specific problem Worker-Employee problem.
        Helps find if the assignment have an exact amount of shifts for a specific worker.

    """

    def __init__(self, variables, possible_values, softness=magicNums.VARIABLE_NAME_SHIFT_SEPARATOR):
        super(ExacShiftsConstraints, self).__init__(variables, possible_values, softness)
        self.num_for_okay = possible_values[0].count(magicNums.DOMAIN_TRUE_VAL)
        self.__special_name_check = self.variables[0].split(magicNums.VARIABLE_NAME_SHIFT_SEPARATOR)[0]

    def __get_counters(self, assignment):
        counter = 0
        none_counter = 0
        for var_name in assignment:
            if var_name.split(magicNums.VARIABLE_NAME_SHIFT_SEPARATOR)[0] == self.__special_name_check:
                if assignment[var_name] == magicNums.DOMAIN_TRUE_VAL:
                    counter += 1
                elif assignment[var_name] is None:
                    none_counter += 1
        return counter, none_counter

    def check_assignment(self, assignment):
        """
        Checks if an assignment is legit or isn't.
        :param assignment:
        :return:
        """
        none_counter = self.check_num_of_nones(assignment)
        if none_counter == len(self.variables):
            return True

        counter, none_counter = self.__get_counters(assignment)

        if counter == self.num_for_okay:
            return True
        elif none_counter >= 1:
            return True
        else:
            return False
