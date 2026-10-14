"""
test_minimax.py
---------------
Proves the AI is optimal:
  1. AI vs AI always ends in a draw (perfect play on both sides).
  2. A random player can NEVER beat the AI over many games.
  3. The AI takes an immediate win and blocks an immediate loss.
Run:  python test_minimax.py
"""

import random
import game_logic as g


# both sides play perfectly so it should always be a draw
def ai_vs_ai():
    board = g.new_board()
    turn = g.AI
    while g.check_winner(board) is None:
        if turn == g.AI:
            board[g.best_move(board)] = g.AI
            turn = g.HUMAN
        else:
            # flip roles so the same function plays X optimally
            flipped = [g.AI if c == g.HUMAN else g.HUMAN if c == g.AI else c for c in board]
            board[g.best_move(flipped)] = g.HUMAN
            turn = g.AI
    return g.check_winner(board)


# random player vs ai, ai should never lose
def random_vs_ai(games=500):
    results = {"X": 0, "O": 0, "draw": 0}
    for n in range(games):
        board = g.new_board()
        # take turns on who goes first
        turn = g.HUMAN if n % 2 == 0 else g.AI
        while g.check_winner(board) is None:
            if turn == g.HUMAN:
                # random player just picks any empty square
                board[random.choice(g.available_moves(board))] = g.HUMAN
                turn = g.AI
            else:
                board[g.best_move(board)] = g.AI
                turn = g.HUMAN
        results[g.check_winner(board)] += 1
    return results


if __name__ == "__main__":
    # test 1: ai vs ai
    r = ai_vs_ai()
    print("AI vs AI result:", r)
    assert r == "draw"

    # Takes the win: O O _ on top row
    b = list("OO XX    ")
    assert g.best_move(b) == 2, "AI should complete its row"
    # Blocks the loss: X X _ on top row
    b = list("XX O     ")
    assert g.best_move(b) == 2, "AI should block"

    res = random_vs_ai()
    print("Random player vs AI (500 games):", res)
    assert res["X"] == 0, "AI lost a game — minimax is broken!"
    print("All tests passed ✅")
