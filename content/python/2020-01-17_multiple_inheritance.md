---
Title: Multiple Inheritance in Python
xref: python-multiple-inheritance
Tags: Python
description: Multiple inheritance is a very powerful core concept of Python. In this article you will learn how to use it and what to look out for.
sources:
    https://en.wikipedia.org/wiki/Multiple_inheritance#/media/File:Diamond_inheritance.svg
status: published
---

## The basics

Inheritance is one of the basic concepts of Object Oriented Programming. 
The most basic example would be something like this:

```python
class Parent:
    def __init__(self, x):
        self.x = x
    
    def __str__(self):
        return f"x: {self.x}"


class Child(Parent):
    pass


# Create a parent and a child object
parent = Parent("Will")
child = Child("Jaden")

# And print both objects
print(parent)
print(child)
```

In this example the `Child` class inherits from the `Parent` class, which means it will inherit all it's functionality.
If we run this code it will print the following to the console:

```
Will
Jaden
```

## Introduction to multiple inheritance

Python has a very powerful concept of multiple inheritance, which allows a developer to create multiple base classes
that a single child class inherits from. There are some thing to look out for though, but I'll get to that later.

```python
class Parent1:

    @property
    def x(self):
        return "X"


class Parent2:
    @property
    def y(self):
        return "y"


class Child(Parent1, Parent2):

    @property
    def z(self):
        return "Z"

if __name__ == '__main__':
    child = Child()
    print(child.x)
    print(child.y)
    print(child.z)
```

Easy as that. You can let the child class inherit from as many base classes as you want. 
When we run the code above we get the following output:

```
X
Y
Z
```

## `__init__` parameters with multiple inheritance

The example above is nice, but wouldn't it be nicer if we could set the names ourselves?
This can be done with parameters we pass to the `__init__` method.

In the next example the properties are converted to attributes, and the names are passed in as parameters.
All three classes also got a `__init__` method, and what's interesting is what happens with the `Child` class 
where we set the `y` attribute, and call `__init__` on both `Mom` and `Dad`.

```python
class Parent1:
    def __init__(self, x):
        self.x = x

class Parent2:
    def __init__(self, y):
        self.y = y

class Child(Parent1, Parent2):
    def __init__(self, x, y, z):
        Parent1.__init__(self, x)
        Parent2.__init__(self,y)
        self.z = z

if __name__ == '__main__':
    child = Child("Jada", "Will", "Jaden")
    print(child.x)
    print(child.y)
    print(child.z)
``` 

This will print the same result, but in this case we were able to pass in the names as parameter values.

```
Jada
Will
Jaden
```

## Gotchas of multiple inheritance

Even though multiple inheritance in Python looks very simple and is in fact one of Pythons most powerful features,
it comes with a couple of gotchas. If you misuse or abuse it, then it will lead to maintenance hell.

So here are a couple of things to look out for when using multiple inheritance.

### Abusing multiple inheritance

Multiple inheritance should be looked at like any other design pattern. 
So use it with care and only when applicable. I found that there are very ofter much better solutions.

### Resolution order

When the child class inherits from multiple base classes with the same attributes or methods,
Python uses a resolution order to figure out the class it will use the method from.

When two or more parent classes are used that have the same methods or attributes,
then they will be resolved from left to right.

So in the example below `Child` inherits from `Parent1` and `Parent2` which both have a method called `a(self)`. 

```python
class Parent1:
    def __init__(self, x):
        self.x = x

    def a(self):
        print(self.x)

class Parent2:
    def __init__(self, y):
        self.y = y

    def a(self):
        print(self.y)

class Child(Parent1, Parent2):
    def __init__(self, x, y):
        Parent1.__init__(self, x)
        Parent2.__init__(self,y)

if __name__ == '__main__':
    child = Child("Jada", "Will")
    print(child.a())
```

Because `Parent1` is used first, his method will be used. So when we run this code we will get the following output:

```
Jada
```

If you want to know the method resolution order, you can always call `.__mro__` or `.mro()` on a class.

```sh
>>> Child.__mro__
(<class '__main__.Child'>, <class '__main__.Parent1'>, <class '__main__.Parent2'>, <class 'object'>)
>>> Child.mro()
(<class '__main__.Child'>, <class '__main__.Parent1'>, <class '__main__.Parent2'>, <class 'object'>)
```

### The diamond problem

The __diamond problem__ or __deadly diamond of death__ occurs 
when multiple parent classes inherit from the same base class 
which makes the inheritance graph look like a diamond.

![Diamond Problem]({static}/img/diamond_inheritance.png)

When both class `A` and class `B` or `C` implemented the same methods,
this will lead to a lot of confusion. It will work, but it will also lead to maintenance hell.

!!! warning
    Always avoid the diamond problem.

#### The diamond problem example

Because this one is so important I wanted to elaborate with an example:

```python
class GrandParent:
    def a(self):
        print("Diamond problem is bad, mmmmkay")


class Parent1(GrandParent):
    def __init__(self, x):
        self.x = x

    def a(self):
        print(self.x)


class Parent2(GrandParent):
    def __init__(self, y):
        self.y = y

    def a(self):
        print(self.y)


class Child(Parent1, Parent2):
    def __init__(self, x, y):
        Parent1.__init__(self, x)
        Parent2.__init__(self, y)


if __name__ == '__main__':
    child = Child("Jada", "Will")
    print(child.a())
```

In this example both `Parent1` and `Parent2` inherit from `GrandParent` and both `GrandParent` and `Parent2` have 
a method called `a(self)`. How do you think this will be resolved? 
Your first thought might be to follow the _left to right_ rule I used before. So let's take a look.

```sh
print(Child.__mro__)
(<class '__main__.Child'>, <class '__main__.Parent1'>, <class '__main__.Parent2'>, <class '__main__.GrandParent'>, <class 'object'>)
```

Now we can see that it's first `Parent1` as you would expect, but next it's `Parent2` and lastly `GrandParent`,
which might not be what you expected.

## Conclusion

Multiple inheritance is one of the most powerful features of Python. 
Once you know how it works and when to use it you can do amazing things with it.
But on the other hand it can lead to some major issues you need to be aware of.
