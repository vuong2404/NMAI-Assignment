import random
import time

class NQueens:
    def __init__(self, n):
        self.n = n # the size of the board
        self.board = [] # the current state of the board
        self.conflicts = {} # the number of conflicts for each queen
        self.total_conflicts = 0 # the total number of conflicts in the board
        self.max_steps = 1000 # the maximum number of steps to try before giving up

    def initialize(self):
        # randomly place one queen in each column
        self.board = list(range(self.n)) # create a list of numbers from 0 to n-1
        random.shuffle(self.board) # shuffle the list to get a random permutation
        # calculate the initial conflicts for each queen
        self.conflicts = {i: self.calculate_conflicts(i) for i in range(self.n)}
        # calculate the initial total conflicts
        self.total_conflicts = sum(self.conflicts.values()) // 2

    def calculate_conflicts(self, i, new_row=None):
        # calculate the number of conflicts for the queen at column i
        # conflicts occur when two queens are in the same row, diagonal, or anti-diagonal
        row = new_row if new_row is not None else self.board[i]
        rows = set() # a set of rows that have queens
        diags = set() # a set of diagonals that have queens
        anti_diags = set() # a set of anti-diagonals that have queens
        for j in range(self.n):
            if j == i: continue # skip the same column
            rows.add(self.board[j]) # add the row of the queen at column j to the set
            diags.add(self.board[j] - j) # add the diagonal of the queen at column j to the set
            anti_diags.add(self.board[j] + j) # add the anti-diagonal of the queen at column j to the set
        conflicts = 0
        if row in rows: conflicts += 1 # same row
        if row - i in diags: conflicts += 1 # same diagonal
        if row + i in anti_diags: conflicts += 1 # same anti-diagonal
        return conflicts

    def update_conflicts(self, i, new_row):
        # update the conflicts for the queen at column i and its neighbors after moving to a new row
        old_row = self.board[i]
        self.board[i] = new_row
        self.total_conflicts = 0 # reset the total conflicts
        for j in range(self.n):
            self.conflicts[j] = self.calculate_conflicts(j) # recalculate the conflicts for each queen
            self.total_conflicts += self.conflicts[j] # update the total conflicts
        self.total_conflicts //= 2

    def solve(self):
        # try to find a solution using hill climbing algorithm
        start_time = time.time()
        for step in range(self.max_steps):
            print(f"Step {step}, total conflicts: {self.total_conflicts}")
            if self.total_conflicts == 0: # found a solution
                end_time = time.time()
                print(f"Solution found in {end_time - start_time} seconds")
                return True
            # find the most conflicted queen
            max_conflicts = max(self.conflicts.values())
            candidates = [i for i in range(self.n) if self.conflicts[i] == max_conflicts]
            i = random.choice(candidates)
            # find the best row to move the queen to
            min_conflicts = self.n
            best_rows = []
            for row in range(self.n):
                if row == self.board[i]: continue # skip the current row
                conflicts = self.calculate_conflicts(i, row)
                if conflicts < min_conflicts:
                    min_conflicts = conflicts
                    best_rows = [row]
                elif conflicts == min_conflicts:
                    best_rows.append(row)
            new_row = random.choice(best_rows)
            # move the queen to the new row and update the conflicts
            self.update_conflicts(i, new_row)
        end_time = time.time()
        print(f"Time execution: {end_time - start_time} seconds")
        return False

    def print_board(self):
        # print the board as a matrix of dots and Qs
        for row in range(self.n):
            line = ""
            for col in range(self.n):
                if self.board[col] == row:
                    line += "Q "
                else:
                    line += ". "
            print(line)

# test the program with n = 10
nq = NQueens(20)
nq.initialize()
nq.solve()
nq.print_board() # uncomment this line to print the board (not recommended for large n)