---
Title: Python Dependency Injection Frameworks
xref: python-dependency-injection-frameworks
Tags: Python,Dependency Injection
description: This article looks into Dependency Injection with Python and the frameworks available for you.
status: published
sources:
    <a href="https://martinfowler.com/articles/injection.html#InversionOfControl" target="_blank">Inversion of Control Containers and the Dependency Injection pattern by Martin Fowler</a>
    <a href="http://tutorials.jenkov.com/dependency-injection/index.html" target="_blank">Dependency Injection by Jakob Jenkov</a>
    <a href="https://en.wikipedia.org/wiki/Dependency_injection" target="_blank">Dependency Injection on Wikipedia</a>
---

Even though the usage of Dependency Injection is not as common in the Python community as it is in the C# or Java communities, 
it is still a very powerful way to implement the [xref:python-dependency-inversion-principle title="Dependency Inversion Principle"].
Thankfully there are several packages available to us that provide us with a dependency injection implementation, 
which I will discuss in this article.


Dependency injection is a style of object configuration in which an objects fields and collaborators are set by an external entity. 
In other words objects are configured by some other object. 
When you are using Dependency injection an object is no longer responsible for configuring itself.
This is taken care of by the container instead. This might be a bit abstract so let's start with a simple example:

## Simple dependency injection example

```python
import imaplib


class EmailClient:
    def receive(self, username: str, password: str) -> List[str]:
        server = imaplib.IMAP4('localhost', 993)
        server.login(username, password)
        server.select('INBOX')
    
        result, data = server.uid('search', None)

        # Process result and data
```

In this example we have an `EmailClient` that uses `imaplib` to receive email messages.
The problem we have here is the fact we hardwired `imaplib.IMAP4` into the email client 
so we cannot use another protocol like `IMAP_SSL`.

We can solve this with dependency injection. For this we make use of Pythons duck typing. 
First we create a [Protocols](https://mypy.readthedocs.io/en/stable/protocols.html#simple-user-defined-protocols)
we can use to define what we expect.

```python
from typing_extensions import Protocol

class EmailReceiver(Protocol):
    def login(self, user: str, password: str): ...
    def select(self, mailbox='INBOX', readonly=False): ...
    def uid(self, command, *args): ...
```

Next we change the EmailClient so it takes a `ReceivingEmailProtocol` and uses that to connect

```python
class EmailClient:
    def __init__(self, email_receiver: EmailReceiver):
        self.server = email_receiver

    def receive(self, username: str, password: str) -> List[str]:
        self.server.login(username, password)
        self.server.select('INBOX')

        result, data = self.server.uid('search', None)

        # Process result and data
```

Lastly we create a new instance for the email receiver and start receiving email

```python
receiver: EmailReceiver = imaplib.IMAP4_SSL("localhost", 993)
client = EmailClient(receiver)
results = client.receive("codingwithjohan@gmail.com", "mysupersecretpasswd")
```

As you can see, in this case we are using the `IMAP4_SSL` instead of just `IMAP` 
without having to change the `EmailClient`.

## Why would you need a dependency injection framework?

If you've been researching Dependency Injection frameworks for python, you've no doubt come across this opinion:

> You dont need Dependency Injection in python. You can just use duck typing and monkey patching!

The position behind this statement is often that you only need Dependency Injection in statically typed languages.

To be honest, you don't really _need_ Dependency Injection in any language, whether it is statically typed or not. 
Dependency Injection can make you life a lot easier though when building large applications.
In my experience monkey patching should be kept to a minimum. I only use it in my tests, for example when I create mocks.

## Python dependency injection frameworks comparison

This chapter compares dependency injection frameworks for Python.

I have limited my research to dependency injection frameworks that are still maintained and have a decent number of users.

### Comparison items

To compare the available dependency injection frameworks I'll keep the following items in mind:

- Scoping: Scopes can be for example 'singleton', 'scoped' or 'per request'. How does the framework handle these scopes?
- Coupling to the framework: How tight is the framework coupled to your code. 
I usually tend to use frameworks that allow me to have very little or no coupling. 
- Testability: How easy is it to test our code when using the framework?

Next to these comparisons I have added some information about the project status and usage.

### Dependency Injector

Dependency Injector is a dependency injection microframework for Python created by ETS Labs. 
It was designed to be a unified and developer-friendly tool that helps implement 
a dependency injection design pattern in a formal, pretty, and Pythonic way.

#### Scoping

Dependency Injector works with providers to create scopes. 
They have [Factory Providers](http://python-dependency-injector.ets-labs.org/providers/factory.html) that creates a new instance on each call, 
a [Singleton Provider](http://python-dependency-injector.ets-labs.org/providers/singleton.html) that creates a new instance on the first call and returns that same instance every next call
and providers for [callables](http://python-dependency-injector.ets-labs.org/providers/callable.html), 
[objects](http://python-dependency-injector.ets-labs.org/providers/object.html) and [coroutines](http://python-dependency-injector.ets-labs.org/providers/coroutine.html).

Next to these they have [one more provider](http://python-dependency-injector.ets-labs.org/providers/dependency.html) that allows you to create libraries and let the user define the dependency.  

Score for scoping: [rating:5]

#### Configurability

Dependency Injector has many options to configure the application, which can all be done at the application top-level, 
or at each module. Dependency Injector does not use Python 3 type hints, which means you have to configure everything by hand.
So when you have a dependency that is used in a lot of places you have to pass it in everywhere.

Score for configurability: [rating:4]

#### Coupling

Dependency injector lets you configure your IoC container at the top level of your application or module. 
This makes it very flexible and loosely coupled. 

Score for coupling: [rating: 5]

#### Statistics

[![PyPI - License](https://img.shields.io/pypi/l/dependency_injector?style=for-the-badge&cacheSeconds=86400)](https://pypi.org/project/dependency-injector/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/dependency_injector?style=for-the-badge&cacheSeconds=86400)](https://pypi.org/project/dependency-injector/)
[![PyPI - Format](https://img.shields.io/pypi/format/dependency_injector?label=PyPI%20Format&style=for-the-badge&cacheSeconds=86400)](https://pypi.org/project/dependency-injector/)
[![PyPI - Status](https://img.shields.io/pypi/status/dependency_injector?label=PyPI%20Status&style=for-the-badge&cacheSeconds=86400)](https://pypi.org/project/dependency-injector/)
[![GitHub stars](https://img.shields.io/github/stars/ets-labs/python-dependency-injector?label=GitHub%20Stars&style=for-the-badge&cacheSeconds=86400)](https://github.com/ets-labs/python-dependency-injector)
[![GitHub forks](https://img.shields.io/github/forks/ets-labs/python-dependency-injector?label=Github%20Forks&style=for-the-badge&cacheSeconds=86400)](https://github.com/ets-labs/python-dependency-injector)
[![GitHub commit activity](https://img.shields.io/github/commit-activity/y/ets-labs/python-dependency-injector?style=for-the-badge&cacheSeconds=86400)](https://github.com/ets-labs/python-dependency-injector)
[![GitHub commit activity](https://img.shields.io/github/contributors/ets-labs/python-dependency-injector?style=for-the-badge&cacheSeconds=86400)](https://github.com/ets-labs/python-dependency-injector)

### Pinject

Pinject is a dependency injection container for Python created by Google. 
It's primary goal is to help developers assemble objects into graphs in an easy, maintainable way.

<ul>
<li class="pro"><i class="fas fa-plus-circle"></i> foo</li>
<li class="con"><img src="/img/test.svg#con"/> bar</li>
</ul>

[![PyPI - License](https://img.shields.io/pypi/l/pinject?style=for-the-badge&cacheSeconds=86400)](https://pypi.org/project/pinject/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/pinject?style=for-the-badge&cacheSeconds=86400)](https://pypi.org/project/pinject/)
[![PyPI - Format](https://img.shields.io/pypi/format/pinject?label=PyPI%20Format&style=for-the-badge&cacheSeconds=86400)](https://pypi.org/project/pinject/)
[![PyPI - Status](https://img.shields.io/pypi/status/pinject?label=PyPI%20Status&style=for-the-badge&cacheSeconds=86400)](https://pypi.org/project/pinject/)
[![GitHub stars](https://img.shields.io/github/stars/google/pinject?label=GitHub%20Stars&style=for-the-badge&cacheSeconds=86400)](https://github.com/google/pinject)
[![GitHub forks](https://img.shields.io/github/forks/google/pinject?label=Github%20Forks&style=for-the-badge&cacheSeconds=86400)](https://github.com/google/pinject)
[![GitHub commit activity](https://img.shields.io/github/commit-activity/y/google/pinject?style=for-the-badge&cacheSeconds=86400)](https://github.com/google/pinject)
[![GitHub commit activity](https://img.shields.io/github/contributors/google/pinject?style=for-the-badge&cacheSeconds=86400)](https://github.com/google/pinject)

### Injector

[![PyPI - License](https://img.shields.io/pypi/l/injector?style=for-the-badge&cacheSeconds=86400)](https://pypi.org/project/injector/)
[![Read the Docs](https://img.shields.io/readthedocs/injector?style=for-the-badge&cacheSeconds=86400)](https://injector.readthedocs.io/en/latest/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/injector?style=for-the-badge&cacheSeconds=86400)](https://pypi.org/project/injector/)
[![PyPI - Format](https://img.shields.io/pypi/format/injector?label=PyPI%20Format&style=for-the-badge&cacheSeconds=86400)](https://pypi.org/project/injector/)
[![PyPI - Status](https://img.shields.io/pypi/status/injector?label=PyPI%20Status&style=for-the-badge&cacheSeconds=86400)](https://pypi.org/project/injector/)
[![GitHub stars](https://img.shields.io/github/stars/alecthomas/injector?label=GitHub%20Stars&style=for-the-badge&cacheSeconds=86400)](https://github.com/alecthomas/injector)
[![GitHub forks](https://img.shields.io/github/forks/alecthomas/injector?label=Github%20Forks&style=for-the-badge&cacheSeconds=86400)](https://github.com/alecthomas/injector)
[![GitHub commit activity](https://img.shields.io/github/commit-activity/m/alecthomas/injector?style=for-the-badge&cacheSeconds=86400)](https://github.com/alecthomas/injector)
[![GitHub commit activity](https://img.shields.io/github/contributors/alecthomas/injector?style=for-the-badge&cacheSeconds=86400)](https://github.com/alecthomas/injector)

### Python Inject

[![PyPI - License](https://img.shields.io/pypi/l/inject?style=for-the-badge&cacheSeconds=86400)](https://pypi.org/project/Inject/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/inject?style=for-the-badge&cacheSeconds=86400)](https://pypi.org/project/Inject/)
[![PyPI - Format](https://img.shields.io/pypi/format/inject?label=PyPI%20Format&style=for-the-badge&cacheSeconds=86400)](https://pypi.org/project/Inject/)
[![PyPI - Status](https://img.shields.io/pypi/status/inject?label=PyPI%20Status&style=for-the-badge&cacheSeconds=86400)](https://pypi.org/project/Inject/)
[![GitHub stars](https://img.shields.io/github/stars/ivankorobkov/python-inject?label=GitHub%20Stars&style=for-the-badge&cacheSeconds=86400)](https://github.com/ivankorobkov/python-inject)
[![GitHub forks](https://img.shields.io/github/forks/ivankorobkov/python-inject?label=Github%20Forks&style=for-the-badge&cacheSeconds=86400)](https://github.com/ivankorobkov/python-inject)
[![GitHub commit activity](https://img.shields.io/github/commit-activity/y/ivankorobkov/python-inject?style=for-the-badge&cacheSeconds=86400)](https://github.com/ivankorobkov/python-inject)
[![GitHub contributors](https://img.shields.io/github/contributors/ivankorobkov/python-inject?style=for-the-badge&cacheSeconds=86400)](https://github.com/ivankorobkov/python-inject)


<!---

### Serum

[![PyPI - License](https://img.shields.io/pypi/l/serum?style=for-the-badge&cacheSeconds=86400)](https://pypi.org/project/Inject/)

[![PyPI - Downloads](https://img.shields.io/pypi/dm/serum?style=for-the-badge&cacheSeconds=86400)](https://pypi.org/project/Inject/)
[![PyPI - Format](https://img.shields.io/pypi/format/inject?label=PyPI%20Format&style=for-the-badge&cacheSeconds=86400)](https://pypi.org/project/Inject/)
[![PyPI - Status](https://img.shields.io/pypi/status/serum?label=PyPI%20Status&style=for-the-badge&cacheSeconds=86400)](https://pypi.org/project/Inject/)

[![GitHub stars](https://img.shields.io/github/stars/suned/serum?label=GitHub%20Stars&style=for-the-badge&cacheSeconds=86400)](https://github.com/suned/serum)
[![GitHub forks](https://img.shields.io/github/forks/suned/serum?label=Github%20Forks&style=for-the-badge&cacheSeconds=86400)](https://github.com/suned/serum)
[![GitHub commit activity](https://img.shields.io/github/commit-activity/y/suned/serum?style=for-the-badge&cacheSeconds=86400)](https://github.com/suned/serum)
[![GitHub commit activity](https://img.shields.io/github/contributors/suned/serum?style=for-the-badge&cacheSeconds=86400)](https://github.com/suned/serum)

## Dependency Injection Frameworks

### EnterPrython

- [EnterPython](https://github.com/Dobiasd/enterprython)
[![GitHub license](https://img.shields.io/github/license/Dobiasd/enterprython?style=flat)](https://github.com/Dobiasd/enterprython/blob/master/LICENSE)
[![GitHub license](https://img.shields.io/github/license/Dobiasd/enterprython)](https://github.com/Dobiasd/enterprython/blob/master/LICENSE)
[![GitHub forks](https://img.shields.io/github/forks/Dobiasd/enterprython?style=social&label=Fork&maxAge=2592000)](https://github.com/Dobiasd/enterprython)
[![GitHub stars](https://img.shields.io/github/stars/Dobiasd/enterprython?style=social&label=Star&maxAge=2592000)](https://github.com/Dobiasd/enterprython)

### Injectable

- [Injectable](https://github.com/allrod5/injectable)

### PyCDI

- [PyCDI](https://github.com/ettoreleandrotognoli/python-cdi)

### Dyject

https://dyject.com/
https://github.com/sumdog/dyject

### Ultra Light Weight Dependency Injector Python

https://github.com/liuggio/Ultra-Lightweight-Dependency-Injector-Python

### Springpython

https://github.com/springpython/springpython

--->
