import math
import time
import matplotlib.pyplot as plt

def evaluate(board):
    # Evaluate the board for the "O" player
    score_o = evaluate_player(board, "O")

    # Evaluate the board for the "X" player
    score_x = evaluate_player(board, "X")

    return score_o - score_x

def evaluate_player(board, player):
    score = 0

    for i in range(3):
        row_count = sum(1 for j in range(3) if board[i][j] == player)
        col_count = sum(1 for j in range(3) if board[j][i] == player)
        score += evaluate_line(row_count)
        score += evaluate_line(col_count)

    diag1_count = sum(1 for i in range(3) if board[i][i] == player)
    diag2_count = sum(1 for i in range(3) if board[i][2 - i] == player)
    score += evaluate_line(diag1_count)
    score += evaluate_line(diag2_count)

    return score

def evaluate_line(count):
    if count == 3:
        return 100  #Best Case, Three in a row, +100
    elif count == 2:
        return 10   #Two in a row, decent, +10
    elif count == 1:
        return 1    # One in a row, ok +1
    else:
        return 0


def is_winner(board, player):
    for i in range(3):
        if all(board[i][j] == player for j in range(3)):
            return True
        if all(board[j][i] == player for j in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

def is_full(board):
    return all(cell is not None for row in board for cell in row)

def get_empty_cells(board):
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] is None]

def minimax(board, depth, maximizing_player, alpha, beta):
    if is_winner(board, "X"):
        return -1
    elif is_winner(board, "O"):
        return 1
    elif is_full(board):
        return 0

    if maximizing_player:
        max_eval = -math.inf
        for i, j in get_empty_cells(board):
            board[i][j] = "O"
            eval = minimax(board, depth + 1, False, alpha, beta)
            board[i][j] = None
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  
        return max_eval
    else:
        min_eval = math.inf
        for i, j in get_empty_cells(board):
            board[i][j] = "X"
            eval = minimax(board, depth + 1, True, alpha, beta)
            board[i][j] = None
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break  
        return min_eval

def find_best_move(board):
    best_val = -math.inf
    best_move = None
    for i, j in get_empty_cells(board):
        board[i][j] = "O"
        move_val = minimax(board, 0, False, -math.inf, math.inf)
        board[i][j] = None
        if move_val > best_val:
            best_move = (i, j)
            best_val = move_val
    return best_move

def print_board(board):
    for row in board:
        print(" ".join([cell if cell is not None else "_" for cell in row]))

def evaluate_algorithm_performance(num_iterations):
    minimax_times = []
    best_move_times = []

    for _ in range(num_iterations):
        board = [[None, None, None], [None, None, None], [None, None, None]]

        start_time = time.time()
        minimax(board, 0, True, -math.inf, math.inf)
        minimax_times.append(time.time() - start_time)

        # Measure time for find_best_move
        start_time = time.time()
        find_best_move(board)
        best_move_times.append(time.time() - start_time)

    return minimax_times, best_move_times

def plot_results(minimax_times, best_move_times):
    plt.figure(figsize=(10, 6))

    # Plotting execution times
    plt.plot(range(1, len(minimax_times) + 1), minimax_times, label='Minimax', marker='o')
    plt.plot(range(1, len(best_move_times) + 1), best_move_times, label='Best Move', marker='o')

    plt.title('Performance Comparison')
    plt.xlabel('Iteration')
    plt.ylabel('Execution Time (seconds)')
    plt.legend()
    plt.show()

def main():
    num_iterations = 100

    minimax_times, best_move_times = evaluate_algorithm_performance(num_iterations)
    plot_results(minimax_times, best_move_times)
    board = [[None, None, None], [None, None, None], [None, None, None]]

    while not is_full(board) and not is_winner(board, "X") and not is_winner(board, "O"):
        print_board(board)
        player_move = tuple(map(int, input("Enter your move (row and column): ").split()))
        if board[player_move[0]][player_move[1]] is not None:
            print("Cell already taken. Try again.")
            continue
        board[player_move[0]][player_move[1]] = "X"

        if is_winner(board, "X"):
            print_board(board)
            print("You win!")
            break

        if is_full(board):
            print_board(board)
            print("It's a draw!")
            break

        print("Computer's turn:")
        computer_move = find_best_move(board)
        print(f"Computer plays at {computer_move}")
        board[computer_move[0]][computer_move[1]] = "O"

        if is_winner(board, "O"):
            print_board(board)
            print("Computer wins!")
            break

if __name__ == "__main__":
    main()
