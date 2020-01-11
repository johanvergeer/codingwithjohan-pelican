---
Title: How to write maintainable Python with SOLID principles
Tags: SOLID,Python
description: SOLID design Principles with Python. Why and How?
---

The __SOLID__ Principles were introduced by Uncle Bob (Robert C. Martin) in 2000. 
__SOLID__ is an acronym that represents the following five principles:

- [__Single Responsibility Principle__](https://drive.google.com/file/d/0ByOwmqah_nuGNHEtcU5OekdDMkk/view){:target="_blank"}: 
"A class should only have a single responsibility, that is, only changes to one part of the software's specification should be able to affect the specification of the class."
- [__Open Closed Principle__](https://drive.google.com/file/d/0BwhCYaYDn8EgN2M5MTkwM2EtNWFkZC00ZTI3LWFjZTUtNTFhZGZiYmUzODc1/view){:target="_blank"}: : 
"Software entities should be open for extension, but closed for modification."
- [__Liskov Substitution Principle__](https://drive.google.com/file/d/0BwhCYaYDn8EgNzAzZjA5ZmItNjU3NS00MzQ5LTkwYjMtMDJhNDU5ZTM0MTlh/view){:target="_blank"}: 
"Derived classes must be substitutable for their base classes."
- [__Interface Segregation Principle__](https://drive.google.com/file/d/0BwhCYaYDn8EgOTViYjJhYzMtMzYxMC00MzFjLWJjMzYtOGJiMDc5N2JkYmJi/view){:target="_blank"}: : 
"Make fine grained interfaces that are client specific."
- [__Dependency Inversion Principle__](https://drive.google.com/file/d/0BwhCYaYDn8EgOTViYjJhYzMtMzYxMC00MzFjLWJjMzYtOGJiMDc5N2JkYmJi/view){:target="_blank"}: : 
"Depend on abstractions, not on concretions."

[@UBPoOOP]

These descriptions are all nice and dandy, but it would be nice if we had some more practical examples.
That is what I will try to provide in this post. Let's start with the first one: 
__Single Responsibility Principle__ or __SRP__
    
    
!!! tip
    Always stay vigilant for __needless complexity__ when following these principles.
    Sometimes taking a simple approach can be the best one. As always, it depends on your use case.
    


## Single Responsibility Principle with Python

### What is a responsibility?

> In the context of the SRP we define a responsibility as a __"reason for change"__. 
If you can think of more than one reason to change a class, it has multiple responsibilities
and thus breaks the SRP.

The author only speaks of _classes_, but I would like to extend that with _functions_.

### Single Responsibility Principle advantages

Using the _Single Responsibility Principle_ has multiple advantages:

- Your code becomes more decoupled
- You get reusable code
- Your code is more testable.

### Single Responsibility Principle example

Let's make the _Single Responsibility Principle_ more clear with a simple example.

```python
class Book:
    def __init__(self, name: str, author: str, content: str):
        self.name: str = name
        self.author: str = author
        self.content: str = content

    def word_count(self, word: str) -> int:
        count = 0
        for w in self.content.split():
            if w == word:
                count += 1
        return count
```

Everything is fine it this first example. We instantiate the book, and we can get the count for a specific word.
Next we get a requirement from the product owner that the book should be printed. 
Since we understand exactly what the product owner means :wink: we print the books `content` to the console.

```python hl_lines="14 15"
class Book:
    def __init__(self, name: str, author: str, content: str):
        self.name: str = name
        self.author: str = author
        self.content: str = content

    def word_count(self, word: str) -> int:
        count = 0
        for w in self.content.split():
            if w == word:
                count += 1
        return count

    def print(self):
        print(self.content)
```

This example is obviously very simple, but it does show how the `Book` class now breaks the _SRP_.
The `Book` class is now responsible for maintaining it's state, and printing itself.

A better way would be to create a `print_book` function. (We don't need a class for this in Python. :smile:).
This makes sure the `Book` class keeps it's own responsibilities and we have a good way to print it. 

```python
def print_book(book: Book) -> None:
    print(book.content)
```

## Open Closed Principle with Python

> SOFTWARE ENTITIES (CLASSES, MODULES, FUNCTIONS, ETC.) SHOULD BE OPEN FOR EXTENSION,
> BUT CLOSED FOR MODIFICATION. [@BMOOSC]

Modules that conform to the open-closed principle have two primary attributes.

1. __They are “Open For Extension”__. This means that the behavior of the module can be extended. 
That we can make the module behave in new and different ways as the requirements of the application change, 
or to meet the needs of new applications.  
2. __They are “Closed for Modification”.__  The source code of such a module is inviolate. 
No one is allowed to make source code changes to it.

In practice we often see that modules are changed when new behavior is required,
which violates the _OCP_. We want to have fixed behavior but still be flexible. :confused:
Let's see how these oppositions can work hand in hand.

### Open Closed Principle example

In the previous example we ended up with the `print_book` function. 
The product owner was really happy with this function, since it can print the book to the console, 
but he would also like to print to a PDF file (for non-technical readers).

So we change the `print_book` function to create a pdf. 
To do this we add a flag parameter that indicates where the book should be printed to.

```python
def print_book(book: Book, whereto: str) -> None:
    if whereto == "console":
        print(book.content)
    elif whereto == "pdf":
        # printing to pdf
    else:
        raise ValueError("Invalid whereto value")
```

This function will work, but it also breaks the _OCP_. 
Let's say the product owner has an unimaginable idea and wants to print the book to paper (pun intended). 
We would have to change the function again. 
Therefore it would be much better to create smaller functions that do one thing.  

First we leave our original function the way it was, 
but to make it more explicit I want to deprecate the original function (for which I like to use 
a library called [Deprecated](https://github.com/tantale/deprecated){:target="_blank"}) and create a new function.

> Explicit is better than implicit. [@ZEN] 

```python
@deprecated
def print_book(book: Book) -> None:
    print(book.content)

def print_book_to_console(book: Book) -> None:
    print(book.content)

def print_book_to_pdf(book: Book) -> None:
    # printing to pdf
```

Now we have a couple of functions that adhere to the _OCP_. 
