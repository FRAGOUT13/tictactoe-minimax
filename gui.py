"""
gui.py
------
Simple Tkinter GUI for Tic-Tac-Toe vs the Minimax AI.
Run:  python gui.py
(Tkinter ships with standard Python on Windows/macOS.
 On Ubuntu/Debian: sudo apt install python3-tk)
"""

import tkinter as tk
import game_logic as g
from stats import load_stats, record_result, reset_stats, format_stats

AI_DELAY_MS = 350  # small pause so the AI move feels natural


class TicTacToeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe vs Minimax")
        self.root.resizable(False, False)

        self.stats = load_stats()
        self.human_first = True
        self.board = g.new_board()
        self.game_over = False

        # label at the top that shows whose turn it is
        self.status = tk.Label(root, text="", font=("Arial", 14))
        self.status.grid(row=0, column=0, columnspan=3, pady=(10, 5))

        # make the 9 buttons for the board
        self.buttons = []
        for i in range(9):
            btn = tk.Button(root, text="", font=("Arial", 32, "bold"),
                            width=3, height=1,
                            command=lambda i=i: self.on_click(i))
            btn.grid(row=1 + i // 3, column=i % 3, padx=3, pady=3)
            self.buttons.append(btn)

        self.stats_label = tk.Label(root, text="", font=("Arial", 11))
        self.stats_label.grid(row=4, column=0, columnspan=3, pady=5)

        # new game and reset buttons at the bottom
        controls = tk.Frame(root)
        controls.grid(row=5, column=0, columnspan=3, pady=(0, 10))
        tk.Button(controls, text="New Game", command=self.new_game).pack(side="left", padx=5)
        tk.Button(controls, text="Reset Stats", command=self.on_reset).pack(side="left", padx=5)

        self.new_game()

    # ---------- game flow ----------
    # clear everything and start again
    def new_game(self):
        self.board = g.new_board()
        self.game_over = False
        for btn in self.buttons:
            btn.config(text="", state="normal", bg="SystemButtonFace" if self._is_windows() else "#f0f0f0")
        self.update_stats_label()
        if self.human_first:
            self.status.config(text="Your turn (X)")
        else:
            self.status.config(text="AI is thinking...")
            self.root.after(AI_DELAY_MS, self.ai_turn)

    def on_click(self, i):
        # ignore the click if game ended or square is already used
        if self.game_over or self.board[i] != g.EMPTY:
            return
        self.place(i, g.HUMAN)
        if not self.check_end():
            self.status.config(text="AI is thinking...")
            self.set_buttons_enabled(False)
            self.root.after(AI_DELAY_MS, self.ai_turn)

    def ai_turn(self):
        # ask game_logic for the best move
        move = g.best_move(self.board)
        self.place(move, g.AI)
        if not self.check_end():
            self.status.config(text="Your turn (X)")
            self.set_buttons_enabled(True)

    def place(self, i, player):
        self.board[i] = player
        # blue for player, red for ai
        color = "#1565c0" if player == g.HUMAN else "#c62828"
        self.buttons[i].config(text=player, disabledforeground=color, fg=color)

    def check_end(self):
        result = g.check_winner(self.board)
        if result is None:
            return False
        self.game_over = True
        self.highlight_win()
        self.set_buttons_enabled(False)
        if result == g.HUMAN:
            self.status.config(text="🎉 You won!")
        elif result == g.AI:
            self.status.config(text="🤖 AI wins!")
        else:
            self.status.config(text="🤝 Draw!")
        self.stats = record_result(self.stats, result)
        self.update_stats_label()
        self.human_first = not self.human_first  # alternate starts
        return True

    # ---------- helpers ----------
    def highlight_win(self):
        # find the winning line and make it yellow
        for a, b, c in g.WIN_LINES:
            if self.board[a] != g.EMPTY and self.board[a] == self.board[b] == self.board[c]:
                for idx in (a, b, c):
                    self.buttons[idx].config(bg="#fff59d")

    def set_buttons_enabled(self, enabled):
        for i, btn in enumerate(self.buttons):
            if enabled and self.board[i] == g.EMPTY and not self.game_over:
                btn.config(state="normal")
            else:
                btn.config(state="disabled")

    def update_stats_label(self):
        self.stats_label.config(text=format_stats(self.stats))

    def on_reset(self):
        self.stats = reset_stats()
        self.update_stats_label()

    @staticmethod
    def _is_windows():
        import sys
        return sys.platform.startswith("win")


if __name__ == "__main__":
    # create the window and run the app
    root = tk.Tk()
    TicTacToeApp(root)
    root.mainloop()
