import copy

rows = []
cols = []
boxes = []
sudokuAr = []
potentialsAr = []

def printPuzzle():
    for x in range(9):
        print("------- ------- -------")
        line = ""
        for y in range(9):
            line += "|" + str(sudokuAr[x*9+y])
            if ((y + 1) % 3 == 0):
                line += "| " 

        print(line)
        if ((x + 1) % 3 == 0):
            print("------- ------- -------")
    print()
    print()

def convertString(sudokuString):
    for x in sudokuString:
        if (x != '0'):
            sudokuAr.append(int(x))
            potentialsAr.append([int(x)])
        else:
            sudokuAr.append(0)
            potentialsAr.append([1,2,3,4,5,6,7,8,9])

def buildIndexHolders():
    for x in range(9):
        row = []
        for y in range(9):
            row.append(x * 9 + y)
        rows.append(row)

    for x in range(9):
        col = []
        for y in range(9):
            col.append(x + y * 9)
        cols.append(col)

    for x in range(9):
        box = []

        boxRow = int(x / 3)
        boxCol = int(x % 3)
        boxCenter = (1 + 3 * boxRow) * 9 + (1 + 3 * boxCol)
        
        for y in range(-1, 2):
            for z in range(-1, 2):
                box.append(boxCenter + y + z * 9)

        boxes.append(box)

def buildPotentials(index):
    rowNum = int(index / 9)
    colNum = index % 9
    boxNum = rowNum - rowNum % 3 + int(colNum / 3)

    # go across row
    for x in rows[rowNum]:
        if sudokuAr[x] in potentialsAr[index]:
            potentialsAr[index].remove(sudokuAr[x])

    # go across col
    for x in cols[colNum]:
        if sudokuAr[x] in potentialsAr[index]:
            potentialsAr[index].remove(sudokuAr[x])

    # go across box
    for x in boxes[boxNum]:
        if sudokuAr[x] in potentialsAr[index]:
            potentialsAr[index].remove(sudokuAr[x])

# check for conjugate triples
def conjTripCheck(selectAr):
    # pull every potential triple and poll for tripleness
    # ugly ugly u gly 
    for x in range(len(selectAr)):
        if len(potentialsAr[selectAr[x]]) == 2 or len(potentialsAr[selectAr[x]]) == 3:
            for y in range(x + 1, len(selectAr)):
                if len(potentialsAr[selectAr[y]]) == 2 or len(potentialsAr[selectAr[y]]) == 3:
                    for z in range(y + 1, len(selectAr)):
                        if len(potentialsAr[selectAr[z]]) == 2 or len(potentialsAr[selectAr[z]]) == 3:
                            # if we get to this point I know I have 3 cells with 2/3 length
                            # if I add every unique from the three lists to one list and it is len 3 then I should meet condition
                            # may not be perfect and could run into issues if conjugate pairs haven't been checked, but they should be 
                            conjTrip = list(dict.fromkeys(potentialsAr[selectAr[x]] + potentialsAr[selectAr[y]] + potentialsAr[selectAr[z]]))
                            if (len(conjTrip) == 3):
                                for a in range(len(selectAr)):
                                    if a != x and a != y and a != z:
                                        if (potentialsAr[selectAr[a]].count(conjTrip[0]) > 0):
                                            potentialsAr[selectAr[a]].remove(conjTrip[0])
                                        if (potentialsAr[selectAr[a]].count(conjTrip[1]) > 0):
                                            potentialsAr[selectAr[a]].remove(conjTrip[1])
                                        if (potentialsAr[selectAr[a]].count(conjTrip[2]) > 0):
                                            potentialsAr[selectAr[a]].remove(conjTrip[2])


# check for conjugate pairs
# if two squares are only num x and num y potentially, then they must be those numbers though we don't know which will be which
# therefore we can remove these as options from the other squares
def conjPairCheck(selectAr):
    # definitely should probably just use like count or something for this but it might be more efficient idk
    # just ugly this way
    # go across unit
    for x in selectAr:
        # if it has 2 elements in its potential, its got the option to be a naked pair
        if len(potentialsAr[x]) == 2:
            # check across backhalf for a naked pair match
            for y in selectAr:
                if x < y and potentialsAr[x] == potentialsAr[y]:
                    # go across the unit again and if the naked pair's elements exist in the remaining units, clear them
                    for z in selectAr:
                        if x != z and y != z:
                            if (potentialsAr[z].count(potentialsAr[x][0]) > 0):
                                potentialsAr[z].remove(potentialsAr[x][0])
                            if (potentialsAr[z].count(potentialsAr[x][1]) > 0):
                                potentialsAr[z].remove(potentialsAr[x][1])

# check for hidden singles
def hiddenSingleCheck(selectAr):
    # build potential indices list
    # essentially go across each square inside unit
    # if square has potential to be filled with number x
    # insert that indice within the xth array within this list
    potentialIndices = [[], [], [], [], [], [], [], [], [], []] 
    for y in selectAr:
        for z in potentialsAr[y]:
            potentialIndices[z].append(y)

    # if len of potential indice is 1, its the only indice that can be the xth number, and thus is the xth number
    # kill potentials as well     
    for y in range(1, 10):
        if (len(potentialIndices[y]) == 1):
            sudokuAr[potentialIndices[y][0]] = y
            potentialsAr[potentialIndices[y][0]] = [y]

def checkPuzzle():
    # go through each potentials list to clear out singles
    for x in range(81):
        if (sudokuAr[x] == 0 and len(potentialsAr[x]) == 1):
            sudokuAr[x] = potentialsAr[x][0]

    # for every row/col/box
    for x in range(9):
        hiddenSingleCheck(rows[x])
        hiddenSingleCheck(cols[x])
        hiddenSingleCheck(boxes[x])
        conjPairCheck(rows[x])
        conjPairCheck(cols[x])
        conjPairCheck(boxes[x])
        conjTripCheck(rows[x])
        conjTripCheck(cols[x])
        conjTripCheck(boxes[x])


def main():
    #print("Type out or copy a string representing a sudoku puzzle, where squares are in order by column left to right, starting with top row and going down. 'M' represents an empty space.")
    enteredString = ""#input("leave blank or type something wrong and we'll just use the one already typed in as a var")
    sudokuString = ""
    if len(enteredString) == 81:
        sudokuString = enteredString
    else:
        sudokuString = "008500000000034000700060009600980103800000002109072004900020007000340000000006400"
    convertString(sudokuString)
    printPuzzle()
    buildIndexHolders()
    solved = False
    old = []
    oldPotentials = []
    index = 0

    frames = 0
    while not solved:
        if (index > 80):
            frames += 1
            checkPuzzle()
            if old == sudokuAr and oldPotentials == potentialsAr:
                solved = True
            index = 0
            old = copy.deepcopy(sudokuAr)
            oldPotentials = copy.deepcopy(potentialsAr)
        if (sudokuAr[index] == 0):
            buildPotentials(index)
        index += 1

    print(frames)
    for i in range(9):
        print(str(potentialsAr[i*9]) + " " + str(potentialsAr[i*9+1]) + " " + str(potentialsAr[i*9+2]) + " " + str(potentialsAr[i*9+3]) + " " + str(potentialsAr[i*9+4]) + " " + str(potentialsAr[i*9+5]) + " " + str(potentialsAr[i*9+6]) + " " + str(potentialsAr[i*9+7]) + " " + str(potentialsAr[i*9+8]))
    printPuzzle()

if __name__ == "__main__":
    main()     