---
Title: Dependency Inversion Principle with Python
slug: python-dependency-inversion-principle
xref: python-dependency-inversion-principle
Tags: SOLID,Python,ISP,Interface Segregation principle
description: In the fifth article on the SOLID Principles with Python we'll look at the Dependency Inversion Principle.
status: published
sources: 
---

This is the fifth and last article on the SOLID Principles with Python. 
In this article we will look into the __D__ of __SOLID__ which stands for Dependency Inversion Principle.

Robert C. Martin states the following:

> * High level modules should not depend upon low level modules. Both should depend upon abstractions. 
> * Abstractions should not depend on details. Details should depend on abstractions.[@MartinDIP]

This article begins with a simple example to explain the Dependency Inversion Principle. 
After this simple example we will have a look at something you will encounter with 
more complex applications and how to overcome them.

[TOC] 

## Simple dependency inversion example

### Without Dependency Inversion Principle

Let's assume we have a class that can print books called `Printer`. Before printing the book, it should be formatted.
For this we will use a class called `Formatter`, which is used by `Printer`. 

```python
class Book:
    def __init__(self, content: str):
        self.content = content

class Formatter:
    def format(self, book: Book) -> str:
        return book.content

class Printer:
    def print(self, book: Book):
        formatter = Formatter()
        formatted_book = formatter.format(book)
        ... 
        # Printing the book
```

This example breaks the DIP because both `Printer` and `Formatter` depend on concretions, not abstractions.
This means we cannot use another `Formatter` or another type of `Book`.

### Create classes that use DIP

To fix this we have to create some abstractions and inject them wherever they are needed.
To accomplish this we can use [Protocols](https://mypy.readthedocs.io/en/stable/protocols.html#simple-user-defined-protocols){:target="_blank"} 
just like we did with the interface segregation principle.

First we will create a Protocol for classes that contain `content` which will be used to create a `Book`.

```python
@dataclass
class HasContentProtocol(Protocol):
    content: str

@dataclass
class Book(HasContentProtocol):
    def __init__(self, content):
        self.content = content
``` 

Next we create a formatter Protocol and create a concrete formatter.
Note the three dots (`...`) in the `format` method of `FormatterProtocol`. 

```python
@dataclass
class FormatterProtocol(Protocol):
    def format(self, has_content: HasContentProtocol):
        ...

class A4Formatter(FormatterProtocol):
    def format(self, has_content: HasContentProtocol):
        return has_content.content # This should obviously contain logic to format to A4 size.
```

### Creating the `Printer` class with the abstractions

Now we can inject the `FormatterProtocol` into the `Printer`

```python
class Printer:
    def __init__(self, formatter: FormatterProtocol):
        self.formatter = formatter

    def print(self, has_content: HasContentProtocol):
        formatted_book = self.formatter.format(has_content)
        ... 
        # Printing the book
```

### Printing the book

This way we don't have any dependencies on implementations, only on abstractions. 
So when we want to print a book to A4 we can just use the `A4Formatter` like this:

```python
book = Book("Amazing book content") # Book is a concretion of HasContentProtocol

formatter = A4Formatter()
printer = Printer(formatter)

printer.print(book)
```

And when we want to print the book to another format, we just create another concreate `FormatterProtocol`
and use it when instantiating the printer

## What about more complex applications?

When you start to build more complex applications the approach I described above would mean 
you have to pass dependencies all the way down the dependency hierarchy. 
This is something you really need to avoid since it will lead to maintenance hell.

### Dependency injection frameworks

One way to solve this issue is by using dependency injection frameworks. 
These frameworks will take care of the dependencies you need at runtime anywhere you need them. 

There are several dependency injection frameworks for Python that are still under active maintenance. 
I wrote an article about [xref:python-dependency-injection-frameworks title="Python Dependency Injection frameworks"]
which you can use to decide which one is best for your application.
