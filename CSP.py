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
        pass  # TODO should assign value, and update every friend of variable of it's new domain.

    def is_consistent(self, variable_name, value):
        """
        checks if this value can be assigned.
        :param variable_name: the name of the variable.
        :param value: value to try and assign to the variable.
        :return: True if it's okay, False otherwise.
        """
        constraints_on_var = self.constraints.get_constraints_by_variable(variable_name)
        all_values = [set(x.get_possible_values()) for x in constraints_on_var]
        legal_values = {}

        for values in all_values:
            legal_values = legal_values & values
        return value in legal_values

    def add_constraint(self):
        """
        add constraint to the visible constraint list.
        :return: True if it added, False otherwise ( can return false if nothing to add).
        """

        # TODO: constraints class should output the constraint in order to update which variables are related to it.
        pass

    def un_assign_variable(self, variable_name, value):
        """
        does necessary updates to the csp object if the value should be un assigned.
        :param variable_name:
        :param value:
        :return:
        """
        pass
