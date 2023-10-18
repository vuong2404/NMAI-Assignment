from BrFS import NQueenBFS


if __name__ == '__main__':
    print('NQueens Problem')
    size = int(input('Enter the size of board: '))

    nqueenbfs = NQueenBFS(size)
    bfs_solutions = nqueenbfs.solve()


    
