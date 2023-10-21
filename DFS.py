class NQueen_DFS:
    def __init__(self, N) -> None:
        self.N = N

    def is_valid(self, board, row, col):
        for i in range(row):
            if board[i] == col or \
                    abs(board[i] - col) == abs(i - row):
                return False
        return True

    def dfs(self, board, row, results):
        if row == self.N:
            results.append(board[:])
            return
        for col in range(self.N):
            if self.is_valid(board, row, col):
                board[row] = col
                self.dfs(board, row + 1, results)

    def solve_n_queens(self):
        board = [-1] * self.N
        results = []
        self.dfs(board, 0, results)

        final_results = []
        for res in results:
            final_results.append([x for x in res])
        return final_results


# khoi tao gia tri cho code tren
nqueen = NQueen_DFS(N=int(input()))
print(nqueen.solve_n_queens())
