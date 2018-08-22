from CSP.Variable import *
import queue
from copy import *
import time
from threading import Thread


class CspHandler:
    """
    main CSP handler. should be main authority for handling variables, domains and constraints.
    """

    def __init__(self, domain, variables, constraints,
                 variable_heuristic_creator, domain_heuristic_creator, forward_checking_flag=True):
        """
        A csp handler, will hold and translate a problem for a solver.
        Can use forward checking.

        :param domain: a lists of lists such that list i corresponds with variable name i.
        :param variables: a list of variable names.
        :param constraints: a constraints function that corresponds with the names of the variables.
        :param variable_heuristic_creator: a variable heuristic creator function. returns an object that derives from
                VariableHeuristic.
        :param domain_heuristic_creator: a domain heuristic creator function. returns an object that derives from
                DomainHeuristic.
        :param forward_checking_flag: determines if we use forward checking in this CSP object.
        """

        self._forward_checking_flag = forward_checking_flag

        self.constraints = constraints
        self.variables = {}
        self._generate_variables(variables, domain)  # builds a dictionary of variables.

        self.variable_heuristic = None
        if variable_heuristic_creator is not None:  # For the case in which WalkSAT is used (No heuristic)
            self.variable_heuristic = variable_heuristic_creator(self.variables)

        self.domain_heuristic = None
        if domain_heuristic_creator is not None:  # For the case in which WalkSAT is used (No heuristic)
            self.domain_heuristic = domain_heuristic_creator()

        self.__fc_variables_backup = []  # a stack contains the previous versions of variables.

        # Restore values for csp restore.
        self.__domain_list = domain
        self.__variables_list = variables
        self.__current_assignment = dict.fromkeys(self.variables, None)

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
                # adding neighbours to a variable:
                neighbours_names = set()
                for constraint in constraints:
                    self.__add_neighbours_to_var(name, constraint.get_variables())
                #     for neighbour in constraint.variables:
                #         neighbours_names.add(neighbour)
                # if name in neighbours_names:
                #     neighbours_names.remove(name)  # remove self from neighbours.
                # self.variables[name].set_neighbours(neighbours_names)  # give a reference to the set.
            else:
                raise Exception("Variable name repeats twice!")

    def shuffle(self):
        self.variable_heuristic.shuffle()

    def restore_csp_handler(self):
        """
        Restarts all variables and re initialize the csp handler using the current constraints.
            will operate as a new CspHandler. if the constraints were updated - would not
            restore them to previous condition.
        :return: None.
        """
        self.__fc_variables_backup = []
        self.variables = {}
        self._generate_variables(self.__variables_list, self.__domain_list)
        if self.variable_heuristic:
            self.variable_heuristic.re_initialize_sort(self.variables)

    def make_visible(self):
        """
        makes all constraints visible.
        :return: None
        """
        self.constraints.set_constraints_visible()
        for variable_name in self.variables:
            # update variables with new constraints, and neighbours.
            constraints = self.constraints.get_constraints_by_variable(variable_name)
            for constraint in constraints:
                self.variables[variable_name].add_constraint(constraint)
                self.__add_neighbours_to_var(variable_name, constraint.get_variables())
        if self.variable_heuristic:
            self.variable_heuristic.re_initialize_sort(self.variables)


    def order_domain_values(self, variable_name):
        """
        Should return some list of values to follow.
        :param variable_name: the name of the variable to get it's domain value from.
        :return: a list of values to assign.
        """
        if self.domain_heuristic is None:
            return self.variables[variable_name].get_possible_domain()
        variable = self.variables[variable_name]
        assignment = self.__get_assignment_of_neighbours(variable)
        assignment[variable.name] = variable.value
        return self.domain_heuristic.get_value(variable, assignment)

    def select_unassigned_variable(self):
        """
        uses heuristic to choose a variable.
        :return: full variable name.
        """
        if self.variable_heuristic is None:
            return list(self.variables.keys())
        return self.variable_heuristic.select_unassigned_variable()

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

        assignment = self.__get_assignment_of_neighbours(variable)
        assignment[variable_name] = value  # Assignment should have the 'new' value.

        res = self.check_constraint_agreement(all_constraints, assignment)
        if not res:
            return res

        if self._forward_checking_flag:
            res = self.forward_checking(variable_name, value)
        return res

    def __add_neighbours_to_var(self, var_name, neighbours_names):
        """
        adds neighbours to the variable, update it such that it would not add itself to the neighbours.
        :param var_name: a variable name.
        :param neighbours_names: the names of all the neighbours.
        """
        self.variables[var_name].add_neighbours(neighbours_names)
        # removing var_name from the variable's neighbours if it was added.
        if var_name in self.variables[var_name].neighbours_names:
            self.variables[var_name].neighbours_names.remove(var_name)

    def add_constraint(self):
        """
        add constraint to the visible constraint list.
        :return: True if it added, False otherwise ( can return false if nothing to add).
        """
        constraint = self.constraints.add_constraint()
        if constraint is None:
            return False
        all_var_names = constraint.get_variables()
        for var_name in all_var_names:
            # adding every ones as my new neighbours.
            self.__add_neighbours_to_var(var_name, all_var_names)
            self.variables[var_name].add_constraint(constraint)
        if self.variable_heuristic:
            self.variable_heuristic.re_initialize_sort(self.variables)
        return True

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
            self.__restore()

    def __get_all_visible_constraints(self):
        all_constraints_dict = self.constraints.get_visible_constraints()
        all_consts_lst = []
        for list_of_consts in all_constraints_dict.values():
            all_consts_lst += list_of_consts
        return all_consts_lst

    def check_assignment(self, variable_assignment):
        """
        # checks the full assignment over all constraints
        :param variable_assignment:
        :return:g
        """
        all_consts_lst = self.__get_all_visible_constraints()
        return self.check_constraint_agreement(all_consts_lst, variable_assignment)

    @staticmethod
    def check_constraint_agreement(constraints, assignment):
        """
        gets a bunch of constraints and an assignment and checks whether all constraints are not violated or not.
        :return True if assignment agrees with all of the constraints, False otherwise.
        """
        for constraint in constraints:
            if not constraint.check_assignment(assignment):
                return False
        return True

    @staticmethod
    def __parralel_check_agreement(ret_val, constraints, assignment, index):
        for i in range(index, len(constraints), 2):
            if not constraints[i].check_assignment(assignment):
                ret_val[0] = 0
                break

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
            # variables_copy[var_name] = deepcopy(self.variables[var_name])
            variables_copy[var_name] = copy(self.variables[var_name])
        return variables_copy

    def __update_neighbours_as_wanting_a_visit(self, var_obj, visited):
        for neighbour in var_obj.get_neighbors():
            if self.variables[neighbour] in visited:
                # meaning we wish to revisit this neighbour.
                visited[var_obj.name][0] = True

    def __is_relevant(self, variable, visited, variables_copy):
        """
        Tests if a certain variable relevant for the rest of the FC tests. A variable is not relevant if it is either
        unchanged by the assignment  of the tested variable, or never visited by the algorithm.
        :param variable: A variable name to check.
        :param visited: A list of visited variable objects.
        :return: True if relevant, otherwise False.
        """
        var_obj = variables_copy[variable]
        if variable not in visited:
            return True
        elif visited[variable][0]:

            # meaning we checked the neighbour and don't need to do it again for same reason.
            visited[variable][0] = False
            return True
        else:
            if len(var_obj.get_possible_domain()) < len(visited[variable][1]):
                self.__update_neighbours_as_wanting_a_visit(var_obj, visited)
            # return True
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

    def __check_possible_domain(self, curr_variable, assignment, variables_copy):
        """
        Tests if the current variable's domain is whipped out. In addition updated the current variable's domain.
        :param curr_variable: A variable name
        :param assignment: The current assignment
        :param variables_copy: A deep copy of csp.variables.
        :return: True if the domain of the current variable is wiped out, False otherwise.
        """
        var_obj = variables_copy[curr_variable]
        # if the variable has an assignment already - do not check it!
        if var_obj.value is not None:
            return False
        copy_of_possible_domain = deepcopy(var_obj.get_possible_domain())
        previous_val = assignment[curr_variable]
        for domain_value in copy_of_possible_domain:  # for d in possible domain.
            assignment[curr_variable] = domain_value
            constraints = var_obj.get_constraints()
            if not self.check_constraint_agreement(constraints, assignment):
                var_obj.remove_from_possible_domain(domain_value)
                # we should remove this value because there is at least one constraint who isn't happy about it.
        assignment[curr_variable] = previous_val
        if len(var_obj.get_possible_domain()) != 0:
            if len(var_obj.get_possible_domain()) == 1:
                assignment[curr_variable] = next(iter(var_obj.get_possible_domain()))
            return False  # variable has at least one value in it's possible domain meaning still isn't empty.
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
        # shortcut: we assign the only possible value as the wanted assignment.
        var_obj = variables_copy[variable_name]
        stored_possible_domain = deepcopy(var_obj.get_possible_domain())
        var_obj.set_value(value)
        var_obj.set_possible_domain([value])

        q = queue.Queue()
        q.put(variable_name)
        while not q.empty():
            curr = q.get()
            if self.__is_relevant(curr, visited, variables_copy):

                self.__enter_neighbors_to_queue(curr, q, variables_copy)
                # saving the current variable's possible domain, if it changes later on than it is interesting
                #  to check again. False indicates that the flag of neighbours changed didn't occur.
                visited[curr] = [False, variables_copy[curr].get_possible_domain()]
                # updates the possible domain, if it returns empty -> than we return False.
                # a = time.time()
                is_wiped_out = self.__check_possible_domain(curr, assignment, variables_copy)
                if is_wiped_out:
                    return False
        var_obj.set_possible_domain(stored_possible_domain)  # restoring the possible domain.
        self.__check_possible_domain(var_obj.name, assignment, variables_copy)  # doing final clean on possible domain
        # storing the non changed variables for a restore later.
        self.__fc_variables_backup.append(self.variables)
        self.variables = variables_copy  # The fc succeeded so we keep the changes in the variables.

        return True

    def __restore(self):
        """
        returns the variables to what they ware one version before fc.
        """
        if len(self.__fc_variables_backup) > -1:
            self.variables = self.__fc_variables_backup.pop()

    ####################
    #   STATS REPORT   #
    ####################
    def get_report(self, assignment):
        """
        Generates a counter {softness level: [number of satisfied constraints, number of constraints over all]}
        where each key points to specific type of constraints.
        """
        all_constraints_dict = self.constraints.get_all_constraints()
        all_consts_lst = []
        for list_of_consts in all_constraints_dict.values():
            all_consts_lst += list_of_consts
        counter = {}
        for constraint in all_consts_lst:
            if constraint.is_soft not in counter:
                counter[constraint.is_soft] = [0, 0]  # number of satisfied, number of constraint from this type.
            if constraint.check_assignment(assignment):
                counter[constraint.is_soft][0] += 1
            counter[constraint.is_soft][1] += 1
        return counter
