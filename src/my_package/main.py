#FIXME fix this import
import numpy

EMPTY_CELL = '0'
HUMAN_PIECE = 'X'
COMP_PIECE = 'O'

#FIXME test variables in place of those passed from command line
n = 6
h = 0

def start_board(n):
    #initializes empty board of NxN size
    board = numpy.full((n, n), EMPTY_CELL)
    return board

def drop_piece(board, col, h):
    #places piece at last empty row after validating
    if is_valid_move(board, col):
        row = find_empty_bottom_row(board, col)
        
        if h == 0:
            board[row][col] = HUMAN_PIECE
            h += 1
            
        elif h == 1:
            board[row][col] = COMP_PIECE
            h -= 1
    
    return h

def is_valid_move(board, col):
    #checks that a column is not already full
    return board[n-1][col] == EMPTY_CELL

def find_empty_bottom_row(board, col):
    #finds the stopping place for a dropped piece
    for row in range(n-1, -1, -1):
        if board[row][col] == EMPTY_CELL:
            return row

board = start_board(n)
print(board)

#FIXME test variables in place of those passed from command line
m = 4

game_over = False

while not game_over:
    if h == 0:
        col = int(input("Player Turn. Choose Column."))
        h = drop_piece(board, col, h)
        print(board)
    if h == 1:
        print('Computer Turn.')
        #FIXME integrate with ai player here
    
