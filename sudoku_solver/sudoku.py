"""Solving algorithm for Sudokus via backtracking and generators"""

from collections.abc import Iterator
from time import perf_counter
from enum import Enum
from samples import sudoku_with_several_solutions as sudoku

class FindNextNumberMetod(Enum):
    LeastPossibleCandidates = 0
    NextInOrder = 1
    Random = 2

def print_sudoku(board: list[list[int]]) -> None:
    """Prints a sudoku to the console"""
    # https://en.wikipedia.org/wiki/List_of_Unicode_characters#Box_Drawing
    count_col = 0
    count_row = 0
    for row in board:
        if count_row % 3 == 0 and count_row < 8 and count_row > 0:
            print("\u2501\u2501\u2501\u2501\u2501\u2501\u254B\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u254B\u2501\u2501\u2501\u2501\u2501\u2501")
        for num in row:
            count_col += 1
            print(num if num > 0 else "*", end="")
            print(" ", end="")
            if count_col % 3 == 0 and count_col < 8:
                print("\u2503 ", end="")
        print()
        count_row += 1
        count_col = 0
    print()

def get_next_cell(board: list[list[int]]) -> None | tuple[int, int, list[int]]:
    """Gets the coordinate of an empty cell (if there is one) with the least
    number of possible candidates as well as the list of these candidates"""
    best_coord: None | tuple[int, int] = None
    best_candidates: None | list[int] = None
    for row in range(9):
        for col in range(9):
            if board[row][col] > 0:
                continue
            candidates = [num for num in range(1, 10) if is_valid(row, col, num, board)]
            if len(candidates) == 1:
                return row, col, candidates
            if best_candidates is None or len(candidates) < len(best_candidates):
                best_coord = (row, col)
                best_candidates = candidates
    if best_coord is None:
        return None
    row, col = best_coord
    return row, col, best_candidates


# used in tutorial on youtube
def get_next_cell_old(board: list[list[int]]) -> None | tuple[int, int, list[int]]:
    """Gets the coordinate of any empty cell (if there is one) and
    its list of candidates. This approach is much less efficient:
    The "hard_sudoku" sample takes around 2 seconds to solve with "get_next_cell",
    but around 17 seconds with "get_next_cell_old" here.
    """
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                #print(f'getting candidates for {row}/{col}')
                candidates = [
                    num for num in range(1, 10) if is_valid(row, col, num, board)
                ]
                return row, col, candidates
    return None

def is_valid(row: int, col: int, num: int, board: list[list[int]]) -> bool:
    """Checks if a potential number is valid at a given position in the board"""
    #print(f'checking {num}')
    if num in board[row]:
        #print(f'{num} in {board[row]} is not valid')
        #print_sudoku(board)
        #input("Press Enter to continue...")
        return False
    if num in [board[i][col] for i in range(0, 9)]:
        return False
    row_start = 3 * (row // 3)
    col_start = 3 * (col // 3)
    return num not in [
        board[row_start + i][col_start + j] for i in range(0, 3) for j in range(0, 3)
    ]

def get_empty_board() -> list[list[int]]:
    #return [
    #    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #    [0, 0, 0, 0, 0, 0, 0, 0, 0],
#]
    return [[0 for _ in range(9)] for _ in range(9)]

def get_solutions(board: list[list[int]], method: FindNextNumberMetod = FindNextNumberMetod.LeastPossibleCandidates) -> Iterator[list[list[int]]]:
    """Generator recursively yielding completions of a Sudoku board"""
    cell: None | tuple[int, int, list[int]]
    match method:
        case FindNextNumberMetod.LeastPossibleCandidates:
            cell = get_next_cell(board)  # or: get_next_cell_old(board)
        case FindNextNumberMetod.NextInOrder:
            cell = get_next_cell_old(board)  # or: get_next_cell_old(board)
        case FindNextNumberMetod.Random:
            #cell = get_next_cell(board)  # or: get_next_cell_old(board)
            #tbd
            pass
        case _:
            cell = get_next_cell(board)

    #print(cell)

    if cell is None:
        yield board
        return
    row, col, candidates = cell
    for num in candidates:
        board[row][col] = num
        yield from get_solutions(board)
        board[row][col] = 0

def main() -> None:
    """Prints the solutions to a sample sudoku"""

    my_board = sudoku
    my_board = get_empty_board()

    print("\nSudoku:\n")
    print_sudoku(my_board)

    single_solution = get_solutions(my_board, FindNextNumberMetod.LeastPossibleCandidates)
    print_sudoku(next(single_solution))
    single_solution.close()

    return

    print("Solutions:\n")

    number_solutions = 0
    solutions = get_solutions(my_board)

    start_time = perf_counter()

    for solution in solutions:
        number_solutions += 1
        print_sudoku(solution)

    end_time = perf_counter()

    message = f"Found {number_solutions} solution"
    if number_solutions > 1:
        message += "s"
    print(message)

    rounded_time = format(end_time - start_time, ".3f")
    print(f"Ellapsed time: {rounded_time}")

    #single_solution = get_solutions(sudoku)
    #print_sudoku(next(single_solution))
    #single_solution.close()


if __name__ == "__main__":
    main()