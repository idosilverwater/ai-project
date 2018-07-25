from WorkersCSP import create_workers_csp
from Degree import *  # TODO(Noy): To remove.

if __name__ == "__main__":
    # csp = create_workers_csp("examples/example1.csp")
    # print(csp.constraints.get_all_constraints())

    #########
    # TESTS #
    #########
    # csp = create_workers_csp("examples\example1.csp")
    # h = Degree(list(csp.variables.values()))
    # print(h.get_sorted_variables())

    ##############
    # J check ups:
    ##############
    csp = create_workers_csp("/Users/yonatanweiss/PycharmProjects/ai-project/examples/example1.csp")
    # print(csp.is_consistent('Sarah 6 1', 'False'))
    csp.assign_variable('Sarah 6 1', 'False')
    for name in ['Ziv 6 1', 'Noga 6 1', 'David 6 1', 'Benzion 6 1']:
        # print(csp.is_consistent(name, 'False'))
        csp.assign_variable(name, 'False')

    # print(c)
