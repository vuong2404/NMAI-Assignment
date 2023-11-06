from BrFS import NQueenBFS

if __name__ == '__main__':
    print('NQueens Problem')
    size = int(input('Enter the size of board: '))

    nqueenbfs = NQueenBFS(size)
    bfs_solutions = nqueenbfs.solve()
    if size <= 8:
        for i,solution in enumerate(bfs_solutions):
            print("Solution",  i + 1)
            nqueenbfs.printBoard(nqueenbfs.make_board(solution))
            print("**********************")
    
    print("Found total", len(bfs_solutions), "solutions")

    
