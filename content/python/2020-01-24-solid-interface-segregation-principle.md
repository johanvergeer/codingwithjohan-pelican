---
Title: Interface Segregation Principle with Python
slug: python-interface-segregation-principle
xref: python-interface-segregation-principle
Tags: SOLID,Python,ISP,Interface Segregation principle
description: This article explains how you can use Protocols to apply the Interface Segregation Principle in Python.
status: published
sources: 
    <a href="https://hackernoon.com/interface-segregation-principle-bdf3f94f1d11" target="_blank">Interface Segregation Principle (Hackernoon)</a>
    
---

## Introduction

> The Interface Segregation Principle (ISP) deals with the disadvantages of “fat” interfaces. 
> Classes that have “fat” interfaces are classes whose interfaces are not cohesive. 
> In other words, the interfaces of the class can be broken up into groups of member functions. 
> Each group serves a different set of clients. Thus some clients use one group of member functions, 
> and other clients use the other groups. [@MartinISP]

The ISP is the fourth principle of Robert C. Martins SOLID principles. 

Being a Python developer you might think: "Why should I care about ISP. We don't have interfaces in Python!". 
But the fact is that you should care about ISP, because you can use it to create small pieces of functionality 
that you and other developers can use them wherever you need them without having to worry 
about other functionality that would come with fat interfaces.

The point is to find the right abstractions. 
And you know your abstractions are incorrect when a client depends on methods it doesn't use.

[TOC]

## Interface Segregation Principle example

When you read this example I assume you have a base knowledge of Python, dataclasses and type hinting.

In this example I will use items you might buy in an online book store. 

### First phase: just books

Let's begin with a class called `Book`.

```python
@dataclass
class Book:
    product_id: int
    title: str
    author: str
    page_count: int
    price: Decimal
    cover: str
```

Next we have a `Cart` class that the user can add books to.

```python
class Cart:
    def __init__(self):
        self._books: List[Book] = []

    def add_product(self, book: Book):
        self._books.append(book)

    @property
    def books(self) -> List[Book]:
        return self._books.copy()
```

Finally we create a `BooksPage` class that will show books to the user.

```python
class BooksPage:
    def __init__(self, books: List[Book]):
        self._books = books

    def show_books(self):
        return self._books
```

So far it has been very easy, but later on we'll find out there are some issues with the design.

### Second phase: adding dvd's

After a while the shop says he wants to start selling dvd's. 
This is something we did not anticipate on and the `Cart` class only accepts `Book` instances.

If we want to follow the ISP we have to create small interfaces that can be used by clients.

So what can we do? First of all we have to figure out which attributes of the `Book` are shared with other items 
that are sold in the store. In this case those attributes are `product_id`, `title` and `price`. 
All other attributes only apply to `Book`. 
We will use [Protocols](https://mypy.readthedocs.io/en/stable/protocols.html#simple-user-defined-protocols){:target="_blank"} 
to define the interfaces.

First we create a `Product` protocol class that contains all common attributes, 
and change the `Book` class which will now inherit from `Product`.

```python
@dataclass
class Product(Protocol):
    product_id: int
    title: str
    price: Decimal

@dataclass
class Book(Product):
    author: str
    page_count: int
    cover: str
```

Next we create the new DVD class, which also inherits from `Product`.

```python
@dataclass
class Dvd(Product):
    director: str
    duration: int
```

Now `Cart` will take in any `Product` instead of just books.
```python
class Cart:
    def __init__(self):
        self._products: List[Product] = []

    def add_product(self, product: Product):
        self._products.append(product)

    @property
    def products(self) -> List[Product]:
        return self._products.copy()
```

And we create a brand new page where the user can view DVD's. 

```python
class DvdsPage:

    def __init__(self, dvds: List[Dvd]):
        self._dvds: List[Dvd] = dvds

    def show_dvds(self) -> List[Dvd]:
        return self._dvds
```

So we segregated some attributes out of `Book` in to the `Product` protocol class, 
which allows use to add all products to the cart, and still let each of them have their own attributes. :sunglasses:

### Third phase: adding an e-book

After we added the dvd's the client comes back and says he wants to start selling e-books. 
We could just use `Book` but that has a `cover`, which doesn't apply to an e-book.
And e-books have a file size, which don't apply to a paper book.
This means we have to do another refactoring.

!!! info
     Refactoring is a very common and important part of software development.

`Product` stays the same, but we will add `Readable` and `ReadableProduct` Protocol classes.
`ReadableProduct` inherits from both `Product` and `Readable`.

```python
@dataclass
class Readable(Protocol):
    author: str
    page_count: int

@dataclass
class ReadableProduct(Product, Readable, Protocol):
    pass
``` 

Next both `Book` and `EBook` will inherit from `ReadableProduct`. `Book` has a `cover` and `EBook` has a `file_size`.

```python
@dataclass
class Book(ReadableProduct):
    cover: str

@dataclass
class EBook(ReadableProduct):
    file_size: int
```

Now all we have to do is change `BooksPage` to a `ReadableProductsPage` 
page which will be used to display both books and e-books. 

```python
class ReadableProductsPage:
    def __init__(self, readable_products: List[ReadableProduct]):
        self._readableProducts = readable_products

    def show_products(self) -> List[ReadableProduct]:
        return self._readableProducts
```

## Final thoughts

The Interface Segregation Principle is at it's core a very simple principle, 
but it might take a while to get a full grasp on it. 
Just like all other SOLID principles and design patterns ISP is not a silver bullet and it should be used when applicable.

I think `Protocol`s from the `typing` module are very useful when building interfaces. 
`Protocol`s are available since Python 3.8.0. 
If you want to use them in an earlier version you van use the 
[`typing_extensions` package](https://pypi.org/project/typing-extensions/){:target="_blank"} 

It is a very powerful principle that can help you to create clean and maintainable code,
but be sure you think about the correct abstractions when using it. 
