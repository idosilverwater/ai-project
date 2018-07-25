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
    import time

    csp = create_workers_csp("/Users/yonatanweiss/PycharmProjects/ai-project/examples/example1.csp")
    # print(csp.is_consistent('Sarah 6 1', 'False'))
    assignment = {name: None for name in csp.variables.keys()}
    for k in assignment:
        assignment[k] = 'False'
        break
    a = time.time()

    csp.check_assignment(assignment)
    print(time.time() - a)
    # print(c)
