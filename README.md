# YChip8

Being a 90's kid, I grew up with a lot of awesome consoles. With time these retro consoles were ported to the home computer. As a side project I wanted to dive into the world of emulators, i.e. creating code that pretends to be a certain hardware environment whereupon a piece of propriatary software ('rom') can run. As such, I created this Chip-8 interpreter/emulator that runs Chip-8 roms.


Features:

 * OpenGL rendering
 * Very high level of compatibility

TODO list

 * Expanding upon existant documentation
 * Better implementation of unit tests
 * Quirks mode in order to support roms that have been badly coded

Installation requirements:

 * Python 3.5 >
 * Pyglet, py, pytest, and prettytable (see requirements.txt)

Usage

 ```
 python main.py <ROM NAME>
 ```

List of included roms:

 * BLITZ
 * BOWLING
 * BRIX
 * HIDDEN
 * INVADERS
 * LUNAR
 * PONG
 * ROCKET
 * TETRIS
 * TICTAC

Keyboard

|               |               |       |
| ------------- |:-------------:| -----:|
| Q             | W             | E     |
| A             | S             | D     |
| Z             | X             | C     |
| R             | F             | V     |
| T             | G             | B     |

+ SPACEBAR

Props to Matthew Mikolay and his [guideline](http://mattmik.com/files/chip8/mastering/chip8.html).

Finally, a big thanks goes out to the moral and/or debugging support of
Vanja Popovic, Marco Westerhof, and Tiemen Glastra.
