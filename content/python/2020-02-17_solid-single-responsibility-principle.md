---
title: Single Responsibility Principle with Python
slug: solid-single-responsibility-principle
xref: solid-single-responsibility-principle
Tags: SOLID,Python,SRP,Single Responsibility Principle
author: Johan Vergeer
description: This article explains how to apply the Single Responsibility Principle in Python.
status: published
---

## Single Responsibility Principle with Python

### What is a responsibility?

> In the context of the SRP we define a responsibility as a __"reason for change"__. 
If you can think of more than one reason to change a class, it has multiple responsibilities
and thus breaks the SRP.

### Single Responsibility Principle advantages

Using the _Single Responsibility Principle_ has multiple advantages:

- Your code becomes more decoupled
- You get reusable code
- Your code is more testable.

### Single Responsibility Principle example

Let's make the _Single Responsibility Principle_ more clear with a simple example.

We create a class called `Burglar`, which has a method called `steal`. This method breaks the __SRP__ because it doesn't just steal. 
It also puts on and removes the invisibility cloak, which might lead to all sorts of issues for the burglar.

```python
class Burglar:
    def __init__(self):
        self._artifacts = []

    def steal(self, artifact: str):
        print("Putting on the invisibility cloak.")
        print("Taking the artifact.")
        self._artifacts.append(artifact)
        print("Removing the invisibility cloak.")

bilbo = Burglar()
bilbo.steal("Arkenstone")
```

A better way would be to create separate methods that can be called when appropriate.

```python
class Burglar:
    def __init__(self):
        self._artifacts = []

    def steal(self, artifact: str):
        print("Taking the artifact.")
        self._artifacts.append(artifact)
    
    def cloak(self):
        print("Putting on the invisibility cloak.")

    def remove_cloak(self):
        print("Removing the invisibility cloak.")


bilbo = Burglar()
bilbo.cloak()
bilbo.steal("Arkenstone")
bilbo.remove_cloak()        
```

Now Bilbo can put on the cloak, walk in, steal the Arkenstone, 
walk out so he won't be seen by Smaug and remove the cloak.


