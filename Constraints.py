from Constraint import *
import WorkersCSP
import magicNums

# magic Nums.
DOMAIN_TRUE_VAL = magicNums.DOMAIN_TRUE_VAL
DOMAIN_FALSE_VAL = magicNums.DOMAIN_FALSE_VAL


class Constraints:
    """
    This class is generating the soft and hard constrains according to the
    parser's output.
    """

    def __init__(self, preferences, non_workable_shifts, variable_names, constraint_heuristic=None):
        """
        Creates several dictionaries of constraints.
        :param preferences: A list of the workers preferences. For example:
         [(1,2,3)] is a list with one preference: worker1 wants to work on
         shift 3 on Tuesday.
        :param variable_names: A list of variables names. A variable name for
        example would be "(1,2,3)"
        """
        self.__preferences = preferences
        self.__non_workable_shifts = non_workable_shifts
        self.__variable_names = variable_names
        self.__constraint_heuristic = constraint_heuristic

        self.__all_constraints = {}  # (Variable names): [constraints on variables]
        self.__visible_constraints = {}  # (Variable names): [constraints on variables]
        self.__constraints_by_var = {}  # var name: [constrains on var]

        # J added this to save runtime:
        self.__dictionary_of_possible_assignments = {}
        self.__build_all_constraints()
        self.__dictionary_of_possible_assignments = {}  # restarting the dictionary.

        self.__set_constraint_by_var()  # todo NOY, should this be called here? (ido) answer is: yes (Jonathan)

    ###################
    # Private Methods #
    ###################

    def __build_all_constraints(self):
        """
        Generates all of the constraints.
        """
        self.__generate_hard_const()
        self.set_constraints_visible()
        self.__generate_soft_const()

    def __variable_names_by_shift(self, day, shift_number):
        """
        This function generates a tuple of variable names that are relevant for
        a certain shift.
        :param: day: For example: 3
        :param: shift: For example: 2
        ============
        For Example:
        ============
        1) A variable name that is relevant to the first shift on Sunday is:
        (5,1,1).
        2) A variable name that is not relevant is: (5,2,3)
        :return: A tuple of variable names
        """
        relevant_vars = []
        for name in self.__variable_names:
            if name.endswith(str(day) + magicNums.SEPARATOR + str(shift_number)):
                relevant_vars.append(name)
        return tuple(relevant_vars)

    def __one_worker_helper(self, number_of_workers, curr, result_lst,
                            current_list):
        """
        A recursive function that returns a list of lists with all possible values for the bakery constraint problem
        [[T,T,T,T,T..T], [T,T,T,T,T..F,T], ...,[F,F,F,F,...,F]].
        """
        if number_of_workers == curr:
            result_lst.append(current_list)
        else:
            self.__one_worker_helper(number_of_workers, curr + 1, result_lst,
                                     current_list + [DOMAIN_TRUE_VAL])
            self.__one_worker_helper(number_of_workers, curr + 1, result_lst,
                                     current_list + [DOMAIN_FALSE_VAL])

    def __generate_assignments_for_at_least_one_worker(self,
                                                       number_of_workers):
        """
        This method generates assignments with respect to the hard constraint:
        "There should be at least one worker in a shift"
        :param: number_of_workers: The number of workers.
        :return: A list of possible assignments.
        For Example(three workers): [[True,True,False],[False,True,False]]
        """
        # J: the previous function was to expensive, i added memory components to save runtime.
        if number_of_workers in self.__dictionary_of_possible_assignments:
            return self.__dictionary_of_possible_assignments[number_of_workers]

        lst = []
        self.__one_worker_helper(number_of_workers, 0, lst, [])
        lst.pop()
        self.__dictionary_of_possible_assignments[number_of_workers] = lst
        return lst

    @staticmethod
    def __add_constraint_to_all_constraints_dict(dictionary, key, value):
        """
        Helper function for the hard constraints adding items.
        """
        if key in dictionary:
            dictionary[key].append(value)
        else:
            dictionary[key] = [value]
        pass

    def __create_constraints_for_worker_in_same_shift(self, assignment_generator):
        """
        Generates hard constraints for same shift and all workers, using an assignment_generator function.
        This will  take all constraints with same day and same shift and generate a constraint with all of the relevant
        variables.
        """
        # Creates a variable list that is relevant to a certain shift:
        for i in range(magicNums.DAYS_IN_WEEK):  # For each day
            for j in range(magicNums.SHIFTS_IN_DAY):  # For each shift.
                relevant_variables = self.__variable_names_by_shift(i, j)
                possible_assignments = assignment_generator(len(relevant_variables))
                new_constraint = Constraint(relevant_variables, possible_assignments, 0)
                self.__add_constraint_to_all_constraints_dict(self.__all_constraints, relevant_variables,
                                                              new_constraint)

    def __generate_non_workable_days(self):
        """
        Create constraints for days that a worker cannot work at.
        """
        for name in self.__non_workable_shifts:
            var_name = (name,)
            new_constraint = Constraint(var_name, [[DOMAIN_FALSE_VAL]], 0)  # hard const that cant be assigned.
            self.__add_constraint_to_all_constraints_dict(self.__all_constraints, var_name, new_constraint)

    def __generate_assignments_for_at_most_x_workers(self, num_workers, x=2):
        """
        creates assignment list for constraint that wish to have at most x workers.
        :param num_workers: the number of variables in a shift.
        :param x: the maximum amount of workers we want to have in a shift.
        :return: a list of possible assignments.
        """
        lst_of_assignments = []
        for item in self.__generate_assignments_for_at_least_one_worker(num_workers):
            if item.count(magicNums.DOMAIN_TRUE_VAL) <= x:
                lst_of_assignments.append(item)
        return lst_of_assignments

    def __generate_hard_const(self):
        """
        Generates the hard constraints and updates self.constraints.
        For now the only hard constraint is: "There should be a least one worker
        in each shift."
        """

        # generates at most two worker assignments, to work with the __create_constraints_for_worker_in_same_shift func.
        def two_workers_at_most(num_workers):
            return self.__generate_assignments_for_at_most_x_workers(num_workers, 2)

        self.__create_constraints_for_worker_in_same_shift(self.__generate_assignments_for_at_least_one_worker)
        self.__generate_non_workable_days()

        self.__create_constraints_for_worker_in_same_shift(two_workers_at_most)

    def __generate_soft_const(self):
        """
        Generates the soft constraints and updates self.constraints.
        """
        for preference in self.__preferences:
            var_name = ("".join(preference),)
            # Adding constraint to all_constraints:
            new_constraint = Constraint(var_name, [[DOMAIN_TRUE_VAL]], 1)
            self.__add_constraint_to_all_constraints_dict(self.__all_constraints, var_name, new_constraint)

    def __set_constraint_by_var(self):
        """
        After the initialization of visible_constraints
        creates a dictionary with variable names as keys
        and a list of constraints the key is in as a value.
        """
        """ 
        for every var we  go over all constraints, and check if the var is in this constraint. if it is: add it. else! fuck off. 
        """
        for var_name in self.__variable_names:
            for constraint_list in self.__visible_constraints.values():
                for constraint in constraint_list:
                    if var_name in constraint.get_variables():
                        if var_name not in self.__constraints_by_var:
                            self.__constraints_by_var[var_name] = [constraint]
                        else:
                            self.__constraints_by_var[var_name].append(constraint)

    #####################
    # Getters & Setters #
    #####################
    def get_visible_constraints(self):
        return self.__visible_constraints

    def get_all_constraints(self):
        return self.__all_constraints

    def set_constraints_visible(self):
        self.__visible_constraints = dict(self.__all_constraints)

    def add_constraint(self):  # TODO fix it so that it can work with CSP.
        variables, constraint = self.__constraint_heuristic(
            self.__visible_constraints, self.__all_constraints)
        # TODO! NOTICE that these constraint should be added to constraints by var too.
        self.__visible_constraints[variables] = constraint

    def get_constraints_by_variable(self, variable_name):
        return self.__constraints_by_var[variable_name]
