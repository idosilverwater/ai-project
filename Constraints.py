from Constraint import *


class Constraints:
    """
    This class is generating the soft and hard constrains according to the
    parser's output.
    """

    def __init__(self, preferences, variable_names, constraint_heuristic=None):
        """
        Creates several dictionaries of constraints.
        :param preferences: A list of the workers preferences. For example:
         [(1,2,3)] is a list with one preference: worker1 wants to work on
         shift 3 on Tuesday.
        :param variable_names: A list of variables names. A variable name for
        example would be "(1,2,3)"
        """
        self.__preferences = preferences
        self.__variable_names = variable_names
        self.__constraint_heuristic = constraint_heuristic
        self.__all_constraints = {}  # (Variable names): [constraints on variables]
        self.__visible_constraints = {}  # (Variable names): [constraints on variables]
        self.__constraints_by_var = {}  # var name: [constrains on var]
        self.__build_all_constraints()

    ###################
    # Private Methods #
    ###################

    def __build_all_constraints(self):
        """
        Generates all of the constraints.
        """
        self.__generate_hard_const()
        self.__generate_soft_const()

    def __variable_names_by_shift(self, day, shift_number):
        """
        This function generates a tuple of variable names that are relevant for
        a certain shift.
        :param: day: For example: 3
        :param: shift: For example: 2
        ============
        For Example:
        ============
        1) A variable name that is relevant to the first shift on Sunday is:
        (5,1,1).
        2) A variable name that is not relevant is: (5,2,3)
        :return: A tuple of variable names
        """
        relevant_vars = []
        for name in self.__variable_names:
            if name.endswith(str(day) + ", " + str(shift_number) + ")"):
                relevant_vars.append(name)
        return tuple(relevant_vars)

    def __one_worker_helper(self, number_of_workers, curr, result_lst,
                            current_list):
        if number_of_workers == curr:
            result_lst.append(current_list)
        else:
            self.__one_worker_helper(number_of_workers, curr + 1, result_lst,
                                     current_list + [True])
            self.__one_worker_helper(number_of_workers, curr + 1, result_lst,
                                     current_list + [False])

    def __generate_assignments_for_at_least_one_worker(self,
                                                       number_of_workers):
        """
        This method generates assignments with respect to the hard constraint:
        "There should be at least one worker in a shift"
        :param: number_of_workers: The number of workers.
        :return: A list of possible assignments.
        For Example(three workers): [[True,True,False],[False,True,False]]
        """
        lst = []
        self.__one_worker_helper(number_of_workers, 0, lst, [])
        lst.pop()
        return lst

    def __generate_hard_const(self):
        """
        Generates the hard constraints and updates self.constraints.
        For now the only hard constraint is: "There should be a least one worker
        in each shift."
        """
        # Creates a variable list that is relevant to a certain shift:
        for i in range(7):  # For each day
            for j in range(3):  # For each shift.
                relevant_variables = self.__variable_names_by_shift(i, j)
                possible_assignments = self.__generate_assignments_for_at_least_one_worker(
                    len(relevant_variables))
                new_constraint = Constraint(relevant_variables,
                                            possible_assignments, 0)
                self.__all_constraints[relevant_variables] = new_constraint

    def __generate_soft_const(self):
        """
        Generates the soft constraints and updates self.constraints.
        """
        for preference in self.__preferences:
            var_name = str(preference)
            # Adding constraint to all_constraints:
            new_constraint = Constraint(var_name, [[True]], 1)
            self.__all_constraints[var_name] = [new_constraint]

    def __set_constraint_by_var(self):
        pass

    #####################
    # Getters & Setters #
    #####################

    def get_visible_constraints(self):
        pass

    def get_all_constraints(self):
        return self.__all_constraints

    def make_visible_for_walksat(self):
        self.__visible_constraints = self.__all_constraints

    def update_visible(self):
        variables, constraint = self.__constraint_heuristic(
            self.__visible_constraints, self.__all_constraints)
        self.__visible_constraints[variables] = constraint

    def get_constraints_by_variable(self, variable_name):
        return self.__constraints_by_var[variable_name]


#########
# Tests #
#########
# p = ["(1, 2, 2)", "(4, 5, 1)"]
# vars = ["(1, 2, 2)", "(2, 2, 2)", "(4, 5, 1)"]
# h = None
# c = Constraints(p, vars, h)
# print(c.get_all_constraints())
