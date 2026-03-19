"""
Minimax algorithm implementation for Connect M game.
"""

# Game piece constants
EMPTY_CELL = '0'
HUMAN_PIECE = 'X'
COMP_PIECE = 'O'
AI_PLAYER = 1
HUMAN_PLAYER = 0


def get_best_move(board, depth, m):
    """
    Finds the best move for the AI using minimax algorithm.
    
    Args:
        board: The current game board state
        depth: The maximum depth to search in the game tree
        m: Number of pieces in a row needed to win
    
    Returns:
        The column index of the best move
    """
    best_move = None
    best_score = float('-inf')
    
    for col in _get_valid_moves(board):
        _make_move(board, col, AI_PLAYER)
        score = minimax(board, depth - 1, False, m, float('-inf'), float('inf'))
        _undo_move(board, col)
        
        if score > best_score:
            best_score = score
            best_move = col
    
    return best_move


def minimax(board, depth, is_maximizing, m, alpha=float('-inf'), beta=float('inf')):
    """
    Minimax algorithm with alpha-beta pruning for Connect M game.
    
    Args:
        board: The current game board state
        depth: The current depth in the game tree
        is_maximizing: Boolean indicating if this is a maximizing or minimizing node
        m: Number of pieces in a row needed to win
        alpha: Alpha value for pruning
        beta: Beta value for pruning
    
    Returns:
        The best score for the current position
    """
    # Check terminal states
    terminal_score = _evaluate_terminal_state(board, m)
    if terminal_score is not None:
        return terminal_score + (depth * 0.01)  # Prefer faster wins
    
    if depth == 0:
        return _evaluate_board(board, m)
    
    if is_maximizing:
        max_eval = float('-inf')
        for col in _get_valid_moves(board):
            _make_move(board, col, AI_PLAYER)
            eval_score = minimax(board, depth - 1, False, m, alpha, beta)
            _undo_move(board, col)
            max_eval = max(max_eval, eval_score)
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break  # Beta cutoff
        return max_eval
    else:
        min_eval = float('inf')
        for col in _get_valid_moves(board):
            _make_move(board, col, HUMAN_PLAYER)
            eval_score = minimax(board, depth - 1, True, m, alpha, beta)
            _undo_move(board, col)
            min_eval = min(min_eval, eval_score)
            beta = min(beta, eval_score)
            if beta <= alpha:
                break  # Alpha cutoff
        return min_eval


def _get_valid_moves(board):
    """
    Gets all valid column moves for the current board state.
    
    Returns:
        List of valid column indices
    """
    valid_cols = []
    for col in range(len(board[0])):
        if board[0][col] == EMPTY_CELL:
            valid_cols.append(col)
    return valid_cols


def _make_move(board, col, player):
    """
    Makes a move on the board for the given player.
    
    Args:
        board: The game board
        col: Column to place piece
        player: AI_PLAYER (1) or HUMAN_PLAYER (0)
    """
    piece = COMP_PIECE if player == AI_PLAYER else HUMAN_PIECE
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == EMPTY_CELL:
            board[row][col] = piece
            break


def _undo_move(board, col):
    """
    Undoes the last move in the given column.
    
    Args:
        board: The game board
        col: Column to remove piece from
    """
    for row in range(len(board)):
        if board[row][col] != EMPTY_CELL:
            board[row][col] = EMPTY_CELL
            break


def _check_win(board, row, col, m):
    """
    Checks if there's a winning condition at the given position.
    
    Args:
        board: The game board
        row: Row index of last move
        col: Column index of last move
        m: Number of pieces in a row needed to win
    
    Returns:
        True if there's a win, False otherwise
    """
    piece = board[row][col]
    if piece == EMPTY_CELL:
        return False
    
    rows = len(board)
    cols = len(board[0])
    directions = [
        (0, 1),   # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal (down-right)
        (1, -1),  # diagonal (down-left)
    ]
    
    def count_in_direction(row_delta, col_delta):
        count = 0
        r, c = row + row_delta, col + col_delta
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == piece:
            count += 1
            r += row_delta
            c += col_delta
        return count
    
    for row_delta, col_delta in directions:
        total = 1 + count_in_direction(row_delta, col_delta) + count_in_direction(-row_delta, -col_delta)
        if total >= m:
            return True
    
    return False


def _evaluate_terminal_state(board, m):
    """
    Evaluates if the game has reached a terminal state (win/loss/draw).
    
    Returns:
        Score if terminal, None otherwise
    """
    # Check for wins by checking all pieces on the board
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == COMP_PIECE and _check_win(board, row, col, m):
                return 100  # AI win
            elif board[row][col] == HUMAN_PIECE and _check_win(board, row, col, m):
                return -100  # Opponent win
    
    # Check for draw (no valid moves)
    if not _get_valid_moves(board):
        return 0  # Draw
    
    return None  # Game is not over


def _evaluate_board(board, m):
    """
    Evaluates the current board position heuristically.
    
    Returns:
        An evaluation score
    """
    score = 0
    rows = len(board)
    cols = len(board[0])
    
    # Give preference to center columns
    center_col = cols // 2
    
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == COMP_PIECE:
                # AI piece: positive score
                score += 1
                # Bonus for center positions
                score += (1 - abs(col - center_col) / center_col) * 0.5
                
            elif board[row][col] == HUMAN_PIECE:
                # Opponent piece: negative score
                score -= 1
                score -= (1 - abs(col - center_col) / center_col) * 0.5
    
    return score