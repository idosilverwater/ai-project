from Solver import Solver
import random
from FormulaTree import *
import numpy as np
import magicNums

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
        accepts a csp problem initialized.
        """
        super(WalkSat, self).__init__(csp)
        self.csp.make_visible()
        self.__p = random_value
        self.__variable_names = list(self.csp.variables)  # a list of all names.
        self.__max_flips = max_flips
        self.__formula_tree = FormulaTree(csp.constraints.get_all_constraints())

        self.assignment = dict()
        print('what')
        self.clauses = self.cnfConverter()
        print('when')


    def __flip_coin(self):
        """
        Return True with probability __p otherwise False.
        :return:
        """
        r = random.random()
        return r < self.__p

    def set_max_flips(self, max_flips):
        self.__max_flips = max_flips

    def __choose_random_variable(self, clause):
        """
        Choose random variable from clause.
        :param clause:
        :return:
        """
        literal = random.choice(clause)
        return literal.var_name

    def __flip_random_variable(self, clause):
        """
        Flip random variable from clause
        :param clause:
        :return:
        """

        variable = self.__choose_random_variable(clause)
        self.__flip_value(variable)

    def is_satisfied(self):
        """
        checks if model is satisfied, which means it checks the assignment over the csp result.
        :return: True or False
        """

        for clause in self.clauses:
            flag = False
            for literal in clause:
                if literal.value:
                    flag = True
                    break
            if not flag:
                return False

        return True

    def __flip_value(self, variable_name):
        """
        Flip the value (True to False and False to True) of the variable named variable_name
        :param variable_name:
        :return:
        """
        new_val = not self.assignment[variable_name]
        # self.remove_value(variable_name) #TODO ask if this has to be thrown out...
        self.assign_value(variable_name, new_val)


    def random_assignment(self):
        """
        Randomly assign each variable a value (either True or False).
        :return:
        """
        for name in self.__variable_names:
            self.assign_value(name, self.__flip_coin())

    def assign_value(self, variable_name, value):
        """
        Assign the value (value) to all literals of the variable named variable_name.
        :param variable_name:
        :param value:
        :return:
        """
        self.assignment[variable_name] = value
        for literal in self.__formula_tree.get_literals_related_to_var(variable_name):
            literal.assign_value(value)

    def cnfConverter(self):
        """
        :return: Convert the Formula tree (which represents a CSP problem) to CNF form.
        """
        rec = self.recursiveCNFConverter(self.__formula_tree.get_root(), 0)
        print("finished conversion")
        return rec

    def recursiveCNFConverter(self, node, i):
        """
        Given tree that represents a csp problem. (a csp with literals and *only* AND and OR operators)
        convert to cnf form. according to the algorithm presented at: http://cs.jhu.edu/~jason/tutorials/convert-to-CNF
        :param node:
        :return:
        """
        if node.is_leaf:
            return {(node.value,)} # returning a set

        right = self.recursiveCNFConverter(node.right, i + 1)
        left = self.recursiveCNFConverter(node.left, i + 1)

        print(i)

        if node.value == AND:
            return left.union(right)
        if node.value == OR:
            new = set()
            for p in left:
                for q in right:
                    new.add(p + q)
            return new

    def random_clause(self):
        """
        :return: return uniformly picked clause
        """
        return random.choice(self.clauses)

    def __flip_most_satisfying(self):
        """
        Flip the variable who's flipping will satisfy the most clauses
        """
        variable_name = self.__most_satisfying()
        self.__flip_value(variable_name)

    def __most_satisfying(self):
        """
        :return: the variable who's flipping will satisfy the most clauses.
        """

        max_var = self.__variable_names[0]
        max_num = self.__num_satisfied(max_var)

        for variable_name in self.__variable_names:
            cur = self.__num_satisfied(variable_name)
            if  cur > max_num:
                max_num = cur
                max_var = variable_name

        return max_var

    def __num_satisfied(self, variable_name):
        """
        Checks how much clauses are satisfied after flipping this variables value.
        :param variable_name: the variable to flip.
        :return: the amount of satisfied clauses after flipping.
        """
        self.__flip_value(variable_name)

        count = 0

        for clause in self.clauses:
            flag = False
            for literal in clause:
                if literal.value:
                    flag = True
                    break
            if flag:
                count += 1

        self.__flip_value(variable_name) # flip back

        return count

    def solve(self):
        """
        The WalkSAT algorithm

        :return: dictionary of assignments (of the form {varName: val})
        """

        self.random_assignment()
        if self.is_satisfied():
            return self.assignment
        else:
            for i in range(self.__max_flips):
                clause = self.random_clause()
                if self.__flip_coin():
                    self.__flip_random_variable(clause)
                else:
                    self.__flip_most_satisfying()

