import magicNums


class FormulaTree:
    """
    Generates and maneges a tree representing a boolean formula.
    """

    def __init__(self, constraints):
        """
        :param constraints: A list of constraints objects.
        Creates a new tree object.
        """
        self.__constraints = constraints
        self.__literals_by_variable_name = {}
        self.__root = self.__build_tree()

    ###################
    # Private Methods #
    ###################

    def __build_sub_tree_of_constraint(self, constraint):
        """
        This method builds a sub tree representing a single constraint. A constraint is of the form:
        "possible_assignment 1 | possible_assignment 2| .....| possible_assignment n
        :return: A pointer to this tree.
        """
        possible_assinment = constraint.get_possible_values()
        variable_names = constraint.get_variables()

    def __generate_literals_for_assignment(self, variable_names, assignment):
        """
        Generates a list of literal objects for a possible assignment.
        :param variable_names: The names of the variables related to the literals
        :param assignment: ?
        :return: a list of literal objects: [literal1, literal2,.....,literal300]
        """
        pass

    def __build_sub_tree_of_possible_assignment(self, assignment, variable_names):
        """
        This method builds a sub tree represents a possible assignment. A possible assignment is of the form:
        literal1 & literal2 & literal 3 &.....& literal k
        :return: A pointer to this tree.
        """
        literals = self.__generate_literals_for_assignment(variable_names, assignment)

    def __build_tree(self):
        """
        Builds a tree representing a formula
        :return: A pointer to the root of the tree.
        """
        clauses = []
        for constraint in self.__constraints:
            clauses.append(self.__build_sub_tree_of_constraint(constraint))

    ##################
    # Public Methods #
    ##################

    def get_root(self):
        return self.__root

    def get_literals_related_to_var(self, variable_name):
        """
        Gets a list of literal object relating to variable name.
        :param variable_name: A string which is a variable name.
        :return: A list of literal objects
        """
        return self.__literals_by_variable_name[variable_name]

    ###############
    # Sub Classes #
    ###############

    class Node():
        """
        Inner class, only to use *inside* of this class.
        """

        def __init__(self, left, right, value=None, is_leaf=False):
            self.left = left
            self.right = right
            self.value = value
            self.is_leaf = is_leaf

    class Literal:
        """
        Literal class, represents a literal in a CNF clause.
        """

        def __init__(self, variable_name_associated_with, is_negated):
            self.assignment_value = None  # the value we will assign to the variable.
            self.literal_value = None  # the value we check when we want to see if a formula is satisfied.
            self.var_name = variable_name_associated_with  # the var name this literal is tied to.
            self.is_negated = is_negated  # is this literal negated.

        def assign_value(self, assignment_value):
            """
            USED BY WALK-SAT ONLY.
            assigns a value, should be used only when we wish to start using the literal.
            :param assignment_value: one of the domain False or domain true values.
            """
            # TODO delete assertion when we are done testing.
            assert (assignment_value == magicNums.DOMAIN_TRUE_VAL or assignment_value == magicNums.DOMAIN_FALSE_VAL)
            self.assignment_value = assignment_value
            if self.is_negated:
                if self.assignment_value == magicNums.DOMAIN_TRUE_VAL:
                    self.literal_value = magicNums.DOMAIN_FALSE_VAL
                else:
                    self.literal_value = magicNums.DOMAIN_TRUE_VAL
            else:
                self.literal_value = assignment_value

        def value(self):
            """
            checks whether this literal is True or False after negation too.
            """
            return self.literal_value == magicNums.DOMAIN_TRUE_VAL

        def flip_self(self):
            """
            Flips the value of this literal.
            :return:
            """
            if self.assignment_value == magicNums.DOMAIN_TRUE_VAL:
                self.assignment_value(magicNums.DOMAIN_FALSE_VAL)
            else:
                self.assignment_value(magicNums.DOMAIN_FALSE_VAL)
