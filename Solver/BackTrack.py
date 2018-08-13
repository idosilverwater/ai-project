from Solver.BaseSolver import *

from threading import Thread, Lock


class Backtrack(Solver):
    """
    a solver class, applies backtrack solving algorithm when solve class is initialized.
    """

    def __init__(self, csp, timeout=30):
        """
        excepts a csp problem initialized.
        """
        super(Backtrack, self).__init__(csp)
        self.__timeout = timeout
        self.terminate_flag = False
        self.__lock = Lock()

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
        assert (var_name is not None)  # TODO remove after tests. (sanity check)

        for value in self.csp.order_domain_values(var_name):
            if self.csp.is_consistent(var_name, value):
                self.assign_value(var_name, value)
                self.__lock.acquire()
                if self.terminate_flag:
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
            self.terminate_flag = True
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
        :return: False if there isn't a solution, True otherwise.
        """
        backtrack_succeed = self.backtrack_on_timer()  # try to satisfy hard constraints.
        if not backtrack_succeed:
            self.reset_assignment()  # resetting the assignment.
            return False
        self.__hard_constraint_satisfied()

        i = 1
        current_assignment = self.assignment
        add_const = self.csp.add_constraint()
        while backtrack_succeed and add_const:  # while we can still add constraints - continues
            print("Adding soft constraint number:", i)
            self.csp.restore_csp_handler()  # restores cso for re run.
            current_assignment = self.assignment
            self.reset_assignment()
            backtrack_succeed = self.backtrack_on_timer()
            i += 1
            add_const = self.csp.add_constraint()

        if not backtrack_succeed and add_const:
            print("couldn't satisfy constraint.")
            print("--------")
        self.assignment = current_assignment
        return True
