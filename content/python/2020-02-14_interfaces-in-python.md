---
title: Interfaces in Python
slug: interfaces-in-python
xref: interfaces-in-python
Tags: python,interfaces,design patters,solid
author: Johan Vergeer
description: How to define interfaces in Python?
status: draft
---

Interfaces are supported in languages like Java, C# and Visual Basic and it is supported in C++ with abstract base classes.

Previously Python did not have any support for abstract base classes. We are able to use mixins but then we are using implementations. 
This would break the **Dependency Inversion Principle** which states that *one should depend upon abstractions, **not** implementations.*

Abstract base classes were defined in [PEP 3119](https://www.python.org/dev/peps/pep-3119/) and added to the Python language in versions 2.6 and 3.0.
These abstract base classes allow us to create abstractions like in the following example:

```python
from abc import ABC, abstractmethod


class MyAbstractBaseClass(ABC):

    @abstractmethod
    def an_abstract_method(self):
        pass
```

There is more you can do in an abstract base class. See the [documentation](https://docs.python.org/3/library/abc.html) to learn more about it.


Here is an implementation of `MyAbstractBaseClass`:

```python
class MyClass(MyAbstractBaseClass):

    def an_abstract_method(self):
        print("Hello from an implementation")
```
