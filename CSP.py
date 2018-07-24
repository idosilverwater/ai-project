from Constraints import *
from Variable import *


class CSP:
    """
    main CSP handler. should be main authority for handling variables, domains and constraints.
    """

    # TODO determine what input the constructor should have.
    def __init__(self, domain, variables, constraints):
        """

        :param domain: a lists of lists such that list i corresponds with variable name i.
        :param variables: a list of variable names.
        :param constraints: a constraints function that coresponds with the names of the variables.
        """
        self.constraints = constraints
        # builds a dictionary of variables.
        self.domains = {}  # a domain for each variable to be used somehow later on. # TODO consider to delete.
        self.variables = {}
        self._generate_variables(variables, domain)

        self.variable_heuristic = None  # TODO.
        self.domain_heuristic = None  # TODO.

        self._forward_checking_flag = False  # TODO.

    def _generate_variables(self, names, domain):
        """
        generate variables instances and tie them to a name.
        lastly creates neighbours for every variable - related variables by constraints.
        :param names: the names of the variables. (list)
        :param domain: the values for each variable (list of lists as in the __init__ func).
        :return: None.
        """
        for i, name in enumerate(names):
            constraints = self.constraints.get_constraints_by_variable(name)
            var = Variable(name, domain[i], constraints)
            if var not in self.variables:
                self.variables[name] = var
                self.domains[name] = domain[i]
                # adding neighbours to a variable:
                neighbours_names = set()
                for constraint in constraints:
                    for neighbour in constraint.variables:
                        neighbours_names.add(neighbour)
                if name in neighbours_names:  # I added this if because it isn't guaranteed (ido).
                    neighbours_names.remove(name)
                self.variables[name].set_neighbours(neighbours_names)  # give a reference to the set.
            else:
                raise Exception("Variable name repeats twice!")

    def make_visible(self):
        """
        makes all constraints visible.
        :return: None
        """
        self.constraints.set_visible_constrains()

    def order_domain_values(self, variable_name):
        """
        Should return some list of values to follow.
        :param variable_name: the name of the variable to get it's domain value from.
        :return: a list of values to assign.
        """
        return self.domain_heuristic.get_order_domain(variable_name, self.domains, self.constraints)

    def select_unassigned_variable(self):
        """
        uses heuristic to choose a variable.
        :return: full variable name.
        """
        return self.variable_heuristic.select_unassigned_variable(self.variables)

    def assign_variable(self, var_name, value):
        """
        function assumes that the value is consistent and can be added to the var name.
        :param var_name:
        :param value:
        :return:
        """
        # add assignment of one value
        variable = self.variables[var_name]
        variable.set_value(value)
        # add forward checking:
        if self._forward_checking_flag:
            pass  # TODO forward checking : should assign value, and update every friend of variable of it's new domain.
        pass

    def is_consistent(self, variable_name, value):
        """
        checks if this value can be assigned.
        :param variable_name: the name of the variable.
        :param value: value to try and assign to the variable.
        :return: True if it's okay, False otherwise.
        """
        # checking if value is in domain and in possible domain:
        variable = self.variables[variable_name]
        if not variable.is_value_legit(value):
            return False

        # Should check every constraint relevant to this variable name and check if the value is allowed there!
        # if one constraint returns no that means this value is not allowed and it contradicts the other
        # values it currently hold.

        variable_set = set()
        all_constraints = self.variables[variable_name].get_constraints()
        for constraint in all_constraints:
            variable_set.add(constraint.get_variables())  # TODO check if this does as expected.

        assignment = {variable_name: self.variables[variable_name].get_value() for variable_name in variable_set}
        # TODO try and optimise this whole operation. Maybe with threads or something. (can thread this function)
        return self.__check_constraint_agreement(all_constraints, assignment)

    def add_constraint(self):
        """
        add constraint to the visible constraint list.
        :return: True if it added, False otherwise ( can return false if nothing to add).
        """

        # TODO: constraints class should output the constraint in order to update which variables are related to it.
        pass

    def un_assign_variable(self, variable_name):
        """
        does necessary updates to the csp object if the value should be un assigned.
        :param variable_name:
        :return:
        """
        variable = self.variables[variable_name]
        current_Value = variable.get_value()  # should be relevant in forward checking.
        variable.set_value(None)
        # TODO cont:
        visited_var = set()
        for constraint in self.variables[variable_name].get_constraints():
            for variable in constraint.get_variables():
                if not variable in visited_var:
                    pass  # TODO
        # forward checking:
        if self._forward_checking_flag:
            pass
        pass

    # TODO check if assignment is a legit one. means that for every constrain, check if all values are possible together
    def check_assignment(self, variable_assignment):
        """
        checks the full assignment over all constraints
        :param variable_assignment:
        :return:
        """
        return self.__check_constraint_agreement(self.constraints.get_all_constraints(), variable_assignment)

    def __check_constraint_agreement(self, constraints, assignment):
        """
        gets a bunch of constraints and an assignment and checks wether all constraints are not violated or not.
        """
        for constraint in constraints:
            if not constraint.check_assignment(assignment):
                return False
        return True
