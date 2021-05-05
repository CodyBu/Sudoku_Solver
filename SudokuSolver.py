from copy import deepcopy
import math

def SolvePuzzle(puzzle):
    """
    :param puzzle: SudokuPuzzle
    :return: Solved SudokuPuzzle
    """
    solved = deepcopy(puzzle)
    data = propagate(solved)
    availability = data[0]
    solved = data[1]
    if not solved.isSolved():
        solved = search(solved, availability, getNextVar(solved, availability))
    return solved

def getConstraints(puzzle, r, c):
    """Finds the values which are constraining variable (r, c)
    :param puzzle: SudokuPuzzle being used
    :param r: Row number of variable
    :param c: Column number of variable
    :return: Set of values constraining variable (r, c)
    """
    #sub-sections of puzzle treated as smaller 3x3 matrix
    sections = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
    values = set()

    #find values in row
    for i in range(9):
        if puzzle.getValue(r, i) != 0:
            values.add(puzzle.getValue(r, i))

    #find values in column
    for i in range(9):
        if puzzle.getValue(i, c) != 0:
            values.add(puzzle.getValue(i, c))

    #find section row and column
    sr = 2
    sc = 2
    if r < 3:
        sr = 0
    elif r < 6:
        sr = 1
    if c < 3:
        sc = 0
    elif c < 6:
        sc = 1
    for n in sections[sr]:
        for m in sections[sc]:
            if puzzle.getValue(n, m) != 0:
                values.add(puzzle.getValue(n, m))
    return values

def getNeighbors(puzzle, r, c):
    """Finds the variables which are constrained by variable (r, c)
        :param puzzle: SudokuPuzzle being used
        :param r: Row number of variable
        :param c: Column number of variable
        :return: Set of variables which variable (r, c) is constraining
        """
    # sub-sections of puzzle treated as smaller 3x3 matrix
    sections = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
    values = set()

    # find values in row
    for i in range(9):
        if puzzle.getValue(r, i) == 0:
            values.add((r, i))

    # find values in column
    for i in range(9):
        if puzzle.getValue(i, c) == 0:
            values.add((i, c))

    # find section row and column
    sr = 2
    sc = 2
    if r < 3:
        sr = 0
    elif r < 6:
        sr = 1
    if c < 3:
        sc = 0
    elif c < 6:
        sc = 1
    for n in sections[sr]:
        for m in sections[sc]:
            if puzzle.getValue(n, m) == 0:
                values.add((n, m))
    return values

def getNextVar(puzzle, availability):
    """Gets the best variable to search based on inputs
    :param puzzle: SudokuPuzzle being searched
    :param availability: Availability set of the puzzle
    :return: Tuple containing row and column number of variable chosen
    """
    mostConstrained = set()
    mostConstraining = None
    min = math.inf

    #fills mostConstrained with most constrained variables
    for var in availability:
        if len(availability[var]) <= min:
            if len(availability[var]) == min:
                mostConstrained.add(var)
            else:
                mostConstrained = set()
                mostConstrained.add(var)
                min = len(availability[var])

    #breaks any tie using most constraining variable
    if len(mostConstrained) > 1:
        mostConstraining = set()
        max = -math.inf
        for var in mostConstrained:
            length = len(getNeighbors(puzzle, var[0], var[1]))
            if length >= max:
                if length == max:
                    mostConstraining.add(var)
                else:
                    mostConstraining = set()
                    mostConstraining.add(var)
                    max = length
    if mostConstraining == None:
        return mostConstrained.pop()
    else:
        return mostConstraining.pop()

def propagate(puzzle):
    """Generates availability sets and propagates changes
    :param puzzle: SudokuPuzzle being used
    :return: Availability set and puzzle if no sets are emptied and no illegal configurations are generated,
     None otherwise
    """
    domain = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    availability = {}
    changed = True
    while changed:
        changed = False
        availability = {}
        for n in range(9):
            for m in range(9):
                if puzzle.getValue(n, m) == 0:
                    availability.update({(n, m): domain-getConstraints(puzzle, n, m)})
                    if len(availability[(n, m)]) == 0:
                        return None
        for key in availability:
            if len(availability[key]) == 1:
                changed = True
                puzzle.setValue(key[0], key[1], availability[key].pop())
        if not puzzle.isLegal():
            return None
    return availability, puzzle

def search(puzzle, avail, start):
    """Chooses a value and searches for a solution
    :param puzzle: SudokuPuzzle being searched
    :param avail: Availability set of puzzle
    :param start: Variable being searched
    :return: Solved puzzle configuration if one exists, None if not
    """
    for value in avail[start]:
        puzzleCopy = deepcopy(puzzle)
        puzzleCopy.setValue(start[0], start[1], value)
        propData = propagate(puzzleCopy)
        if propData is not None:
            if propData[1].isComplete():
                return propData[1]
            else:
                result = search(propData[1], propData[0], getNextVar(propData[1], propData[0]))
                if result is not None:
                    return result
