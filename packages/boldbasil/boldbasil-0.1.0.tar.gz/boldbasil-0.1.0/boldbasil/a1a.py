def a1a():
    # N-Queens Problem
    def is_safe(board, row, col):
        for i in range(col):
            if board[row][i] == 'Q':
                return False
        for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
            if board[i][j] == 'Q':
                return False
        for i, j in zip(range(row, len(board), 1), range(col, -1, -1)):
            if board[i][j] == 'Q':
                return False
        return True

    def solve_n_queen(N):
        board = [['.'] * N for _ in range(N)]

        def solve_util(col):
            if col >= N:
                return True
            for i in range(N):
                if is_safe(board, i, col):
                    board[i][col] = 'Q'
                    if solve_util(col + 1):
                        return True
                    board[i][col] = '.'
            return False

        if not solve_util(0):
            print("Solution doesn't exist")
            return False

        print("\nN-Queen Solution:")
        for i in range(N):
            for j in range(N):
                print(board[i][j], end=' ')
            print()

    # Take input and solve N-Queens
    N = int(input('Enter N for N-Queens Problem: '))
    solve_n_queen(N)

    # Salary Prediction using Linear Regression
    import numpy as np
    import matplotlib.pyplot as plt
    from sklearn.linear_model import LinearRegression

    x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]).reshape(-1, 1)  # Years of experience
    y = np.array([39000, 46000, 57000, 63000, 69000, 76000, 83000, 91000, 97000, 102000])  # Salaries

    linear = LinearRegression()
    linear.fit(x, y)

    y_pred = linear.predict(x)

    plt.scatter(x, y, color='blue', label='Actual Salary')
    plt.plot(x, y_pred, color='red', label='Predicted Salary')
    plt.title('Salary vs Experience')
    plt.xlabel('Years of Experience')
    plt.ylabel('Salary')
    plt.legend()
    plt.show()


    # Run the function
    a1a()
