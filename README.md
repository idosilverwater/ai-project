# INTRO TO AI - FINAL PROJECT

## Authors
Jonathan Weiss

Noy SternLicht

Ido-Moshe Silverwater

## Usage

In a Workers CSP problem every worker gives out the list of shifts during the week
he would prefer working at.

The file that contains the problem should look as follows.

For The People Name1, Name2, Name3, Name4
And the constraints:
Name1 In Tuesday wants to work in the second shift
Name1 In Thursday wants to work in the first shift
Name2 In Sunday wants to work in the first shift
Name3 In Wednesday wants to work in the first shift
Name3 In Tuesday wants to work in the first shift
Name3 In Sunday wants to work in the second shift
Name3 In Monday wants to work in the second shift

(As you can see Name4 hasn't any special requests)
(Sunday gets 0, throw Saturday gets 6
Also First shift gets 0, throw Third shift that gets 2)

```
Domain:
True
False
Names:
Name1
Name2
Name3
Name4
Constraints:
Name1 2 1
Name1 4 0
Name2 0 0
Name3 3 0
Name3 2 0
Name3 0 1
Name3 1 1
```

The file should be kept in the folder named examples.

##

This is our final project in the course "Introduction to Artificial Intelligence" in HUJI.

We built a Constraint Satisfaction Problem solver.

More specifically it gets workers preferences as to work hours, and tries to satisfy as many wishes as it can.
