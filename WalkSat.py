from Solver import Solver
import random


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
