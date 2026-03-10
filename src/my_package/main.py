import argparse

EMPTY_CELL = '0'
HUMAN_PIECE = 'X'
COMP_PIECE = 'O'


def start_board(n):
    # creates initial empty board state of size n x n
    return [[EMPTY_CELL for _ in range(n)] for _ in range(n)]

def draw_board(board):
    # shows current board state in terminal with ASCII art
    n = len(board[0])
    cell_width = 3

    sep = "+" + "+".join(["-" * cell_width] * n) + "+"

    print(sep)
    for r in range(len(board)):
        row_cells = []
        for c in range(n):
            cell = board[r][c]
            display = " " if cell == EMPTY_CELL else cell
            row_cells.append(f"{display:^{cell_width}}")
        print("|" + "|".join(row_cells) + "|")
        print(sep)


def win_check(board, row, col, m):
    previous_move = board[row][col]
    rows = len(board)
    cols = len(board[0])
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal (down-right)
        (1, -1),  # diagonal (down-left)
    ]
    
    def count_in_direction(row_change, col_change):
        count = 0
        r, c = row + row_change, col + col_change
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == previous_move:
            count += 1
            r += row_change
            c += col_change
        return count
    
    for row_change, col_change in directions:
        # counts consecutive pieces in both directions, returns a win if m is met
        total = 1 + count_in_direction(row_change, col_change) + count_in_direction(-row_change, -col_change)
        if total >= m:
            return True
    
    # returns no win if not enough consecutive pieces
    return False
 
def drop_piece(board, col, player):
    # places piece at last empty row after validating
    n = len(board[0])
    if not (0 <= col < n):
        print(f"Invalid column {col}. Choose between 0 and {n-1}.")
        return None, None

    if not is_valid_move(board, col):
        print(f"Column {col} is full. Choose another column.")
        return None, None

    row = find_empty_bottom_row(board, col)
    board[row][col] = HUMAN_PIECE if player == 0 else COMP_PIECE
    return row, col


def is_valid_move(board, col):
    # checks that a column is not already full
    return board[0][col] == EMPTY_CELL


def find_empty_bottom_row(board, col):
    # finds the stopping place for a dropped piece
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == EMPTY_CELL:
            return row


def is_board_full(board):
    return all(cell != EMPTY_CELL for cell in board[0])


def main():
    parser = argparse.ArgumentParser(
        prog="connectM",
        usage="connectM N M H",
    )

    parser.add_argument("N", type=int)
    parser.add_argument(
        "M",
        type=int,
        )
    parser.add_argument(
        "H",
        type=int,
        choices=[0, 1],
    )

    args = parser.parse_args()

    # assigns values from command line
    n = args.N
    m = args.M
    h = args.H

    # starts game
    board = start_board(n)
    draw_board(board)

    # handles turns as long as the game isn't over
    game_over = False
    while not game_over:
        current_player = "Player" if h == 0 else "Computer"
        try:
            # gets input from player
            col = int(input(f"{current_player} Turn. Choose Column: "))
        except ValueError:
            print("Please enter a column in range.")
            continue

        # places piece
        row, col = drop_piece(board, col, h)
        if row is None:
            continue

        draw_board(board)

        # checks for m in a row and ends the game if won
        if win_check(board, row, col, m):
            print(f"{current_player} wins!")
            game_over = True
            continue

        # checks for a tied game and ends if board is full
        if is_board_full(board):
            print("Tie game!")
            game_over = True
            continue

        # change turns
        h = 1 - h


if __name__ == "__main__":
    main()
