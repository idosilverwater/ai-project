# INTRO TO AI - FINAL PROJECT

## Authors

Ido-Moshe Silverwater

Noy SternLicht

Jonathan Weiss

## Usage
to run the program type in terminal: python3 Main.py <the file path you we wish to use> <all other optial parameters>
where optional parameters are:

```
positional arguments:
  filename              Problem filename

optional arguments:
  -h, --help            show this help message and exit
  --no-soft             With/out soft constraints
  --bt                  Solve using BackTrack algorithm
  --ws                  Solve using a WalkSAT algorithm modified for binary
                        domain CSP.
  --mc                  Use the Minimum Conflict domain heuristic. only when
                        using the Backtrack algoroithm
  --lc                  Use the Least Constraining Value domain heuristic.
                        only when using the Backtrack algoroithm
  --mr                  Use the Minimum Remaining Val variable heuristic. only
                        when using the Backtrack algoroithm
  --deg                 Use the Degree variable heuristic. only when using the
                        Backtrack algoroithm
  --sma                 Use the Soft Max Assignment heuristic for the soft
                        constraint heuristic
  --sn                  Use the Soft Name heuristic for the soft constraint
                        heuristic
  --sd                  Use the Soft Degree heuristic for the soft constraint
                        heuristic
  --bt-t BT_T           The maximum amount a backtrack session is allowed to
                        run. Default timeout is 30
  --bt-no-forward-check
                        Use forward checking in backtrack
  --max-flips MAX_FLIPS
                        Max flips to be used in the WalkSAT algorithm
  --walksat-alpha WALKSAT_ALPHA
                        In the WalkSAT algorithm exploration is determined by
                        the alpha value, alpha= 0 full exploitation, alpha=1
                        full exploration.
  --mws MWS             Max amount of workers per shift
```


## About the problem and the input file:

In a Workers CSP problem every worker gives out the list of shifts during the week
he would prefer working at, and if he wishes for exact amount of shifts he can add that too.

The file that contains the problem should look as follows.

For The workers David, Benzion, Rivka and Sarah.

the preferences:

* David In Tuesday wants to work in the second shift
* David In Thursday wants to work in the first shift
* Benzion In Sunday wants to work in the first shift
* Rivka In Wednesday wants to work in the first shift
* Rivka In Tuesday wants to work in the first shift
* Rivka In Sunday wants to work in the second shift
* Rivka In Monday wants to work in the second shift
* Benzion wants 3 shifts total

(As you can see Sarah hasn't any special requests)

shifts looks as follows: <day> <shift> where days are from 0 up to 4 (5 work days in a week) and shifts have at most 3 shifts
starting from 0 and up to 2.

The file for the program:
```
Domain:
True
False
Names:
David
Benzion
Rivka
Sarah
Preferences:
David 2 1
David 4 0
Benzion 0 0
Rivka 3 0
Rivka 2 0
Rivka 0 1
Rivka 1 1
MinimumWantedShifts:
Benzion 3

```
Notice that the last line should be empty.

##

This is our final project in the course "Introduction to Artificial Intelligence" in HUJI.

We built a Constraint Satisfaction Problem solver.

More specifically it gets workers preferences as to work hours, and tries to satisfy as many wishes as it can.
