---
title: Python Dependency Injection Frameworks
slug: python-dependency-injection-frameworks
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
I also did not include any examples because each framework already provides very good examples.

### Dependency Injector

Dependency Injector is a dependency injection microframework for Python created by ETS Labs. 
It was designed to be a unified and developer-friendly tool that helps implement 
a dependency injection design pattern in a formal, pretty, and Pythonic way.

<ul class="procon pro">
<li>Very flexible</li>
<li>Factory Providers that creates a new instance on each call</li>
<li>Singleton Providers  that creates a new instance on the first call and returns that same instance every next call</li>
<li>Allows clients of your library to inject dependencies</li>
<li>Doesn't interfere with your existing code</li>
</ul>

<ul class="procon con">
<li>Doesn't use static type checking</li>
<li>No smart binding, which means you have to configure everything by hand</li>
</ul>

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

<ul class="procon pro">
<li>Uses implicit bindings for classes by default...</li>
<li>... and has many configuration options</li>
<li>Auto copying args to fields with decorators</li>
<li>Binding specs for more complex bindings</li>
<li>Binding specs for more complex bindings</li>
<li>Defaults to Singleton scope which creates a new object on the first call and reuses it after that ...</li> 
<li>... and it also supports Prototype scope which instantiates a new object on each call ...</li>
<li>... and you can create your own custom scopes</li>
<li>Possible to do partial injections.</li>
<li>No separate config file.</li>
</ul>

<ul class="procon con">
<li>Doesn't use static type checking</li>
<li>Some features require the use of decorators, which couples Pinject to your application.</li>
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

Python dependency injection framework, inspired by Guice which aims for simplicity, doesn't use a global state and uses static type checking.

<ul class="procon pro">
<li>Uses static type checking to resolve dependencies</li>
<li>Very simple to configure</li>
<li>Supports dataclasses</li>
<li>Helpers for testing</li>
<li>Creates a new object on each call by default ...</li>
<li>... and you can use `@singleton` ...</li>
<li>... and you can create your own scopes</li>
</ul>

<ul class="procon con">
<li>It looks like it forces the use of decorators, which couples Injector heavily to your application</li>
</ul>

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

Dependency injection the python way, the good way. Not a port of Guice or Spring.

<ul class="procon pro">
<li>Uses static type checking to resolve dependencies</li>
<li>Very simple to configure</li>
<li>Integrates with Django</li>
<li>Partial injection</li>
<li>Helpers for testing</li>
<li>Binding of simple keys. (e.g. name and email)</li>
</ul>

<ul class="procon con">
<li>Python Inject is coupled heavily into your application</li>
</ul>

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
