"""
cli.py
------
Play Tic-Tac-Toe against the Minimax AI in your terminal.
Run:  python cli.py
"""

import game_logic as g
from stats import load_stats, record_result, reset_stats, format_stats


def print_board(board):
    # Show cell numbers 1-9 on empty squares so the player knows what to type
    cells = [c if c != g.EMPTY else str(i + 1) for i, c in enumerate(board)]
    print()
    print(f"  {cells[0]} | {cells[1]} | {cells[2]}")
    print("  --+---+--")
    print(f"  {cells[3]} | {cells[4]} | {cells[5]}")
    print("  --+---+--")
    print(f"  {cells[6]} | {cells[7]} | {cells[8]}")
    print()


# keeps asking until the user types a valid empty square
def ask_human_move(board):
    while True:
        choice = input("Your move (1-9): ").strip()
        # make sure its a number between 1 and 9
        if not choice.isdigit() or not 1 <= int(choice) <= 9:
            print("Please enter a number from 1 to 9.")
            continue
        idx = int(choice) - 1
        if board[idx] != g.EMPTY:
            print("That square is taken. Try another.")
            continue
        return idx


def play_one_game(human_first):
    # start with an empty board
    board = g.new_board()
    turn = g.HUMAN if human_first else g.AI

    # keep playing until someone wins or its a draw
    while g.check_winner(board) is None:
        print_board(board)
        if turn == g.HUMAN:
            board[ask_human_move(board)] = g.HUMAN
            turn = g.AI
        else:
            # ai picks its move here
            move, score, nodes = g.best_move(board, return_stats=True)
            board[move] = g.AI
            print(f"AI plays {move + 1}  (searched {nodes} positions, eval {score})")
            turn = g.HUMAN

    print_board(board)
    # game is over, show who won
    result = g.check_winner(board)
    if result == g.HUMAN:
        print("🎉 You won! (That shouldn't happen... check the code!)")
    elif result == g.AI:
        print("🤖 AI wins!")
    else:
        print("🤝 It's a draw!")
    return result


def main():
    # load old stats from the file
    stats = load_stats()
    print("=== Tic-Tac-Toe vs Minimax AI ===")
    print(f"You are {g.HUMAN}, the AI is {g.AI}.")
    print(format_stats(stats))

    human_first = True
    # main menu loop
    while True:
        print("\n[p] Play   [s] Stats   [r] Reset stats   [q] Quit")
        cmd = input("> ").strip().lower()
        if cmd == "p":
            result = play_one_game(human_first)
            stats = record_result(stats, result)
            print(format_stats(stats))
            human_first = not human_first  # alternate who starts
            print(f"Next game: {'you go' if human_first else 'AI goes'} first.")
        elif cmd == "s":
            print(format_stats(stats))
        elif cmd == "r":
            stats = reset_stats()
            print("Stats reset.")
        elif cmd == "q":
            print("Bye!")
            break
        else:
            print("Unknown option.")


if __name__ == "__main__":
    main()
