Title: Creating Matrix Rain On Good Old Terminals
Date: 2021-12-04 05:47
Modified: 2020-03-21 05:47
Category: Python
Slug: matrix-rain
Tags: python, grammar
Authors: Rishi Maker
Summary: Matrix Rain

Matrix 4 is releasing this month. Matrix is one of the most influential movies of all time.

A feature of the movie was the Matrix Rain.

I went retro this week and scripted the Matrix Rain console application. 

In this blog I will go over how to create matrix rain on a terminal. 

The command line output of the program can be viewed on [Youtube](https://www.youtube.com/watch?v=uJwc8n0OnQE)


## Summary


- What is Matrix Rain?
- Approach
- Character Set
- Flickering Rain
- Enable VT100 mode on Windows 10+
- The Curses Library
- Conclusion

For reference the entire project can be found [here](https://github.com/cmlzaGk/mtrixrain/)

## What is Matrix Rain?

[Matrix Rain](https://en.wikipedia.org/wiki/Matrix_digital_rain) is a visualization of characters falling downwards on a console in the form of rain. 


## Approach

The overall approach is naive 

* Prepare a buffer
* Repeat forever
    * Clear the screen
    * Render the buffer
    * Sleep for some time (refresh rate)
    * Update the buffer so that all horizontal lines move downwards

This works for most part, except for some challenges that I will take about, as well as how to overcome them.


## Character Set

The Unicode characters and font-family to choose in a terminal-based matrix rain is very important. Two conditions need to be met. 

All characters should be printable on the terminal, and the font-family should be Mono-spaced.

Mono-spaced means that the letters occupy same amount of horizontal space. 

If this property is not true, then the lines that we print will be scattered, and there will not be an appearance of a vertical flow.

The default font "Consolas" on Windows terminal is Mono-spaced and meets the requirement. 

I did a manual test to check which Unicode ranges can be displayed on the screen.

I built this range manually because I noticed that I could not rely isprintable() method of string in python. 

e.g. My console was unable to print 0x16ef, but isprintable() returned True. 


```python
### https://stackoverflow.com/questions/1477294/generate-random-utf-8-string-in-python

include_ranges = [
    ( 0x0023, 0x0026 ),
    ( 0x0028, 0x007E ),
    ( 0x00A1, 0x00AC ),
    ( 0x00AE, 0x00FF ),
    ( 0x0100, 0x017F ),
    ( 0x0180, 0x024F ),
    ( 0x2C60, 0x2C7F ),
    ( 0x16A0, 0x16F0 ),
    ( 0x0370, 0x0377 ),
    ( 0x037A, 0x037E ),
    ( 0x0384, 0x038A ),
    ( 0x038C, 0x038C ),
]


# Used in manual testing
for current_range in include_ranges :
    for code_point in range(current_range[0], current_range[1] + 1):
        print('0x{:4x} {} {}'.format(code_point, chr(code_point), chr(code_point).isprintable()))


# Once include_ranges is determined
ALPHABETS = [
    chr(code_point) for current_range in include_ranges
        for code_point in range(current_range[0], current_range[1] + 1)

```

## Flickering Rain

I am trying to build Matrix Rain using standard library. With that restriction in place, the interesting part is how to clear the terminal.

The first approach is to invoke a shell call, and call 'cls' on windows, and that is not a bad start.

![Alt Text](/images/flickering_matrix.gif)

As can be seen, we have achieved a rain effect, but this level of flickering is unacceptable.

This flickering occurs, because of the time it takes to do an inter-process call, clear and then display our content from another process.

We have to do better.

## Enable VT100 mode on Windows 10+

The flicker occurs because of the delay within the refresh because clear screen happens in another process. 

There is no standard API to clear the screen. However, starting [Windows 10](https://superuser.com/questions/413073/windows-console-with-ansi-colors-handling/1050078#1050078), console got support for VT100 escape sequences that can be sent to the console.

It can be enabled using system libraries, however I enabled it by setting a DWORD 'VirtualTerminalLevel' on registry key 'HKEY_CURRENT_USER\Console' to 0x1. 

The following code can test if the console understands VT100 escape sequencing. 

```python
import sys
# send the escape sequence to clear the screen for VT100 compatible console
sys.stdout.write('This should not be visible\033[H\033[JThis should be first line of the screen')
sys.stdout.flush()
```

The flicker stops after replacing the 'cls' call with VT100 escape sequences. 

![Alt Text](/images/vt100_matrix.gif)

VT100 controls also allows us to enter color codes, which completes the rendering, because we need that green matrix effect. 

![Alt Text](/images/vt100_color_matrix.gif)

## The Curses Library

While we have just seen how to build Matrix Rain on console using standard library, we have however restricted our target consoles to VT100 consoles. 

Besides, there is no standard way to get a terminal's width and height. In the above application, I pass the width and height of the console layout as a parameter. 

This is not ideal. 

All these problems are solved by using a portable library like 'Curses'. Curses is not shipped with the standard Python distribution on Windows. 

However, there are third party Curses library that can be installed using pip. 

The overall approach does not change with Curses, except the library for rendering. 

While using Curses, I did something different - I decided to do async rendering and have veritical channels get drained asynchronously too. 

The output of the Curses implementation is on [Youtube](https://www.youtube.com/watch?v=uJwc8n0OnQE)

## Conclusion

Console programming still has applications particularly in non-graphical systems that still exist.

Matrix Rain is a fun problem to learn the techniques. It is simple enough to solve and can have satisfying results. 

See you at the theatres. 
