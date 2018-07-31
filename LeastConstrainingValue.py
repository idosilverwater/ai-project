from DomainHeuristic import DomainHeuristic


# please notice that this doesn't need an init. the init is in it's parent class DomainHeuristic (ido)


class LeastConstrainingValue(DomainHeuristic):


    def neighbor_conflict(self, value):
        """
        This returns the amount of domain values that have been blocked off for the neighboring variables.
        :return:
        """
        neighbors = self.variable.get_neighbors()

        count = 0

        for neighbor in neighbors:
            if neighbor.get_value == None: # If the neighbor is already assigned
                neighbor.get_constraints()


        return count

    def get_order_domain(self):
        """
        Selects the value for variable, that is least constricting to variables neighbors.
        neighbors being other variables that share at least one constraint with it.
        :param variable: The variable we want to assign a value to.
        :return: A value for variable according to the heuristic
        """

        order = self.variable.get_domain()
        order.sort(key=self.neighbor_conflict)

        return order

        #
        # for d in order
        #
        # min_conflicted_value = possible_domain[0]
        # min_conflicts = self.neighbor_conflict(min_conflicted_value)
        #
        # for d in self.variable.domain:
        #     cur = self.neighbor_conflict(d)
        #     if min_conflicts > cur:
        #         min_conflicted_value = d
        #         min_conflicts = cur
        #
        # return min_conflicted_value
