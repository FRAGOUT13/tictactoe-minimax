"""
game_logic.py
-------------
Core Tic-Tac-Toe rules + the Minimax AI.
No UI code lives here, so both the CLI and the GUI can reuse it.

Board representation: a list of 9 cells, indexed like this:

     0 | 1 | 2
    ---+---+---
     3 | 4 | 5
    ---+---+---
     6 | 7 | 8

Each cell is "X", "O", or " " (empty).
"""

import math

# X is the player and O is the computer
HUMAN = "X"
AI = "O"
EMPTY = " "

# All 8 ways to get three in a row
WIN_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),   # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),   # columns
    (0, 4, 8), (2, 4, 6),              # diagonals
]


# makes a fresh empty board
def new_board():
    return [EMPTY] * 9


def available_moves(board):
    """Return indices of all empty cells."""
    return [i for i, cell in enumerate(board) if cell == EMPTY]


def check_winner(board):
    """Return 'X' or 'O' if someone has won, 'draw' if board is full, else None."""
    # check every line to see if all 3 are the same
    for a, b, c in WIN_LINES:
        if board[a] != EMPTY and board[a] == board[b] == board[c]:
            return board[a]
    if EMPTY not in board:
        return "draw"
    return None


# ---------------------------------------------------------------------------
# MINIMAX
# ---------------------------------------------------------------------------
# Idea: the AI imagines every possible future game.
#   - The AI is the "maximizer": it wants the highest score.
#   - The human is the "minimizer": we assume they play perfectly and
#     pick the move that's worst for the AI.
# Scores at the end of a game:
#   AI wins  -> +10 - depth   (win sooner = better)
#   Human wins -> depth - 10  (lose later = less bad)
#   Draw     -> 0
# Alpha-beta pruning skips branches that can't change the final decision,
# which makes the search much faster without changing the result.
# ---------------------------------------------------------------------------

def minimax(board, depth, is_maximizing, alpha=-math.inf, beta=math.inf, stats=None):
    if stats is not None:
        stats["nodes"] += 1

    result = check_winner(board)
    if result == AI:
        return 10 - depth
    if result == HUMAN:
        return depth - 10
    if result == "draw":
        return 0

    if is_maximizing:                       # AI's turn
        best = -math.inf
        for move in available_moves(board):
            board[move] = AI                # try the move
            score = minimax(board, depth + 1, False, alpha, beta, stats)
            board[move] = EMPTY             # undo it
            best = max(best, score)
            alpha = max(alpha, best)
            if beta <= alpha:               # prune: human won't allow this branch
                break
        return best
    else:                                   # Human's turn
        best = math.inf
        for move in available_moves(board):
            board[move] = HUMAN
            score = minimax(board, depth + 1, True, alpha, beta, stats)
            board[move] = EMPTY
            best = min(best, score)
            beta = min(beta, best)
            if beta <= alpha:               # prune: AI won't allow this branch
                break
        return best


def best_move(board, return_stats=False):
    """Pick the optimal move for the AI."""
    # counts how many positions it checked
    stats = {"nodes": 0}
    best_score = -math.inf
    move_choice = None
    # try every empty spot and keep the one with best score
    for move in available_moves(board):
        board[move] = AI
        score = minimax(board, 0, False, stats=stats)
        board[move] = EMPTY
        if score > best_score:
            best_score = score
            move_choice = move
    if return_stats:
        return move_choice, best_score, stats["nodes"]
    return move_choice
