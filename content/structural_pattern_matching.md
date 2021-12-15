Title: Structural Pattern Matching in Python
Date: 2021-12-15 01:42
Modified: 2021-12-15 01:52
Category: Python
Tags: python, python3.10
Slug: structural-pattern-matching
Authors: Rishi Maker
Summary: I discuss a new feature of Python 3.10 - Structural Pattern Matching

Python 3.10 was released in October 2021. 

A major highlight of the release is a new language feature called Structural Pattern Matching.  

Structural Pattern Matching was made famous in Scala but is found explicitly or implicitly in many languages.

It is a key paradigm of modern programming. 

In this blog, I will share my thoughts on this feature. 

I will cover why it is important, and how to approach it, but this is not a tutorial of the feature. 

I encourage reading [PEP 636](https://www.python.org/dev/peps/pep-0636/), which is a complete tutorial of the feature IMO.  

## Links

[PEP 636](https://www.python.org/dev/peps/pep-0636/) Structural Pattern Matching: Tutorial


[PEP 634](https://www.python.org/dev/peps/pep-0634/) Structural Pattern Matching: Specification

[PEP 635](https://www.python.org/dev/peps/pep-0635/) Structural Pattern Matching: Motivation and Rationale


## Contents

- What is Structural Pattern Matching?
- Motivation and Applications
- Pattern is not an expression
- Performance 
- Conclusion


## What is Structural Pattern Matching?

Structural Pattern Matching is a programming technique that takes a Subject and a set of Patterns and performs a pattern test on structure and state. 

A successful pattern match results in execution of a block of code corresponding to the Pattern. 

In typical usage, a side effect of pattern matching is name-binding, which live in enclosing scope. 

Python 3.10 implements this by introduction of a new statement called the “match” statement. Typical usage is as follows

```python
match subject_expr: 
    case pat1: 
        do_something()
    case pat2: 
        do_something_else()
```

In effect, match statement is a replacement for something like 

```python
if matches(expr1, pat1) : 
    do_something()
elif matches(expr2, pat2):
    do_something_else()

```

I will use “match statement" interchangeably with “Structural Pattern Matching” for the remaining sections of the blog. 


## Motivation and Applications

The match statement is usable in places where different blocks of code need to be executed based on the structure or state of the data. This means that it can be used in a lot of different places. 

The motivation to use a match statement is to simplify the code and make it more readable. 

The Subject is a regular python expression which can resolve to most sequences, dictionary or an object. Patterns can test for a match of length, type, specific index, key, attribute values, inheritance etc.

As a use case, a typical json handler checks data for states or properties and performs corresponding actions.

With match pattern, a handler for json data becomes very simple. 


```python

def process_media_blob(jsondata):
    match jsondata:
        case {'type':'audio', 'format' :'mp3', 'data': data}:
            render_mp3(data)

        case {'type':'video', 'format' : ('webm' | 'mkv') as videoformat, 'data': data}:
            render_video(data, videoformat)

        case _:
            raise MediaInputException('Usage: .... ')
```

The above match statement performed the necessary tests for presence of keys and their expected values elegantly. 

It also introduced ‘data’ and ‘format’ values to the scope namespace as ‘data’ and ‘videoformat’ respectively.  

The above is an example when the subject is a dictionary. [PEP 636](https://www.python.org/dev/peps/pep-0636/) exhausts use cases for data-structures like list, class, tuples etc. 


## Pattern is not an expression

An important thing to remember is that a Pattern is not a Python expression, even though under certain situations it looks exactly like a Python expression. 

A Pattern has completely different grammar rules from an expression. 

As an example below, `Point(x=0, y=1)` as an expression instantiates an object. The same as a Pattern statement is a rule check.


```python

class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

p = Point(x=0, y=1)

match p:
    case Point(x=0, y=1):
        print('p is an object of class Point with attributes x as 0 and y as 1')
    case _:
        print(' p is something else')
```

## Performance 

The match clause is functionally equivalent to “if .. elif .. “ tests. 

Even for potentially problematic patterns like sequences, constraints are in place to keep processing fast. 

E.g., The greedy operator ‘*’ in sequence patterns can only be used once in a pattern. 

The Pattern is a language specific rule and not a regular expression. 

Hence performance is equivalent to the earlier alternate patterns of "if .. elif ..". 


## Conclusion

Structural Pattern Matching is a very exciting addition to the Python language. 

Scala has already shown why this is a very popular and modern style of programming. 

Portions of python language already use the match clause to simplify existing code. 

Match statement is a language feature. Understanding it is not just useful for writing elegant code but also to read future Python code. 

