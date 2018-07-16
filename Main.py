from WorkersCSP import create_workers_csp


if __name__ == "__main__":
   csp = create_workers_csp("examples/example1.csp")
   print(csp.constraints.get_all_constraints())
