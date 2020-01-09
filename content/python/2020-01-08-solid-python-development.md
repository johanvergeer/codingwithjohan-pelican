---
Title: Solid Python Development
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

## Single Responsibility Principle with Python

