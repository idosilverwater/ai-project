from Constraint import *


class Constraints:
    """
    This class is generating the soft and hard constrains according to the
    parser's output.
    """

    def __init__(self, preferences, variable_names):
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
            if name.endswith(str(day) + " " + str(shift_number)):
                relevant_vars.append(name)
        return tuple(relevant_vars)

    def __generate_hard_const(self):
        """
        Generates the hard constraints and updates self.constraints.
        For now the only hard constraint is: "There should be a least one worker
        in each shift."
        """
        # Creates a variable list that is relevant to a certain shift:
        # TODO(Noy): Find a better way to do it.
        for i in range(7):  # For each day
            for j in range(3):  # For each shift.
                relevant_variables = self. __variable_names_by_shift(i, j)

    def __generate_soft_const(self):
        """
        Generates the soft constraints and updates self.constraints.
        """
        for preference in self.__preferences:
            var_name = preference
            # Adding constraint to all_constraints:
            new_constraint = Constraint(var_name, [(True)], 1)
            self.__all_constraints[(var_name)] = [new_constraint]

    def __set_constraint_by_var(self):
        pass

    #####################
    # Getters & Setters #
    #####################

    def get_visible_constraints(self):
        pass

    def get_all_constraints(self):
        return self.__all_constraints

    def set_visible_constrains(self):
        pass

    def get_constraints_by_variable(self, variable_name):
        return self.__constraints_by_var[variable_name]


#########
# Tests #
#########
p = [(1, 2, 3), (4, 5, 6)]
vars = [(1, 2, 3), (4, 5, 6)]

c = Constraints(p, vars)
print(c.get_all_constraints())
