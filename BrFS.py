from queue import Queue
from NQueens import NQueens
class NQueenBFS (NQueens):
    @NQueens.timing_decorator
    def solve(self):
        if self.size < 3:
            return []
        queue = Queue()
        solutions = []
        queue.put([])

        while not queue.empty():
            solution = queue.get()

            if not self.is_valid_constraint(solution):
                continue
            row = len(solution)
            if row == self.size:
                solutions.append(solution)
            else:
                for col in range(self.size):
                    new_solution = solution.copy()
                    new_solution.append(col)
                    queue.put(new_solution)
        
        return solutions
    


