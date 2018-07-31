from Constraints import *
from Variable import *
import Degree

# import LeastConstrainingValue


# import DomainHeuristic, LeastConstrainingValue, MinimumConflict, MinimumRemainingValue
# TODO arc consistency.
"""
HOW to do arc consistency- copy current CSP. than do ar consistency on the non copied.
This way we can "rewrite" back to the old csp when the backtrack fails. problem is: costly on memory. 
but fuck it, we've got at least 4GB of mem...
"""


# TODO forward checking.


class CSP:
    """
    main CSP handler. should be main authority for handling variables, domains and constraints.
    """

    # TODO determine what input the constructor should have.
    def __init__(self, domain, variables, constraints, forward_checking_flag=False):
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
        # TODO need this to be generic!
        self.variable_heuristic = Degree.Degree(self.variables)  # variable_heuristic_factory(self.variables)
        self.domain_heuristic = None  # domain_heuristic_factory(self.variables, self.constraints)

        self._forward_checking_flag = forward_checking_flag

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
        self.constraints.set_constraints_visible()

    def order_domain_values(self, variable_name):
        """
        Should return some list of values to follow.
        :param variable_name: the name of the variable to get it's domain value from.
        :return: a list of values to assign.
        """
        return self.variables[variable_name].get_possible_domain()  # TODO should use the heuristics.
        # return self.domain_heuristic.get_order_domain()

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
        pass  # TODO

    # def __forward_check_consistent(self, variable_name):
    #     # TODO  notice this is a Scetch with no basis..
    #     variable = self.variables[variable_name]
    #     # variable.set_affecting_value(value)
    #     affected_variables = []
    #     for neighbour in variable.get_neighbors():
    #         if self.variables[neighbour].is_not_assigned:
    #             affected_variables.append(neighbour)

    def is_consistent(self, variable_name, value):
        """
        checks if this value can be assigned.

        # Should check every constraint relevant to this variable name and check if the value is allowed there!
        # if one constraint returns no that means this value is not allowed and it contradicts the other
        # values it currently hold.

        :param variable_name: the name of the variable.
        :param value: value to try and assign to the variable.
        :return: True if it's okay, False otherwise.
        """
        # checking if value is in domain and in possible domain:
        variable = self.variables[variable_name]
        if not variable.is_value_legit(value):
            return False

        # if self._forward_checking_flag: #TODO understand how to forward checking god dammnit.
        #     self.__forward_check_consitent(variable_name)

        all_constraints = self.variables[variable_name].get_constraints()

        variable_set = variable.get_neighbors()
        assignment = {variable_name: self.variables[variable_name].get_value() for variable_name in variable_set}
        assignment[variable_name] = value  # Assignment should have the 'new' value.

        # TODO try and optimise this whole operation. Maybe with threads or something. (can thread this function)
        return self.__check_constraint_agreement(all_constraints, assignment)

    def add_constraint(self):
        """
        add constraint to the visible constraint list.
        :return: True if it added, False otherwise ( can return false if nothing to add).
        """
        self.add_constraint()
        # TODO add True or False return if it is possible to add constraint.

    def un_assign_variable(self, variable_name):
        """
        does necessary updates to the csp object if the value should be un assigned.
        :param variable_name:
        """
        variable = self.variables[variable_name]
        current_Value = variable.get_value()  # should be relevant in forward checking.
        variable.set_value(None)

        # forward checking:
        if self._forward_checking_flag:
            pass  # TODO...
        pass

    # TODO check if assignment is a legit one. means that for every constrain, check if all values are possible together
    def check_assignment(self, variable_assignment):
        """
        # checks the full assignment over all constraints
        :param variable_assignment:
        :return:
        """
        # We reached this hence we failed.
        all_constraints_dict = self.constraints.get_all_constraints()
        all_consts_lst = []
        for key in all_constraints_dict:
            all_consts_lst += all_constraints_dict[key]
        return self.__check_constraint_agreement(all_consts_lst,
                                                 variable_assignment)

    @staticmethod
    def __check_constraint_agreement(constraints, assignment):
        """
        gets a bunch of constraints and an assignment and checks wether all constraints are not violated or not.
        """
        # if we wish to parallel this function-we need to split the dictionary of constraints and give it to each thread
        for constraint in constraints:
            if not constraint.check_assignment(assignment):
                return False
        return True
