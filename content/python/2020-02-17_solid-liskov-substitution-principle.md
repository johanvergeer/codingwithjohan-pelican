---
title: Liskov Substitution Principle with Python
slug: solid-liskov-substitution-principle
xref: solid-liskov-substitution-principle
Tags: SOLID,Python,LSP,Liskov Substitution Principle
author: Johan Vergeer
description: This article explains how to apply the Liskov Substitution Principle in Python.
status: published
---

## Liskov Substitution Principle with Python

> Derived classes must be substitutable for their base classes.

The __Liskov Substitution Principle__ (LSP) was created by Barbara Liskov in 1987:

> What is wanted here is something like the following substitution property: If
for each object `o1` of type `S` there is an object `o2` of type `T` such that for all
programs `P` defined in terms of `T`, the behavior of `P` is unchanged when `o1` is
substituted for `o2` then `S` is a subtype of `T`. [@Liskov1987]

This is a whole mouth full, so I will try to explain it with an example. 

### Liskov Substitution Principle example

In this example we're going to let everyone in Middle Earth dance. 
First we create an abstract base class called `MiddleEarthInhabitant`, after which we create an `Human` and a `Hobbit`

```python
from abc import ABC

class MiddleEarthInhabitant(ABC):
    def dance(self):
        ...

class Human(MiddleEarthInhabitant):
    def dance(self):
        print("Going wild on the dance floor.")

class Hobbit(MiddleEarthInhabitant):
    def dance(self):
        print("Look at those big feet go.")

class Party:
    def __init__(self, guests: List[MiddleEarthInhabitant]):
        self._guests = guests

    def que_music(self):
        for guest in self._guests:
            guest.dance()        
```

Now when we want to create an `Orc`, which is also a Middle Earth inhabitant, we hit a problem: Orcs are fighters, not dancers.
This means the `LSP` would be violated.

In order to fix this we have to create a separate interface (Which is an abstract base class in Python)
and use that to create the party people.

```python
from abc import ABC

class MiddleEarthInhabitant(ABC):
    ...

class Dancer(ABC):
    def dance(self):
        ...

class Human(MiddleEarthInhabitant, Dancer):
    def dance(self):
        print("Going wild on the dance floor.")


class Hobbit(MiddleEarthInhabitant, Dancer):
    def dance(self):
        print("Look at those big feet go.")

class Party:
    def __init__(self, guests: List[Dancer]):
        self._guests = guests

    def que_music(self):
        for guest in self._guests:
            guest.dance()        
```

Now we can create an `Orc`, which still is a `MiddleEarthInhabitant`, but he doesn't have to dance.

