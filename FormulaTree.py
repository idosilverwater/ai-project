class FormulaTree():
    """
    Generates and maneges a tree representing a boolean formula.
    """

    def __init__(self, constraints):
        """
        Creates a new tree object.
        """
        self.constraints = constraints
        self.root = self.__build_tree()

    def __build_sub_tree_of_clause(self):
        """
        This method builds a sub tree representing a single clause. A clause if of the form:
        "constraint1 & constraint2 & ....& constraint m"
        :return: A pointer to the root of this evergreen tree.
        """
        pass

    def __build_sub_tree_of_constraint(self):
        """
        This method builds a sub tree representing a single constraint. A constraint is of the form:
        "possible_assignment 1 | possible_assignment 2| .....| possible_assignment n
        :return: A pointer to this tree.
        """
        pass

    def __build_sub_tree_of_possible_assignment(self):
        """
        This method builds a sub tree represents a possible assignment. A possible assignment is of the form:
        literal1 & literal2 & literal 3 &.....& literal k
        :return: A pointer to this tree.
        """
        pass

    def __build_tree(self):
        """
        Builds a tree representing a formula
        :return: A pointer to the root of the tree.
        """
        pass

    class Node():
        """
        Inner class, only to use *inside* of this class.
        """
        def __init__(self, left, right, value=None, is_leaf=False):
            self.left = left
            self.right = right
            self.value = value
            self.is_leaf = is_leaf



