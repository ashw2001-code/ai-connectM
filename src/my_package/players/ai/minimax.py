"""
Minimax algorithm implementation for Connect M game.
"""


from my_package.main import EMPTY_CELL
from my_package.main import HUMAN_PIECE
from my_package.main import COMP_PIECE
from my_package.main import m



def minimax(board, depth, is_maximizing, alpha=float('-inf'), beta=float('inf')):
    """
    Minimax algorithm with alpha-beta pruning for Connect M game.
    
    Args:
        board: The current game board state
        depth: The current depth in the game tree
        is_maximizing: Boolean indicating if this is a maximizing or minimizing node
        alpha: Alpha value for pruning
        beta: Beta value for pruning
    
    Returns:
        The best score for the current position
    """
    # Check terminal states
    terminal_score = _evaluate_terminal_state(board)
    if terminal_score is not None:
        return terminal_score + (depth * 0.01)  # Prefer faster wins
    
    if depth == 0:
        return _evaluate_board(board)
    
    if is_maximizing:
        max_eval = float('-inf')
        for col in _get_valid_moves(board):
            _make_move(board, col, 1)  # AI player
            eval_score = minimax(board, depth - 1, False, alpha, beta)
            _undo_move(board, col)
            max_eval = max(max_eval, eval_score)
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break  # Beta cutoff
        return max_eval
    else:
        min_eval = float('inf')
        for col in _get_valid_moves(board):
            _make_move(board, col, 2)  # Opponent player
            eval_score = minimax(board, depth - 1, True, alpha, beta)
            _undo_move(board, col)
            min_eval = min(min_eval, eval_score)
            beta = min(beta, eval_score)
            if beta <= alpha:
                break  # Alpha cutoff
        return min_eval


def get_best_move(board, depth):
    """
    Finds the best move for the AI using minimax algorithm.
    
    Args:
        board: The current game board state
        depth: The maximum depth to search in the game tree
    
    Returns:
        The column index of the best move
    """
    best_move = None
    best_score = float('-inf')
    
    for col in _get_valid_moves(board):
        _make_move(board, col, 1)  #AI player
        score = minimax(board, depth - 1, False)
        _undo_move(board, col)
        
        if score > best_score:
            best_score = score
            best_move = col
    
    return best_move


def _evaluate_terminal_state(board):
    """
    Evaluates if the game has reached a terminal state (win/loss/draw).
    
    Returns:
        Score if terminal, None otherwise
    """
    # Implement based on your board state checking logic
    # Return high score for AI win, low score for opponent win, 0 for draw
    if _get_valid_moves(board) == []:
        return 0  # Draw
        # Check for win conditions for both players
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == COMP_PIECE and _check_win(board, row, col, 1):
                return 100  # AI win
            elif board[row][col] == HUMAN_PIECE and _check_win(board, row, col, 0):
                return -100  # Opponent win
    if _get_valid_moves(board) != []:
        return None  # Game is not over

    
    pass


def _evaluate_board(board):
    """
    Evaluates the current board position heuristically.
    
    Returns:
        An evaluation score
    """
    # Implement heuristic evaluation based on:
    # - Piece count advantage
    # - Threat detection
    # - Control of center positions
    score = 0
    highest_score = float('-inf')
    lowest_score = float('inf')
    
    
    if board is None:
        return 0
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == COMP_PIECE:
                score = 1 + _adjacent_count(board, row, col, 1)
                if board[row - 1][col] == EMPTY_CELL and row - 1 >= 0:
                    _make_move(board, col, 0)  # Simulate opponent move to check for threats
                    opponent_score = -1 + _adjacent_count(board, row, col, 0)
                    _undo_move(board, col)
                    if opponent_score > 0:
                        score -= opponent_score  # Penalize if opponent has a strong threat
                if score > highest_score:
                    highest_score = score
                
            elif board[row][col] == HUMAN_PIECE:
                score = -1 + _adjacent_count(board, row, col, 0)
                if board[row - 1][col] == EMPTY_CELL and row - 1 >= 0:
                    _make_move(board, col, 1)  # Simulate AI move to check for threats
                    opponent_score = 1 + _adjacent_count(board, row, col, 1)
                    _undo_move(board, col) 
                    if opponent_score > 0:
                        score += opponent_score  # Reward if AI has a strong threat
                if score < lowest_score:
                    lowest_score = score

    

    return score
pass


def _get_valid_moves(board):
    """
    Gets all valid column moves for the current board state.
    
    Returns:
        List of valid column indices
    """
    # Return columns that are not full
    open_cols = []

    for col in range(len(board[0])):
        if board[0][col] == EMPTY_CELL:  # Assuming top row is index 0
            open_cols.append(col)
    return open_cols
        
pass


def _make_move(board, col, h):
    """
    Makes a move on the board for the given player.
    
    Args:
        board: The game board
        col: Column to place piece
        player: Player ID (1 for AI, 0 for player)
    """
    # Place piece in lowest available row of column
    for row in range(len(board)-1, -1, -1):
        if board[row][col] == EMPTY_CELL and board[row + 1][col] != EMPTY_CELL:
            board[row][col] = COMP_PIECE if h == 1 else HUMAN_PIECE
            break
pass


def _undo_move(board, col):
    """
    Undoes the last move in the given column.
    
    Args:
        board: The game board
        col: Column to remove piece from
    """
    # Remove the top piece from the column
    for row in range(len(board)):
        if board[row][col] != EMPTY_CELL:
            board[row][col] = EMPTY_CELL
            break
pass

def _check_win(board, row, col, player):
    """
    Checks if the given player has won the game.
    
    Args:
        board: The game board
        player: Player ID to check for win condition
    Returns:
        True if player has won, False otherwise
    """
    # Check horizontal, vertical, and diagonal for M in a row
    if player == 1:
        if _adjacent_count(board, row, col, player) >= m - 1:
            return True
    elif player == 0:
        if _adjacent_count(board, row, col, player) <= -(m - 1):
            return True
    return False
pass

def _adjacent_count(board, row, col, player):
    """
    Counts adjacent pieces for the given player starting from a position.
    
    Args:
        board: The game board
        row: Starting row index
        col: Starting column index
        player: Player ID to count pieces for
    Returns:
        Count of adjacent pieces
    """
    # Count pieces in all directions (horizontal, vertical, diagonal)
    count = 0
    vertical_count = 0
    horizontal_count = 0
    diagonal_down_right_count = 0
    diagonal_down_left_count = 0

    # Implement counting logic based on your board structure
    if board[row][col] == HUMAN_PIECE:
        if board[row - 1][col] == HUMAN_PIECE:
            horizontal_count += 1 + _adjacent_count(board, row - 1, col, player)
        if board[row + 1][col] == HUMAN_PIECE:
            horizontal_count += 1 + _adjacent_count(board, row + 1, col, player)
        if board[row][col - 1] == HUMAN_PIECE:
            vertical_count += 1 + _adjacent_count(board, row, col - 1, player)
        if board[row][col + 1] == HUMAN_PIECE:
            vertical_count += 1 + _adjacent_count(board, row, col + 1, player)
        if board[row - 1][col + 1] == HUMAN_PIECE:
            diagonal_down_left_count += 1 + _adjacent_count(board, row - 1, col + 1, player)
        if board[row + 1][col - 1] == HUMAN_PIECE:
            diagonal_down_left_count += 1 + _adjacent_count(board, row + 1, col - 1, player)
        if board[row - 1][col - 1] == HUMAN_PIECE:
            diagonal_down_right_count += 1 + _adjacent_count(board, row - 1, col - 1, player)
        if board[row + 1][col + 1] == HUMAN_PIECE:
            diagonal_down_right_count += 1 + _adjacent_count(board, row + 1, col + 1, player)
        count = -1 * max(horizontal_count, vertical_count, diagonal_down_right_count, diagonal_down_left_count)
    elif board[row][col] == COMP_PIECE:
        if board[row - 1][col] == COMP_PIECE:
            horizontal_count += 1 + _adjacent_count(board, row - 1, col, player)
        if board[row + 1][col] == COMP_PIECE:
            horizontal_count += 1 + _adjacent_count(board, row + 1, col, player)
        if board[row][col - 1] == COMP_PIECE:
            vertical_count += 1 + _adjacent_count(board, row, col - 1, player)
        if board[row][col + 1] == COMP_PIECE:
            vertical_count += 1 + _adjacent_count(board, row, col + 1, player)
        if board[row - 1][col + 1] == COMP_PIECE:
            diagonal_down_left_count += 1 + _adjacent_count(board, row - 1, col + 1, player)
        if board[row + 1][col - 1] == COMP_PIECE:
            diagonal_down_left_count += 1 + _adjacent_count(board, row + 1, col - 1, player)
        if board[row - 1][col - 1] == COMP_PIECE:
            diagonal_down_right_count += 1 + _adjacent_count(board, row - 1, col - 1, player)
        if board[row + 1][col + 1] == COMP_PIECE:
            diagonal_down_right_count += 1 + _adjacent_count(board, row + 1, col + 1, player)
        count = max(horizontal_count, vertical_count, diagonal_down_right_count, diagonal_down_left_count)

    return count
pass