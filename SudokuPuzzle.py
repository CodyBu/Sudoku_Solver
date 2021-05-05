class SudokuPuzzle:

    __slots__ = ['puzzle']

    def __init__(self, puzzle):
        """Initializes a puzzle with data from 9x9 2d array parameter
        :param puzzle: 9x9 2d integer array
        """
        self.puzzle = puzzle

    def getValue(self, n, m):
        """
        :param n: Row number
        :param m: Column number
        :return: Value at position (n, m)
        """
        return self.puzzle[n][m]

    def setValue(self, n, m, new):
        """Sets value at (n, m) to new value
        :param n: Row number
        :param m: Column number
        :param new: Value being added
        :return: True if added, False if not
        """
        if new >= 0 and new < 10:
            self.puzzle[n][m] = new
            return True
        return False

    def isComplete(self):
        """ Checks if all variables have been assigned values
        :return: True if all variables are assigned, False if not
        """
        for n in range(9):
            for m in range(9):
                if self.puzzle[n][m] == 0:
                    return False
        return True

    def isLegal(self):
        """ Checks if current configuration violates any constraints
        :return: True if configuration if legal, False if not
        """
        # checks for same values in rows
        for n in range(9):
            rows = set()
            for m in range(9):
                if self.puzzle[n][m] != 0:
                    size = len(rows)
                    rows.add(self.puzzle[n][m])
                    if size == len(rows):
                        return False

        #checks for same values in columns
        for m in range(9):
            cols = set()
            for n in range(9):
                if self.puzzle[n][m] != 0:
                    size = len(cols)
                    cols.add(self.puzzle[n][m])
                    if size == len(cols):
                        return False

        #checks for same values in sections
        sections = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
        for r in sections:
            for c in sections:
                sects = set()
                for n in r:
                    for m in c:
                        if self.puzzle[n][m] != 0:
                            size = len(sects)
                            sects.add(self.puzzle[n][m])
                            if size == len(sects):
                                return False
        return True

    def isSolved(self):
        """Checks if current configuration is solved.txt
        :return: True if puzzle is solved.txt, False if not
        """
        return self.isComplete() and self.isLegal()

    def printPuzzle(self):
        """Prints the puzzle to command line
        :return: Nothing
        """
        for i in range(9):
            print(self.puzzle[0][i], end=" ")
        for n in range(1, 9):
            print()
            for m in range(9):
                print(self.puzzle[n][m], end=" ")
        print("\n")

def parsePuzzle(fileName):
    """Creates a SudokuPuzzle object from a .txt file
    :param fileName: File name
    :return: SudokuPuzzle object with data
    """
    data = []
    f = open(fileName, 'r')
    for line in f:
        splitLine = line.split(sep=" ")
        row = []
        if len(splitLine) >= 9:
            for i in range(9):
                row.append(int(splitLine[i]))
        data.append(row)
    f.close()
    return SudokuPuzzle(data)