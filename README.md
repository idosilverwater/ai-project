# INTRO TO AI - FINAL PROJECT

## Authors
Jonathan Weiss

Noy SternLicht

Ido-Moshe Silverwater

## Usage

In a Workers CSP problem every worker gives out the list of shifts during the week
he would prefer working at.

The file that contains the problem should look as follows.

For The workers David, Benzion, Rivka, Sarah.

And the preferences:

* David In Tuesday wants to work in the second shift
* David In Thursday wants to work in the first shift
* Benzion In Sunday wants to work in the first shift
* Rivka In Wednesday wants to work in the first shift
* Rivka In Tuesday wants to work in the first shift
* Rivka In Sunday wants to work in the second shift
* Rivka In Monday wants to work in the second shift

(As you can see Sarah hasn't any special requests)

(Sunday gets 0, throw Saturday gets 6
Also First shift gets 0, throw Third shift that gets 2)

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
```

The file should be kept in the folder named examples.

##

This is our final project in the course "Introduction to Artificial Intelligence" in HUJI.

We built a Constraint Satisfaction Problem solver.

More specifically it gets workers preferences as to work hours, and tries to satisfy as many wishes as it can.
