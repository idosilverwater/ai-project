from Variable import *
import queue
from copy import *


# import LeastConstrainingValue


# import DomainHeuristic, LeastConstrainingValue, MinimumConflict, MinimumRemainingValue
# TODO arc consistency.


class CSP(object):
    """
    main CSP handler. should be main authority for handling variables, domains and constraints.
    """

    def __init__(self, domain, variables, constraints,
                 variable_heuristic_creator, domain_heuristic_creator, forward_checking_flag=True):
        """
        :param domain: a lists of lists such that list i corresponds with variable name i.
        :param variables: a list of variable names.
        :param constraints: a constraints function that corresponds with the names of the variables.
        """
        self.constraints = constraints
        self.domains = {}  # a domain for each variable to be used somehow later on. # TODO consider to delete.
        self.variables = {}
        self._generate_variables(variables, domain)  # builds a dictionary of variables.
        self.variable_heuristic = variable_heuristic_creator(self.variables)
        self.domain_heuristic = domain_heuristic_creator()
        self.__fc_variables_backup = [self.variables]  # a stack contains the previous versions of variables.
        self._forward_checking_flag = forward_checking_flag

        self.assignment = {}  # TODO remove, this isn't relevant for csp and it should not manage it.

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
                self.variables[name].set_neighbours(
                    neighbours_names)  # give a reference to the set.
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
        variable = self.variables[variable_name]
        assignment = self.__get_assignment_of_neighbours(variable)
        assignment[variable.name] = variable.value
        return self.domain_heuristic.get_value(variable, assignment)

    def select_unassigned_variable(self):
        """
        uses heuristic to choose a variable.
        :return: full variable name.
        """
        return self.variable_heuristic.select_unassigned_variable()

    def get_assignment(self):
        return self.assignment

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
        self.assignment[var_name] = value  # TODO - move out of CSP.

    def __get_assignment_of_neighbours(self, variable):
        """
        :param variable: actual variable and not var_name
        :return: the assignment of the neighbours.
        """
        variable_set = variable.get_neighbors()
        return {variable_name: self.variables[variable_name].get_value()
                for variable_name in variable_set}

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

        all_constraints = self.variables[variable_name].get_constraints()

        variable_set = variable.get_neighbors()
        assignment = self.__get_assignment_of_neighbours(variable)
        assignment[variable_name] = value  # Assignment should have the 'new' value.

        res = self.check_constraint_agreement(all_constraints, assignment)
        if not res:
            return res

        if self._forward_checking_flag:
            res = self.forward_checking(variable_name, value)
        return res

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
        # TODO : MAJOR checks.

        # forward checking:
        if self._forward_checking_flag:
            self.__restore()

    def check_assignment(self, variable_assignment):
        """
        # checks the full assignment over all constraints
        :param variable_assignment:
        :return:
        """
        all_constraints_dict = self.constraints.get_visible_constraints()
        all_consts_lst = []
        for list_of_consts in all_constraints_dict.values():
            all_consts_lst += list_of_consts
        return self.check_constraint_agreement(all_consts_lst,
                                               variable_assignment)

    @staticmethod
    def check_constraint_agreement(constraints, assignment):
        """
        gets a bunch of constraints and an assignment and checks whether all constraints are not violated or not.
        :return True if assignment agrees with all of the constraints, False otherwise.
        """
        # if we wish to parallel this function-we need to split the dictionary of constraints and give it to each thread
        for constraint in constraints:
            if not constraint.check_assignment(assignment):
                return False
        return True

    ####################
    # FORWARD CHECKING #
    ####################
    """
    What We Need:
    1) A way to check if a variable was changed.
    2) A way to deep copy variables.
            should copy every element with no common mutables between thte lists except the constraints which will
            not be affected by a copy.
            To do so - please make a copy function for Variable class in according to copy() protocol of python.

    3) Generate current assignment
    4)use FC, when in need to check an assignment: Find all common constraints and give them to __check_constraints_agreement
                with the current assignment of FC.

    5) Restore - returns the variables to what they ware one version before fc.
                should use a stack that each item in stack contains a whole variable dictionary. of the vars before FC was
                initiated.
    """

    def __copy_variables(self):
        """
        Deep copy self.variables.
        :returns: A dictionary, which is a copy of self.variables
        """
        variables_copy = {}
        for var_name in self.variables:
            variables_copy[var_name] = deepcopy(self.variables[var_name])
        return variables_copy

    def __is_relevant(self, variable, visited, variables_copy):  # todo: test
        """
        Tests if a certain variable relevant for the rest of the FC tests. A variable is not relevant if it is either
        unchanged by the assignment  of the tested variable, or never visited by the algorithm.
        :param variable: A variable name to check.
        :param visited: A list of visited variable objects.
        :return: True if relevant, otherwise False.
        """
        var_obj = variables_copy[variable]
        if variable not in visited:
            visited[variable] = [False, var_obj.get_possible_domain()]
            return True
        elif visited[variable][0]:
            # meaning we checked the neighbour and don't need to do it again for same reason.
            visited[variable][0] = False
            return True
        else:
            var_obj = variables_copy[variable]
            if len(var_obj.get_possible_domain()) != len(visited[variable][1]):
                for neighbour in var_obj.get_neighbors():
                    if self.variables[neighbour] in visited:
                        # meaning we wish to revisit this neighbour.
                        visited[variable][0] = True
                return True
            return False

    def generate_current_assignment(self):
        """
        Generates the current assignment out of the current state of the variables.
        :param value: the current tested value.
        :return: An assignment (A dictionary of the form: {var_name: value})
        """
        return {variable_name: self.variables[variable_name].get_value() for variable_name in self.variables.keys()}

    def __enter_neighbors_to_queue(self, variable, fc_queue, variables_copy):
        """
        This method enters the variable's neighbors to queue.
        :param variable: A variable name
        :param fc_queue: A queue object.
        :param variables_copy: A deep copy of csp.variables.
        """
        neighbors_names = variables_copy[variable].get_neighbors()
        for neighbor in neighbors_names:
            fc_queue.put(neighbor)

    def __check_possible_domain(self, curr_variable, assignment, variables_copy):  # TODO: test
        """
        Tests if the current variable's domain is whipped out. In addition updated the current variable's domain.
        :param curr_variable: A variable name
        :param assignment: The current assignment
        :param variables_copy: A deep copy of csp.variables.
        :return: True if the domain of the current variable is wiped out, False otherwise.
        """
        var_obj = variables_copy[curr_variable]
        copy_of_possible_domain = deepcopy(var_obj.get_possible_domain())
        for d in copy_of_possible_domain:
            assignment[curr_variable] = d
            constraints = var_obj.get_constraints()
            if self.check_constraint_agreement(constraints, assignment):
                return False  # We have a legal value - everything is ok.
            var_obj.remove_from_possible_domain(d)
        return True  # curr_variable is wiped out.

    def forward_checking(self, variable_name, value):
        """
        This is the method that runs the forward checking algorithm.
        :param variable_name: The name of the variable we would like to find assignment too.
        :param value: The value we want to assign to the variable.
        :return True if an assignment was found, False otherwise
        """
        assignment = self.generate_current_assignment()
        visited = {}  # A dictionary of the form: {variable name: (flag, domain)} the flag is used in __is_relevant.
        variables_copy = self.__copy_variables()
        assignment[variable_name] = value
        var_obj = variables_copy[variable_name]
        var_obj.set_value(value)
        var_obj.set_possible_domain([value])
        q = queue.Queue()
        q.put(variable_name)

        while not q.empty():
            curr = q.get()
            if self.__is_relevant(curr, visited, variables_copy):
                self.__enter_neighbors_to_queue(curr, q, variables_copy)
                visited[curr] = (False, variables_copy[curr].get_possible_domain())
                is_wiped_out = self.__check_possible_domain(curr, assignment, variables_copy)
                if is_wiped_out:
                    return False
        self.__fc_variables_backup.append(self.variables)
        self.variables = variables_copy  # The fc succeeded so we keep the changes in the variables.
        return True

    def __restore(self):
        """
        returns the variables to what they ware one version before fc.
        """
        if len(self.__fc_variables_backup) > -1:
            self.variables = self.__fc_variables_backup.pop()
