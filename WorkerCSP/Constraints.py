from CSP.Constraint import *
import magicNums

# magic Nums.
from SoftConstraintHeuristics.DegreeSoftHeuristic import *

DOMAIN_TRUE_VAL = magicNums.DOMAIN_TRUE_VAL
DOMAIN_FALSE_VAL = magicNums.DOMAIN_FALSE_VAL


# TODO ADD complicated constraints still.
class Constraints:
    """
    This class is generating the soft and hard constrains according to the
    parser's output.
    """

    def __init__(self, preferences, non_workable_shifts, variable_names, minimum_wanted_shift_dict=None,
                 maximum_workers_per_shift=2, constraint_heuristic_factory=None):
        """
        Creates several dictionaries of constraints.
        :param preferences: A list of the workers preferences. For example:
         [(1,2,3)] is a list with one preference: worker1 wants to work on
         shift 3 on Tuesday.
        :param variable_names: A list of variables names. A variable name for
        example would be "(1,2,3)"
        """
        self.__maximum_workers_per_shift = maximum_workers_per_shift
        self.__minimum_shifts_num = minimum_wanted_shift_dict

        self.__preferences = preferences
        self.__non_workable_shifts = non_workable_shifts
        self.__variable_names = variable_names

        self.__all_constraints = {}  # (Variable names): [constraints on variables]
        self.__visible_constraints = {}  # (Variable names): [constraints on variables]
        self.__constraints_by_var = {}  # var name: [constrains on var]

        # J added this to save runtime:
        self.__dictionary_of_possible_assignments = {}
        self.__build_all_constraints()
        self.__dictionary_of_possible_assignments = {}  # restarting the dictionary.

        self.__set_constraint_by_var()

        # perpetration for add constraints:
        # self.__ordered_soft_constraints = self.__generate_add_constraints_list(constraint_heuristic_factory)
        # TODO add heuristics to the main and what to choose.
        self.__ordered_soft_constraints = self.__generate_add_constraints_list(DegreeSoftConstraintsHeuristic)
        self.__ordered_soft_constraints.reverse()  # TODO check if needed!

    #####################
    # Getters & Setters #
    #####################
    def get_visible_constraints(self):
        """
        gets a dictionary of all visible constraints.
        """
        return self.__visible_constraints

    def get_all_constraints(self):
        """
        gets a dictionary of visible constraints.
        """
        return self.__all_constraints

    def set_constraints_visible(self):
        """
        makes all constraints visible.
        """
        self.__visible_constraints = dict(self.__all_constraints)
        self.__set_constraint_by_var()
        self.__ordered_soft_constraints = []

    def add_constraint(self):
        """
        adds one constraint to the visible constraints and returns said constraint. if it fails returns None.
        :return: Constraint object or None.
        """
        # If self.__ordered_soft_constraints is None or it is an empty list: returns None.
        if not self.__ordered_soft_constraints:
            return None

        soft_constraint = self.__ordered_soft_constraints.pop()
        variables = soft_constraint.get_variables()
        keys = self.__get_all_keys_containing_vars(self.__all_constraints, variables)
        for key in keys:
            if key in self.__visible_constraints:
                if soft_constraint in self.__visible_constraints:
                    raise Exception("There shouldn't be the same soft constraint in the visible!")
                self.__visible_constraints[key].append(soft_constraint)
            else:
                self.__visible_constraints[key] = [soft_constraint]
        return soft_constraint

    def get_constraints_by_variable(self, variable_name):
        """
        :param: variable_name: a string name of a variable.
        :return: a list of constraints objects that are tied to this variable name.
        """
        return self.__constraints_by_var[variable_name]

    ###################
    # Private Methods #
    ###################
    def __generate_add_constraints_list(self, constraint_heuristic_factory):
        """
        generates a list of ordered soft constraints.
        :param constraint_heuristic_factory: a function that returns a heuristic for constraints given a list of hard
                constraints and a list of soft constraints.
        :return: an ordered list of soft constraints.
        """
        if constraint_heuristic_factory is None:
            return None

        soft_const = []
        hard_consts = []
        for key in self.__all_constraints:
            for constraint in self.__all_constraints[key]:
                if constraint.is_soft != magicNums.HARD_CONSTRAINT_VALUE:
                    soft_const.append(constraint)
                else:
                    hard_consts.append(constraint)

        self.__constraint_heuristic = constraint_heuristic_factory(hard_consts, soft_const)
        return self.__constraint_heuristic.get_adding_order()

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
            if name.endswith(str(day) + magicNums.VARIABLE_NAME_SHIFT_SEPARATOR + str(shift_number)):
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
            if value not in dictionary[key]:  # TODO maybe make into set for faster check.
                dictionary[key].append(value)
        else:
            dictionary[key] = [value]

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
                new_constraint = Constraint(relevant_variables, possible_assignments, magicNums.HARD_CONSTRAINT_VALUE)
                self.__add_constraint_to_all_constraints_dict(self.__all_constraints, relevant_variables,
                                                              new_constraint)

    def __generate_non_workable_days(self):
        """
        Create constraints for days that a worker cannot work at.
        """
        for name in self.__non_workable_shifts:
            var_name = (name,)
            # hard const that cant be assigned.
            new_constraint = Constraint(var_name, [[DOMAIN_FALSE_VAL]], magicNums.HARD_CONSTRAINT_VALUE)
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

    def __generate_assignments_for_at_least_x_possible_true(self, num_workers, x):
        """
        creates assignment list for constraint that wish to have at most x workers.
        :param num_workers: the number of variables in a shift.
        :param x: the maximum amount of workers we want to have in a shift.
        :return: a list of possible assignments.
        """
        lst_of_assignments = []
        for item in self.__generate_assignments_for_at_least_one_worker(num_workers):
            if item.count(magicNums.DOMAIN_TRUE_VAL) >= x:
                lst_of_assignments.append(item)
        return lst_of_assignments

    def __generate_hard_const(self):
        """
        Generates the hard constraints and updates self.constraints.
        For now the only hard constraint is: "There should be a least one worker
        in each shift."
        """

        # generates at most two worker assignments, to work with the __create_constraints_for_worker_in_same_shift func.
        def x_workers_at_most(num_workers):
            return self.__generate_assignments_for_at_most_x_workers(num_workers, self.__maximum_workers_per_shift)

        self.__create_constraints_for_worker_in_same_shift(self.__generate_assignments_for_at_least_one_worker)
        self.__generate_non_workable_days()

        self.__create_constraints_for_worker_in_same_shift(x_workers_at_most)

    def __preference_days_constraints(self):
        for preference in self.__preferences:
            var_name = (" ".join(preference),)
            # Adding constraint to all_constraints:
            new_constraint = Constraint(var_name, [[DOMAIN_TRUE_VAL]], magicNums.BAKERY_SOFT_CONSTRAINT_VALUE)
            self.__add_constraint_to_all_constraints_dict(self.__all_constraints, var_name, new_constraint)

    def __gather_all_possible_shifts(self, name):
        """
        generates all possible variations of variable according to its name.  That is a list of all possible days and
            shifts: [David i j for i, j in days, shifts]
        :param name: a string representing the name of the variable.
        :return: a tuple.
        """
        all_possible_days = []
        for day in range(magicNums.DAYS_IN_WEEK):
            for shift in range(magicNums.SHIFTS_IN_DAY):
                all_possible_days.append(magicNums.VARIABLE_NAME_SHIFT_SEPARATOR.join([name, str(day), str(shift)]))
        return tuple(all_possible_days)

    def __wanted_amount_of_shifts(self):
        """
        :return:
        """
        if self.__minimum_shifts_num:
            visited = set()
            for variable_name in self.__variable_names:
                name = variable_name.split(magicNums.VARIABLE_NAME_SHIFT_SEPARATOR)[0]
                if name not in visited:
                    visited.add(name)
                    possible_assignment = self.__generate_assignments_for_at_least_x_possible_true(
                        magicNums.DAYS_IN_WEEK * magicNums.SHIFTS_IN_DAY,
                        self.__minimum_shifts_num[name])
                    all_names = self.__gather_all_possible_shifts(name)
                    new_constraint = Constraint(all_names, possible_assignment,
                                                magicNums.SHIFTS_IN_WEEK_CONSTRAINT_VALUE)
                    self.__add_constraint_to_all_constraints_dict(self.__all_constraints, all_names,
                                                                  new_constraint)

    def __exac_amount_of_shifts(self):
        if self.__minimum_shifts_num:
            visited = set()
            for variable_name in self.__variable_names:
                name = variable_name.split(magicNums.VARIABLE_NAME_SHIFT_SEPARATOR)[0]
                if name not in visited:
                    visited.add(name)
                    all_assignments = self.__generate_assignments_for_at_least_one_worker(
                        magicNums.DAYS_IN_WEEK * magicNums.SHIFTS_IN_DAY)
                    res = [
                        *filter(lambda x: x.count(DOMAIN_TRUE_VAL) == self.__minimum_shifts_num[name], all_assignments)]
                    if res:
                        all_names = self.__gather_all_possible_shifts(name)
                        new_constraint = Constraint(all_names, res,
                                                    magicNums.SHIFTS_IN_WEEK_CONSTRAINT_VALUE)
                        self.__add_constraint_to_all_constraints_dict(self.__all_constraints, all_names,
                                                                      new_constraint)
        pass

    def __generate_soft_const(self):
        """
        Generates the soft constraints and updates self.__all_constraints.
        """
        self.__preference_days_constraints()
        # self.__wanted_amount_of_shifts()
        self.__exac_amount_of_shifts()

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
                            # in efficient but necessary. can be overcome by use of more memory.
                            if constraint not in self.__constraints_by_var[var_name]:
                                self.__constraints_by_var[var_name].append(constraint)

    @staticmethod
    def __get_all_keys_containing_vars(dictionary_of_constraints, iterable_of_variables):
        """
        because the variables may be ordered differently than the keys: we wish to find all the keys that are
            corresponding to the varibles we've got currently.
        :param dictionary_of_constraints:
        :param iterable_of_variables:
        :return: a list of keys in the dictionary given.
        """
        lst_of_keys = []
        # key is a tuple of variables!
        for key in dictionary_of_constraints:
            if len(key) == len(iterable_of_variables):
                counter = 0
                for variable in iterable_of_variables:
                    if variable in key:
                        counter += 1
                # check if the counter
                if counter == len(key) and counter == len(iterable_of_variables):
                    lst_of_keys.append(key)
        return lst_of_keys
