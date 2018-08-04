from WorkersCSP import create_workers_csp
from Degree import *  # TODO(Noy): To remove.
from BackTrack import *
from WalkSat import *
from LeastConstrainingValue import *

BACKTRACK = 'b'
WALKSAT = 'w'

algorithms = {'b': Backtrack, 'w': WalkSat}

def worker_solve(filename, algo, preferences):
    csp = create_workers_csp(filename, preferences)
    algorithm = algorithms[algo](csp)
    if algorithm.solve(): # TODO need the calling for the function to be generic (instead of "backtrack" "run")
        print("Satisfiable")

        dic = algorithm.get_assignment()

        print(1, algorithm.get_num_satisfied())
        print(2, len(algorithm.constraints))

        for v in dic:
            print(v, ":", dic[v])

    else:
        print("Unsatisfiable")
    print("Done")

if __name__ == "__main__":
    worker_solve("examples/example1.csp", WALKSAT, True)

