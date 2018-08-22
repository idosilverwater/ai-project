from Solver.BaseSolver import *

from threading import Thread, Lock
import magicNums

class Backtrack(Solver):
    """
    a solver class, applies backtrack solving algorithm when solve class is initialized.
    """

    def __init__(self, csp, timeout=None):
        """
        excepts a csp problem initialized.
        """
        super(Backtrack, self).__init__(csp)
        self.__timeout = timeout
        self.__termination_flag = False
        self.__lock = Lock()
        self.num_constrains_added = 0

    def backtrack(self):
        """
        backtrack algorithm for the given csp problem.
        :return: True if assignment is possible. False otherwise
        """
        # Base case:
        if self.is_assignment_complete():
            if self.assignment_legit():
                return True
            return False

        # Body of recursion:
        var_name = None
        for var in self.csp.select_unassigned_variable():  # choose the variable that isn't assigned.
            if self.assignment[var] is None:
                var_name = var
                break
        # Notice, if this jumped: probably more variables in CSPHandler than there are in the assignment.
        assert (var_name is not None)

        for value in self.csp.order_domain_values(var_name):
            if self.csp.is_consistent(var_name, value):
                self.assign_value(var_name, value)

                self.__lock.acquire()  # Locking before checking shared variable.
                if self.__termination_flag:
                    self.__lock.release()
                    return False  # terminate run before recursion call.
                if self.__lock.locked():
                    self.__lock.release()

                res = self.backtrack()
                if not res:
                    self.remove_value(var_name)
                else:
                    return True
        return False

    def __run_backtrack(self, result):
        result[0] = self.backtrack()

    def backtrack_on_timer(self):
        """
        Runs backtrack over a set of time to run.
        :return:
        """
        result = [False]
        thread = Thread(target=Backtrack.__run_backtrack, args=(self, result))
        thread.start()
        # wait a timeout, if thread is already finished joins it with no waiting.
        thread.join(self.__timeout)
        if thread.is_alive():  # time out ended and the thread is still running - kill it..

            # acquire lock, and change exclusive variable termination flag.
            self.__lock.acquire()
            self.__termination_flag = True
            self.__lock.release()

            thread.join()  # awaits thread to stop
            print("Time out reached. Terminating solver.")
            result[0] = False
        return result[0]

    @staticmethod
    def __hard_constraint_satisfied():
        print("found satisfying assignment for hard constraints.")
        print("-----------------")

    def solve(self):
        """
        tries and solve for the csp problem while adding more and more constraints to the problem.
        Current assignment must be reseted before call!
        :return: False if there isn't a solution, True otherwise.
        """
        print("******Starting Backtrack******")
        backtrack_succeed = self.backtrack_on_timer()  # try to satisfy hard constraints.
        if not backtrack_succeed:
            if self.__termination_flag:
                return magicNums.TIMEOUT_HARD_CONSTRAINT
            return magicNums.FAILED
        self.__hard_constraint_satisfied()

        i = 1
        current_assignment = self.assignment
        add_const = self.csp.add_constraint()
        while add_const:  # while we can still add constraints - continues # TT
            print("Adding soft constraint number:", i)
            self.csp.restore_csp_handler()  # restores csp for re run.
            current_assignment = self.assignment
            self.reset_assignment()
            backtrack_succeed = self.backtrack_on_timer()
            if not backtrack_succeed:
                break
            add_const = self.csp.add_constraint()
            i += 1

        # if backtrack_succeed and not add_const:  # TF
        #     # RETURN SUCCESS. -> we manage to do everything, and the self.assignment is okay.
        #     pass
        #
        # if not backtrack_succeed and add_const:  # FT
        #     # self.assignment = prev_assignment
        #     # return the cause of no satisfaction.
        #     pass
        #
        # else:  # FF
        #     # we failed in adding the constraint, and we failed the last. (after  last possible soft constraint)
        #     pass

        self.num_constrains_added = i
        if not backtrack_succeed and add_const:  # FT
            self.num_constrains_added -= 1
            self.assignment = current_assignment
            print("couldn't satisfy constraint.")
            print("--------")
            self.print_report()
            if self.__termination_flag:
                return magicNums.TIMEOUT
            return magicNums.SOFT_FAIL

        elif not backtrack_succeed and not add_const:  # FF
            self.num_constrains_added -= 1
            self.assignment = current_assignment
            return magicNums.SOFT_FAIL

        # TF
        else:
            print(self.assignment)
            print(current_assignment)
            self.print_report()
            return magicNums.SUCCESS

    def get_num_soft_constraints_added(self):
        return self.num_constrains_added
