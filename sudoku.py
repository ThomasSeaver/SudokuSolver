def printPuzzle(sudokuAr):
    for x in range(9):
        print("-------------------")
        line = ""
        for y in range(9):
            line += "|" + sudokuAr[x*9 + y]
        line += "|"
        print(line)
    print("-------------------")

def convertString(sudokuString):
    sudokuAr = []
    for x in sudokuString:
        sudokuAr.append(x)
    return sudokuAr

def checkSquare(index, sudokuAr):
    possibles = ["1","2","3","4","5","6","7","8","9"]
    for x in range(9 * int(index / 9), 9 + 9 * int(index / 9)):
        if sudokuAr[x] in possibles:
            possibles.remove(sudokuAr[x])


    for x in range(0, 9):
        if sudokuAr[index % 9 + 9 * x] in possibles:
            possibles.remove(sudokuAr[index % 9 + 9 * x])

    boxRow = int((int(index / 9)) / 3)
    boxCol = int((index % 9) / 3)

    boxCenter = (1 + 3 * boxRow) * 9 + (1 + 3 * boxCol)

    for x in range(-1, 1):
        for y in range(-1, 1):
            if sudokuAr[(boxCenter + y) + 9 * x] in possibles:
                possibles.remove(sudokuAr[(boxCenter + y) + 9 * x])

    return possibles

def main():
    print("Type out or copy a string representing a sudoku puzzle, where squares are in order by column left to right, starting with top row and going down. 'M' represents an empty space.")
    enteredString = input("leave blank or type something wrong and we'll just use the one already typed in as a var")
    sudokuString = ""
    if len(enteredString) == 81:
        sudokuString = enteredString
    else:
        sudokuString = "M7M3M5MM9MMMMMM1M8MMMM9MMMMM3M4MMMMMM98MM2MM77M4MMM9MMMMMMMMMM5MMM68MM436MMMMMMMM"
    sudokuAr = convertString(sudokuString)
    printPuzzle(sudokuAr)
    unsolved = True
    encounteredM = True
    index = 0
    while unsolved:
        if (index > 80):
            if not encounteredM:
                unsolved = False
            encounteredM = False
            index = 0
        if (sudokuAr[index] == 'M'):
            encounteredM = True
            resultList = checkSquare(index, sudokuAr)
            if (len(resultList) == 1):
                sudokuAr[index] = resultList[0]
        index += 1

    printPuzzle(sudokuAr)

if __name__ == "__main__":
    main()