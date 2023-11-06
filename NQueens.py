import time

class NQueens:
    def __init__(self, size):
        self.size = size

    def solve(self):
        pass

    # Utils function

    # Check position of queens is valid constraint
    # params queens: array of queens's position
    def is_valid_constraint(self, queens):
        num = len(queens)
        for i in range(num):
            for j in range(i + 1, num):
                a, b = i, queens[i]
                c, d = j, queens[j]
                if a == c or b == d or abs(a - c) == abs(b - d):
                    return False
        return True

    # Create a board with the position of queens
    def make_board(self, queens):
        board = [[0] * self.size for _ in range(self.size)]
        for i in range(len(queens)):
            board[i][queens[i]] = 1
        return board

    # Print the board
    def printBoard(self, board):
        for i in range(self.size):
            for j in range(self.size):
                print(" Q " if board[i][j] == 1 else " - ", end="")
            print()
    
    # Decorator to calculate execution time
    def timing_decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()

            execution_time = end_time - start_time
            print(f"Execution time: {execution_time} seconds")
            return result

        return wrapper