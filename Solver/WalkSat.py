from Solver.BaseSolver import *
import random
import magicNums
import time

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


# TODO work with self assignment and not csp. assignment.
class WalkSat(Solver):
    """
    a Walksat based solver for csp problems.
    """

    def __init__(self, csp, random_value=0, max_flips=40):
        """
        accepts a csp problem initialized.
        """
        super(WalkSat, self).__init__(csp)
        self.csp.make_visible()
        self.__p = random_value
        self.__variable_names = list(self.csp.variables)  # a list of all names.
        self.__max_flips = max_flips

        self.constraints = list()
        self.list_of_constraints()
        self.satisfied = {}


    def list_of_constraints(self):  # TODO check this?
        constraints = set()

        for vars in self.csp.constraints.get_all_constraints():
            constraints = constraints.union(self.csp.constraints.get_all_constraints()[vars])

        self.constraints = list(constraints)

    def get_assignment(self):
        return self.assignment

    def __flip_coin(self, prob = None):
        """
        Return True with probability __p otherwise False.
        :return:
        """
        if prob == None:
            prob = self.__p

        r = random.random()
        if r < prob:
            return True
        return False

    def set_max_flips(self, max_flips):
        self.__max_flips = max_flips

    def __choose_random_variable(self, constraint):
        """
        Choose random variable from constraint.
        :param constraint:
        :return:
        """
        return random.choice(constraint.get_variables())

    def __flip_random_variable(self, constraint):
        """
        Flip random variable from clause
        :param clause:
        :return:
        """

        variable = self.__choose_random_variable(constraint)
        self.__flip_value(variable)

    # def is_satisfied(self):
    #     """
    #     checks if model is satisfied, which means it checks the assignment over the csp result.
    #     :return: True or False
    #     """
    #
    #     for clause in self.clauses:
    #         flag = False
    #         for literal in clause:
    #             if literal.value:
    #                 flag = True
    #                 break
    #         if not flag:
    #             return False
    #
    #     return True

    def is_satisfied(self):
        """
        checks if model is satisfied, which means it checks the assignment over the csp result.
        :return: True or False
        """
        return self.csp.check_constraint_agreement(self.constraints, self.assignment)

    def __flip(self, val):
        if val == magicNums.DOMAIN_TRUE_VAL:
            return magicNums.DOMAIN_FALSE_VAL
        return magicNums.DOMAIN_TRUE_VAL

    def __flip_value(self, variable_name):
        """
        Flip the value (True to False and False to True) of the variable named variable_name
        :param variable_name:
        :return:
        """
        old = self.csp.variables[variable_name].get_value()
        self.assign_value(variable_name, self.__flip(old))

    def random_assignment(self):
        """
        Randomly assign each variable a value (either True or False).
        :return:
        """

        def put_flip_coin_val():
            if self.__flip_coin():
                return magicNums.DOMAIN_TRUE_VAL
            return magicNums.DOMAIN_FALSE_VAL

        for name in self.__variable_names:
            self.assign_value(name, put_flip_coin_val())  # TODO Notice i changed it to work with actual domain values.

    def random_constraint(self):
        """
        :return: return uniformly picked clause
        """
        t = time.time()
        constraint = random.choice(self.constraints)
        return constraint

    def __flip_most_satisfying(self):
        """
        Flip the variable who's flipping will satisfy the most clauses
        """
        variable_name = self.__most_satisfying()
        self.__flip_value(variable_name)

        for constraint in self.csp.variables[variable_name].get_constraints():
            if constraint.check_assignment(self.assignment):
                self.satisfied[constraint] = True
            else:
                self.satisfied[constraint] = False


    def __most_satisfying(self):
        """
        :return: the variable who's flipping will satisfy the most clauses.
        """


        max_var = self.__variable_names[0]
        max_num = self.__num_satisfied(max_var)

        for variable_name in self.__variable_names:
            cur = self.__num_satisfied(variable_name)
            if cur > max_num:
                max_num = cur
                max_var = variable_name
            elif cur == max_num:
                max_var = variable_name

        return max_var

        # return max_vars[0]

    # def get_type_0_satisfied(self):
    #     """
    #     Get amount of satisfied constraints that are of type 0
    #     :return:
    #     """
    #     count = 0
    #
    #     for constraint in self.


    def get_num_satisfied(self):
        """
        Get amount of satisfied constraints
        :return:
        """

        count = 0

        for constraint in self.constraints:
            if constraint.check_assignment(self.assignment):
                count += 1

        return count

    def __num_satisfied(self, variable_name):
        """
        Checks how much clauses are satisfied after flipping this variables value.
        :param variable_name: the variable to flip.
        :return: the amount of satisfied clauses after flipping.
        """
        self.__flip_value(variable_name)

        restore = {}

        if len(self.satisfied) == 0:
            for constraint in self.constraints:
                if constraint.check_assignment(self.assignment):
                    self.satisfied[constraint] = True
                else:
                    self.satisfied[constraint] = False
        else:
            for constraint in self.csp.variables[variable_name].get_constraints():
                restore[constraint] = self.satisfied[constraint]
                if constraint.check_assignment(self.assignment):
                    self.satisfied[constraint] = True
                else:
                    self.satisfied[constraint] = False

        count = 0
        for constraint in self.satisfied:
            if self.satisfied[constraint]:
                count += 1

        self.__flip_value(variable_name)  # flip back

        for constraint in restore:
            self.satisfied[constraint] = restore[constraint]

        return count

    def solve(self):
        """
        The WalkSAT algorithm

        :return: dictionary of assignments (of the form {varName: val})
        """

        self.random_assignment()

        if self.is_satisfied():
            return magicNums.SUCCESS
        else:
            for i in range(self.__max_flips):
                constraint = self.random_constraint()
                if self.__flip_coin():
                    # print("random")
                    self.__flip_random_variable(constraint)
                else:
                    # print("most")
                    self.__flip_most_satisfying()

        print("Total Amount of Constraints:", len(self.constraints))
        print("Total Satisfied Constraints:", self.get_num_satisfied())
        return magicNums.SUCCESS
