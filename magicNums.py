"""
This module serves only as a magic number holder for the whole project.
"""
#
# the domain Values for bakery problems.
DOMAIN_TRUE_VAL = 'True'
DOMAIN_FALSE_VAL = 'False'

# Days and shifts for the bakery problem.
DAYS_IN_WEEK = 5  # number of days in a week.
SHIFTS_IN_DAY = 3  # number of shifts in a day.

# NAME Shift SEPARATOR : david<SEPARATOR>number<SEPARATOR>number:
VARIABLE_NAME_SHIFT_SEPARATOR = " "

# Boolean
AND = "&"
OR = "|"

# MAIN CHOOSE OPTION VALUES:
# Algo choose:
BACKTRACK = 'b'
WALKSAT = 'w'

# Heuristic Choose:
MIN_REMAINING_VAL = "min_remaining_val"
MIN_CONFLICT = "min_conflict"
LEAST_CONSTRAINING_VAL = "least_constraining_val"
DEGREE = "degree"

WORKER_PROB = 'w'

# Hard constraint Value
HARD_CONSTRAINT_VALUE = 0
SHIFTS_IN_WEEK_CONSTRAINT_VALUE = 1
BAKERY_SOFT_CONSTRAINT_VALUE = 2

# Types of soft constraints heuristic:
DEGREE_SOFT_CONSTRAINT_HEURISTIC_TYPE = "SOFT_DEGREE"
MAX_ASSIGNMENT_SOFT_CONSTRAINT_HEURISTIC = "SOFT_MAX_ASSIGNMENT"
NAME_SOFT_CONSTRAINT_HEURISTIC = "SOFT_NAME"
