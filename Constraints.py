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
        self.__constraints_by_var = {}  # (var name): [constrains on var]
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

    def __generate_hard_const(self):
        """
        Generates the hard constraints and updates self.constraints.
        """
        pass

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


#########
# Tests #
#########
p = [(1, 2, 3), (4, 5, 6)]
vars = [(1, 2, 3), (4, 5, 6)]

c = Constraints(p, vars)
print(c.get_all_constraints())
