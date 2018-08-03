###########
# Imports #
###########
import magicNums

#############
# Constants #
#############
AND = magicNums.AND
OR = magicNums.OR


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

    def __concatenate(self, nodes, operation):
        """
        This method builds a  binary tree such that "nodes" are the leafs, and the ancestors are nodes that have the
        value "operation".
        :param nodes: A list of nodes to bi concatenated.
        :param operation: Either "And" or "Or"
        :return: a pointer to the tree.
        """
        if len(nodes) < 1:
            raise ValueError("nodes is empty")

        curr_root = nodes[0]
        for i in range(len(nodes) - 1):
            curr_root = self.Node(curr_root, nodes[i + 1], operation, False)

        return curr_root

    def __create_nodes_from_literals(self, literals):
        """
        This method generates a list of nodes out of a list of literals.
        :param literals: A list of literal objects.
        :return: A list of nodes corresponding to the list of literals.
        """
        nodes = []
        for literal in literals:
            new_node = self.Node(None, None, literal, True)
            nodes.append(new_node)
        return nodes

    def __add_to_dictionary(self, literal, variable_name):
        """
        Adds literal to self.__literals_by_variable_name
        :param literal: a literal object
        :param variable_name: A variable name
        """
        if variable_name not in self.__literals_by_variable_name:
            self.__literals_by_variable_name[variable_name] = [literal]
        else:
            self.__literals_by_variable_name[variable_name] += [literal]

    def __generate_literals_for_assignment(self, variable_names, assignment):
        """
        Generates a list of literal objects for a possible assignment.
        :param variable_names: The names of the variables related to the literals
        :param assignment: A tuple containing "magicNums.DOMAIN_FALSE_VAL" or "magicNums.DOMAIN_TRUE_VAL"
        :return: a list of literal objects: [literal1, literal2,.....,literal300]
        """
        literals = []
        is_negated = False

        for i, variable in enumerate(variable_names):
            if assignment[i] == magicNums.DOMAIN_FALSE_VAL:
                is_negated = True
            literal = self.Literal(variable, is_negated)
            literals.append(literal)
            self.__add_to_dictionary(literal, variable)
            is_negated = False
        return literals

    def __build_sub_tree_of_possible_assignment(self, assignment, variable_names):
        """
        This method builds a sub tree represents a possible assignment. A possible assignment is of the form:
        literal1 & literal2 & literal 3 &.....& literal k
        :return: A pointer to this tree.
        """
        literals = self.__generate_literals_for_assignment(variable_names, assignment)
        literal_nodes = self.__create_nodes_from_literals(literals)

        curr_root = self.__concatenate(literal_nodes, AND)

        return curr_root

    def __build_sub_tree_of_constraint(self, constraint):
        """
        This method builds a sub tree representing a single constraint. A constraint is of the form:
        "possible_assignment 1 | possible_assignment 2| .....| possible_assignment n
        :return: A pointer to this tree.
        """
        possible_assignments = constraint.get_possible_values()
        variable_names = constraint.get_variables()
        roots_of_assignment_trees = []

        for assignment in possible_assignments:
            root_of_assignment = self.__build_sub_tree_of_possible_assignment(assignment, variable_names)
            roots_of_assignment_trees.append(root_of_assignment)

        curr_root = self.__concatenate(roots_of_assignment_trees, OR)
        return curr_root

    def __build_tree(self):
        """
        Builds a tree representing a formula. Formula is of the form: clause1 & clause2 & .... & clause m.
        """
        clauses = []
        for key in self.__constraints:
            for constraint in self.__constraints[key]:
                clauses.append(self.__build_sub_tree_of_constraint(constraint))

        return self.__concatenate(clauses, AND)

    @staticmethod
    def __print_tree(tree_node, lst):
        if tree_node is None:
            return
        FormulaTree.__print_tree(tree_node.left, lst)
        lst.append(tree_node.value)
        FormulaTree.__print_tree(tree_node.right, lst)

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

    def print_self(self):
        lst = []
        self.__print_tree(self.__root, lst)
        print(self.__root.value)
        print(lst)

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

        def __repr__(self):
            if self.is_negated:
                return "not(" + str(self.var_name) + ")"
            return self.var_name
#########
# Tests #
#########
# from Constraint import *
#
# constraints = {}
# c2 = Constraint(["(vividish 1 0)", "(vividisha 0, 0)"], [(magicNums.DOMAIN_FALSE_VAL, magicNums.DOMAIN_TRUE_VAL), (magicNums.DOMAIN_FALSE_VAL, magicNums.DOMAIN_FALSE_VAL)], 1)
# c1 = Constraint(["(vividish 1 1)"], [(magicNums.DOMAIN_FALSE_VAL,), (magicNums.DOMAIN_TRUE_VAL,)], 1)
# constraints[("(vividish 1 0)", "(vividisha 0, 0)")] = [c2]
# constraints[("(vividish 1 1)")] = [c1]
# tree = FormulaTree(constraints)
# tree.print_self()
