from SudokuPuzzle import SudokuPuzzle, parsePuzzle
from SudokuSolver import SolvePuzzle


if __name__ == '__main__':
    puzz = parsePuzzle("sudokus/s15a.txt")
    print("Starting Puzzle:")
    puzz.printPuzzle()
    solvedPuzz = SolvePuzzle(puzz)
    if solvedPuzz is None or not solvedPuzz.isSolved():
        print("This puzzle is unsolvable")
    else:
        print("Solved Puzzle:")
        solvedPuzz.printPuzzle()
