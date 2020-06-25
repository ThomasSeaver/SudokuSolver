# SudokuSolver
Attempt at building a python script that solves an input sudoku puzzle

works pretty well, takes in input string in code or can uncomment input line but that sucks
goes across each square, finds what can fit in the square based on row/col/box
if this list of options is length 1, by necessity that is what goes in the square

secondly, check for conjugate pairs / triples within units (row/box/col)

if some square x and some square y exist where the potential fitting numbers for both are a and b,
we know square x will contain a or b and square y will contain the complement
by necessity, the rest of the squares will not have a or b, and we can remove them as potential options

for triplets, if the following squares have the following options (with or without an optional third)
x: a, b(, c)
y: a, c(, b)
z: b, c(, a)
we know that within this unit these three squares will contain some combination of a, b, and c,
thus no other squares in this unit have the option of a, b, or c, and we can strip them from their lists

to be a more complete basic solver, should handle pointing pairs / box-line reduction;
we can find that if one unit has only options for a number within another unit 
this second unit can strip the rest of its squares of the option, as to fulfill the first options 
responsibility, we can not put the option in other squares within unit 2

ex: top two squares in column have option 2, rest of column is not 2
we can strip 2 as an option from the rest of the box, as a 2 must be within this column

ex. left middle and right middle squares in box have option 3, rest of box is not 3
we can strip 3 as an option from the rest of the row, as a 3 must be within the box on this row

hard to explain, but semi-obvious in play. Harder to program as it requires comparing the units against eachother 
something my code does not really do in its current format
probably won't get around to adding it as it is not the most typical solution and my code falls apart against most non trivial puzzles

great great great resource: https://www.sudokuwiki.org
has a much better and more comprehensive solver, and good descriptions of various solving methods
no code taken, but definitely used to understand where my code ran into walls