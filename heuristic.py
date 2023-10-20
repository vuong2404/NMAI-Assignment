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
        self.board = [random.randint(0, self.n - 1) for _ in range(self.n)]
        self.conflicts = {i: self.calculate_conflicts(i) for i in range(self.n)}
        self.total_conflicts = sum(self.conflicts.values()) // 2

    def calculate_conflicts(self, i, new_row=None):
        row = self.board[i]
        conflicts = 0
        for j in range(self.n):
            if j == i: continue 
            if self.board[j] == row: conflicts += 1
            if abs(self.board[j] - row) == abs(j - i): conflicts += 1 
        return conflicts

    def update_conflicts(self, i, new_row):
        old_row = self.board[i]
        self.board[i] = new_row
        for j in range(self.n):
            if j == i: continue 
            old_conflicts = self.conflicts[j]
            new_conflicts = self.calculate_conflicts(j)
            self.conflicts[j] = new_conflicts
            self.total_conflicts += (new_conflicts - old_conflicts)
        self.conflicts[i] = 0

    def solve(self):
        start_time = time.time()
        for step in range(self.max_steps):
            print(f"Step {step}, total conflicts: {self.total_conflicts}")
            if self.total_conflicts == 0: # found a solution
                end_time = time.time()
                print(f"Solution found in {end_time - start_time} seconds")
                return True
            max_conflicts = max(self.conflicts.values())
            candidates = [i for i in range(self.n) if self.conflicts[i] == max_conflicts]
            i = random.choice(candidates)
            min_conflicts = self.n
            best_rows = []
            for row in range(self.n):
                if row == self.board[i]: continue 
                conflicts = self.calculate_conflicts(i, row)
                if conflicts < min_conflicts:
                    min_conflicts = conflicts
                    best_rows = [row]
                elif conflicts == min_conflicts:
                    best_rows.append(row)
            new_row = random.choice(best_rows)
            self.update_conflicts(i, new_row)
        end_time = time.time()
        print(f"Time execution: {end_time - start_time} seconds")
        return False

    def print_board(self):
        for row in range(self.n):
            line = ""
            for col in range(self.n):
                if self.board[col] == row:
                    line += "Q "
                else:
                    line += ". "
            print(line)

# test the program with n = 100000
nq = NQueens(100)   # can replace N to test
nq.initialize()
nq.solve()
# nq.print_board() # uncomment this line to print the board (not recommended for large n)