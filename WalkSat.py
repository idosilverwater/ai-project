from Solver import Solver
import random

"""
Literal inner class. // contains: assignment_value, var_name that it is tied too, isNot - is this literal has a
                not over it, formula_val - determined by assignment with isNot.
                function: flip_self()  # J is doing
TreeNode: left, right, value, is_leaf. //  value = literal object or AND_VAL = 'And' or OR_VAL = 'or'.  means leaf, 
                                            or type of operation. # N is doing
                                             
TreeBuilder -> Contains TreeNodes, and constraints.  using constraints will build a tree of clauses.
            __build_sub_tree_of_clause - build one tree for a single clause given. (returns a tree node of clauses)
            __build_constraint_sub_claus()
            build_tree() -> concat every clause by an and node. return tree.  # N is doing

CnfConverter(Tree) returns list of lists. [(This is and between the lists)[(this is or between the lists)l1,l2,l3],...
                                                        [l4,l2,1]and[not()]...[...]] = Formula # N is doing
evaluator(Formula) // given formula we know every litteral and we should check the fricken values of it.
WalkSat:
    attributes: 
        TreeBuilder
        dict_of_var_name -> [literals list]
    funcs:
        flip_literal(literal) // should know how to flip all related literals. (using  dict_of_var_name)
        choose_clause_randomly(list_of_clauses)
        cnfConverter() -> converts the result of build_tree(), using formula to cnf algorithm.
        walksat() -> runs walkSat over the formula given by cnfConverter.
        choose_which_literal_to_flip() // done greedily.  # J is doing
"""


class WalkSat(Solver):
    """
    a Walksat based solver for csp problems.
    """

    def __init__(self, csp, random_value=0.5, max_flips=1000):
        """
        excepts a csp problem initialized.
        """
        super(WalkSat, self).__init__(csp)
        self.csp.make_visible()
        self.__p = random_value
        self.__variable_names = list(self.csp.variables)  # a list of all names.
        self.__max_flips = max_flips

    def __flip_coin(self):
        r = random.random()
        return r < self.__p

    def set_max_flips(self, max_flips):
        self.__max_flips = max_flips

    def __choose_random_variable(self):
        position = random.randint(self.__variable_names)
        return self.__variable_names[position]

    def is_satisfied(self):
        """
        checks if model is satisfied, which means it checks the assignment over the csp result.
        :return: True or False
        """
        for name in self.__variable_names:
            if not self.csp.variables[name].is_satisfied():
                return False
        return True

    def __flip_value(self, variable_name):
        """ assign the opposite value."""
        new_val = not self.assignment[variable_name]
        self.remove_value(variable_name)
        self.assign_value(variable_name, new_val)

    def __greedy_walksat(self):
        """
        Should choose a variable and a value to assign to it. such that it minimises the amount of
        :return:
        """
        pass  # TODO

    def random_assignment(self):
        """
        Tries to put random assignment, if there is no possible assignment returns false.
        :return:
        """
        for name in self.__variable_names:
            self.assign_value(name, self.__flip_coin())

    def solve(self):
        """
        tries and solve for the csp problem while adding more and more constraints to the problem.
        :return: False if there isn't a solution, True otherwise.
        """
        self.random_assignment()
        for i in range(self.__max_flips):
            if self.is_satisfied():
                return True
            if self.__flip_coin():
                variable_name = self.__choose_random_variable()
                self.__flip_value(variable_name)
            else:
                self.__greedy_walksat()
        return False
