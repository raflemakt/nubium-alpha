# NUBIUM-ALPHA
Nubium ALPHA is a simple python/ncurses application which aims to be an inspiration to number theory enthusiasts.

It focuses on the *Divisor Plot*, a visualization of the integers with very simple rules but with exceedingly complex emergent patterns and interesting implications.

## Background
I discovered the divisor plot sometime around 2012 when writing integer sequences by hand. It has led to many profound moments as I've understood more and more of its implications:
* The entries in the n'th column is the numbers which *n* is dividable by.
* The columns with only two entries are *prime numbers*.
* The columns with an odd number of entries are *square numbers*.
* The amount of entries in a column represents the divisor function *tau(n)*.
* Columns with an abundance of entries are *highly composite*, and around them a *prime pair* can often be found.
  * Columns with an unbroken line of entries make a symmetry with the number 0 around its mid-point n/2.
    * The first column with a record unbroken line of entries is a number in the *Higly Composite Numbers* sequence (OEIS A002182) and they suggest some fractal structure of the prime numbers:
	-- the numbers between 60 and 120 that are primes must be primes between 0 and 60 (subtracting 60)

After drawing divisor plots by hand for many years I decided to program this utility to draw them for me, and it certainly is faster. As I'm neither a programmer or a mathematician (I'm a pianist) you should be sceptical about anything stated by me or in the program as it really is developed for my own amusement only.

If you find Nubium ALPHA interesting, or if you have feedback/suggestions, please let me know at raflemakt@hotmail.com

# TODO: plans for NUBIUM-ALPHA

## Planned Features
* Implement a way to access the OEIS database. Either let the user choose to download or add important sequences.
  * Make a way to project sequences over the  *DIVISOR GRAPH*
  * Make a way to search for sequences

* Improve the  *DIVISOR GRAPH MENU*
  * Make more hotkeys and show them by pressing ? or F1
    * Mode for  *MARKING OEIS SEQUENCE WITH VERTICAL BARS*, maybe with the primes as default
    * Mode for selecting a part of the graph, between two numbers, ..forgot idea
    * Access a pop-up window to type in number
    *  *SEEK POSITION IN GRAPH* in different increments, like a OEIS sequence
	-- useful to see "animations" in interesting sequences
  * When seeking to a new number which takes a certain amount of time or more, show a  *LOADING BAR* and the opportunity to cancel the operation.

* Idea for menu entry: Some kind of knowledge database
  * Cons: interfering with the learning process

* Translate NUBIUM-ALPHA into a less esoteric language
* Help/About/Options  -- menu. 

* README.md: add images

## Known Issues:
* Nubium ALPHA is currently written in native python, the reason for this is I wanted to learn the basics and to experience finding better algorithms myself. In time I will move on to using a library like  *numpy* for faster calculations.
  * A consequence of this is that the program currently freezes when trying to calculate too high numbers. I'm planning to add a loading bar to prevent crashes due to this. For the time being, expect freezes when going over 200 million.
* If the window is shrunk too small the program will crash
* Nubium ALPHA is developed on Linux, so I'm not certain everything is working on other operating systems. In theory it should, but *curses* may need to be installed manually.
