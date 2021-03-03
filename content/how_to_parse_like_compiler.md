Title: How To Parse Like A Compiler - Part I
Date: 2020-03-21 05:47
Modified: 2020-03-21 05:47
Category: Python
Slug: python-parse-compiler-part1
Tags: python, lark, grammar
Authors: Rishi Maker
Summary: Python Lark Part 1

This week I helped a friend parse a file consisting of Poker hand histories.
Instead of creating a hand parser, I wrote a small grammar and used a Python module called Lark to parse the file into a syntax tree. An integration like this used to be tedious in the past, but modern languages allow you to develop such a solution rather quickly.


The aim of this blog is to highlight how to use context free grammars as an alternative to hand parsers. In part I, I will focus on parsing and the next part will be on transformation.

This is a rather deep topic and I am by no means a language expert. I do not intend to cover theories of compilers, languages, parsers or syntax trees, but I will leave some practical references for those interested. I think that those with a basic understanding of context free grammars and Python can pick this solution, or you can read this again after doing a quick refresher on these topics.

## Summary


- Problem Statement
- Lark
- Context Free Grammar
- Earley vs LALR
- Building our grammar
- Moving to LALR
- Conclusion

For reference the entire project can be found [here](https://github.com/cmlzaGk/samplecodes/tree/main/parselikeacompiler1)

## Problem Statement

We will attempt to parse a poker hand history file.

Each hand begins with a handnumber and is seperated by other hands by an empty newline.

A hand consists of the complete state information of the game. The players, their positions, starting stacks, actions they took on each poker street, followed by the results.

I hand-created a [sample file](https://github.com/cmlzaGk/samplecodes/blob/main/parselikeacompiler1/sample.txt) for this blog consisting of two hands.

The actual file that I parsed consisted a few hundred hands from one game.

Online Poker players can download these files from the sites they play in. Each site could have its own format and there are many paid Software online for parsing these files into databases.



## Lark

Lark is a python module that needs be installed using PIP.

As always, I recommend creating a virtual python environment before installing any module to keep your global module space on your machine clean.

```bash
C:\~>mkdir samplelark

C:\~>cd samplelark

C:\~\samplelark>python -m venv venv

C:\~\samplelark>.\venv\Scripts\activate

(venv) C:\Users\rishim\samplelark>pip install lark
Collecting lark
  Using cached https://files.pythonhosted.org/packages/69/8b/9418c0d24df0e8261c24e4b7218e80369f175c68eb3dfa119bc89d53f7fc/lark-0.11.1-py2.py3-none-any.whl
Installing collected packages: lark
Successfully installed lark-0.11.1
You are using pip version 19.0.3, however version 21.0.1 is available.
You should consider upgrading via the 'python -m pip install --upgrade pip' command.

(venv) C:\~\samplelark>

```

To understand how to use Lark, lets attempt to parse a nested list of words.

We will apply a simple grammar - a list consists of a list of single word or list, or it consists words and lists seperated by comma.

In different words, a list consists of a single word or list, followed by zero or more sequences of comma and a single list or word.

More formally

```text
list -> [listelem ("," listelem)*]
listelem: list|WORD
```

A complete Lark based parser looks like this:

```python
from lark import Lark
cfg = r'''
    list: "[" listelem ("," listelem)* "]"
    listelem: list|WORD

    %import common.WS
    %ignore WS
    %import common.WORD
'''

list_parser = Lark(cfg, start='list')
print(list_parser.parse('[test, me, [I, am, nested, [no, kidding]]]').pretty())
```

The parse() function above returned a syntax-tree.

The syntax tree is the parsed output, which we will explore in part II. In this part, we will just print a pretty output of the tree.

The output indicates, we were able to succesfully parse the word and capture all the terminals and non terminals that we defined.

```bash
(venv) C:\~\Samplelark>python nestedlist.py
list
  listelem      test
  listelem      me
  listelem
    list
      listelem  I
      listelem  am
      listelem  nested
      listelem
        list
          listelem      no
          listelem      kidding
```

This is the core principle of cfg parsing and allows us to cleanly implement a parser.


## Context Free Grammar

A Context Free Grammar (CFG) consists of four things:

1. Terminals : The terminals make up the actual content of a sentence. "[", "," , WORD are all terminals in our example. Note that WORD is in implemented as a regex and we could have defined it ourselves instead of using LARK predefinitions.  We will use our own regex Terminals in the actual solution.

2. NonTerminals : Phrase or a clause in grammar. eg. list, listelem

3. Production Rules : A mapping between NonTerminals and a set of Terminals and NonTerminals. eg. listelem: list|WORD is a production rule.

3. Start Elem: A special NonTerminal. This is essentially the rule we are trying to parse an input into.

The language is Context Free because its parsing does not depend on the actual value of a terminal.

It is not possible to create an XML parser using a CFG if the parser attempts to match the correctness of start element tag and end element tag. We can create a rule in CFG where a start<X> and end element</Y> exist and are well nested, but we cannot guarentee X == Y.

Such would be possible with a context sensitive grammar. In reality, CFG is still used for XML, but matching of X and Y is left to the next stage, the transformer (or the compiler).


## Parsers

The first stage of parsing is lexical analyzer where the input is converted into tokens, however the actual parsing is performed by the parser.

There are two main types of parsers supported by Lark - Earley and LALR.

Earley can parse any grammar that we can write in CFG because it performs backtracking. Essentially, if a rule does not match, it can backtrack and use the next available rule.

Such operation is clearly very expensive and is infact cubic in complexity. Unless performance is a major consideration, use Earley to begin with. It is infact default parser for Lark.

If you are able to construct grammar in a manner where a parser can deterministicly make a decision on which rule to use next, you could use the LALR parser.

LALR parses in linear time and fails fast.

In a nutshell, LALR is a shift-reduce parser and that can parse a language does not have any conflicts between shifting and reducing.

I will give an example of such a conflict later.

By definition, Earley can parse more languages than LALR, but IMO most parsing problems in day to day life can be parsed using LALR.

Lark will help you understand which particular construct of your grammar creates a conflict, and if you are able to modify your grammar, you should move to LALR.


## Building a Grammar

For reference the sample input file can be found [here](https://github.com/cmlzaGk/samplecodes/blob/main/parselikeacompiler1/sample.txt)

I started building the parser intitutively to begin with by reading the file.

I parsed one hand first, section by section, expanding my grammar.

The roadblock here were the statements begining with player names because the player names could be one or more words.

```text
foobar checks
Mr Foo bets 12
```

This meant the lexical scanner will not be able to identify the player. If I used a rule such as a "oneword|twowords" to identify the player, the lexer will not be able to disambiguate between 'foobar checks' or 'Mr. foo'.

Eventually, I decided that since I was parsing games with static list of player names, I will just include player name as grammar terminals.

This allows me to be context free.

I can also create a pre-parser that will generate the player names as terminals before I start the main parser, so I was not very concerned about broader application of this approach.

As I started parsing more and more hands in the file, I encountered new conditions which I incorporated into my grammar and my final main rule took a form that was able to parse the entire file.

```text
    handhistory: handdesc when table seats posts preflop [flop] [turn] [river] [boards] summary winner [shows]
```

For reference the earley parser implementation can be found [here](https://github.com/cmlzaGk/samplecodes/blob/main/parselikeacompiler1/hhparser.py)


## Moving to LALR

The above implementation was Earley and was visibly slow. I decided to move my parser to LALR.

It is pretty straight-forward in Lark to move to LALR. I just needed to pass the parameter parser='lalr' to Lark constructor.

However, my parser broke immediately, and I noticed that asking the lexer to ignore whitespace meant that new statements were not easily recognized.

I conclude that Earley was doing a lot of backtracking between rules because of ignoring whitespace. I made the parser strict about whitespace and I was able to parse most of the structures.

I ran into a conflict resolution with my Non Terminal called 'shows'.

```text
    handhistory: handdesc when table seats posts preflop [flop] [turn] [river] [boards] summary winner [shows]
    shows: showdown*
```

This directive happens when a player shows a hand. Square brackets in terminals indicate that the NonTerminal appears zero or one times.

The asterix symbol in the NonTerminal is a regular regex symbol indicating zero or more times.

Hence when there were no occurrences of shows, the parser didn't know which production rule to use, because both the rules matched.

An LALR parser needs to know with certainty whether to shift the square bracket rule or to reduce with the second production.

I resolved this by restructuring shows to have one or more occurences.

Hence 'shows' is only reduced when there is actually a showdown directive. If there is no showdown, a shift is performed.

The complete LALR parser implementation can be found [here](https://github.com/cmlzaGk/samplecodes/blob/main/parselikeacompiler1/hhparser_lalr.py)


## Conclusion

At the end the complete parser was very quick to create and I was able to develop it organically and intituively.

I will admit that it is difficult to understand error conditions during building, and it requires a fair bit of step by step parsing.

The overall process is very quick because at the end of the day, the code is concise and quite frankly easier to understand

I have used this in parsing poker ranges and poker hand histories.

In the next part, I will explain the transformation technique. Afterall, the canonical use of parsing is in converting data from one form to another.
