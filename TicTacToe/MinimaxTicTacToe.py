import tkinter as tk
from tkinter import messagebox
import os
import json

# Constants
BOARD_SIZE = 3
REWARD = 10
HIGHSCORE_FILE = 'highscores.json'


class TicTacToeGUI:
    def __init__(self, master):
        self.master = master
        self.master.title('Tic Tac Toe')
        self.buttons = {}
        self.highscores = {'PvP_O': 0, 'PvP_X': 0, 'PvC': 0}
        self.load_highscores()
        self.init_mode_selection()

    def init_mode_selection(self):
        self.mode_selection_frame = tk.Frame(self.master)
        self.mode_selection_frame.pack()

        self.board_size_entry = tk.Entry(self.mode_selection_frame)
        self.board_size_entry.pack(side=tk.LEFT)
        self.board_size_entry.insert(0, "3")  # Default to a 3x3 board

        tk.Button(self.mode_selection_frame, text='Player vs Player',
                  command=lambda: self.start_game('PvP')).pack(side=tk.LEFT)
        tk.Button(self.mode_selection_frame, text='Player vs Computer',
                  command=lambda: self.start_game('PvC')).pack(side=tk.LEFT)

    def start_game(self, mode):
        self.game_mode = mode
        try:
            board_size = int(self.board_size_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Board size must be an integer")
            return

        if board_size < 3:
            messagebox.showerror("Error", "Board size must be at least 3")
            return

        self.game = TicTacToe(board_size)
        self.mode_selection_frame.destroy()
        self.init_board()

    def init_board(self):
        for i in range(self.game.size):
            for j in range(self.game.size):
                position = self.game.size * i + j + 1
                button = tk.Button(
                    self.master, text=' ', font=('Arial', 20), height=2, width=5,
                    command=lambda pos=position: self.player_move(pos))
                button.grid(row=i, column=j)
                self.buttons[position] = button

    def player_move(self, position):
        if self.game_mode == 'PvP':
            self.handle_pvp_move(position)
        else:
            self.handle_pvc_move(position)

    def handle_pvp_move(self, position):
        if self.game.is_cell_free(position):
            self.game.update_player_position(self.game.current_player, position)
            self.update_button_text()
            game_over = self.game.check_game_state()
            if game_over:
                if self.game.is_draw():
                    messagebox.showinfo("Game Over", "It's a draw!")
                else:
                    self.update_highscore(self.game.current_player)
                    messagebox.showinfo("Game Over", f"{self.game.current_player} wins!")
                self.display_highscore()
                self.game.reset_game()
                self.reset_board()
            else:
                self.game.switch_player()

    def handle_pvc_move(self, position):
        if self.game.is_cell_free(position):
            self.game.update_player_position(self.game.player, position)
            self.update_button_text()
            if not self.game.check_game_state():
                self.game.move_computer()
                self.update_button_text()
                if self.game.check_game_state():
                    self.update_highscore(self.game.computer)
                    self.display_highscore()
                    self.game.reset_game()
                    self.reset_board()

    def update_button_text(self):
        for position, player in self.game.board.items():
            self.buttons[position].config(text=player)

    def reset_board(self):
        for button in self.buttons.values():
            button.config(text=' ')

    def load_highscores(self):
        if os.path.exists(HIGHSCORE_FILE):
            with open(HIGHSCORE_FILE, 'r') as file:
                self.highscores = json.load(file)

        if 'PvP_O' not in self.highscores:
            self.highscores['PvP_O'] = 0
        if 'PvP_X' not in self.highscores:
            self.highscores['PvP_X'] = 0

    def update_highscore(self, winner):
        if self.game_mode == 'PvP':
            if winner == 'O':
                self.highscores['PvP_O'] += 1
            elif winner == 'X':
                self.highscores['PvP_X'] += 1
        elif winner == self.game.player and self.game_mode == 'PvC':
            self.highscores['PvC'] += 1
        self.save_highscores()

    def display_highscore(self):
        messagebox.showinfo(
            "High Score",
            f"PvP High Score for O: {self.highscores['PvP_O']}\n"
            f"PvP High Score for X: {self.highscores['PvP_X']}\n"
            f"PvC High Score: {self.highscores['PvC']}")

    def save_highscores(self):
        with open(HIGHSCORE_FILE, 'w') as file:
            json.dump(self.highscores, file)


class TicTacToe:
    def __init__(self, size=3):
        self.size = size
        self.board = {i: ' ' for i in range(1, size * size + 1)}
        self.player = 'O'
        self.computer = 'X'
        self.current_player = 'O'

    def reset_game(self):
        self.board = {i: ' ' for i in range(1, 10)}
        self.current_player = 'O'

    def switch_player(self):
        self.current_player = 'X' if self.current_player == 'O' else 'O'

    def update_player_position(self, player, position):
        if self.is_cell_free(position):
            self.board[position] = player
            return True
        return False

    def is_cell_free(self, position):
        return self.board[position] == ' '

    def check_game_state(self):
        if self.is_draw():
            messagebox.showinfo("Game Over", "It's a draw!")
            return True
        if self.is_winning(self.player):
            messagebox.showinfo("Game Over", "Player wins!")
            return True
        if self.is_winning(self.computer):
            messagebox.showinfo("Game Over", "Computer wins!")
            return True
        return False

    def is_winning(self, player):
        for i in range(self.size):
            if all(self.board[i * self.size + j + 1] == player for j in range(self.size)) or \
               all(self.board[j * self.size + i + 1] == player for j in range(self.size)):
                return True
        if all(self.board[i * self.size + i + 1] == player for i in range(self.size)) or \
           all(self.board[i * self.size + (self.size - i)] == player for i in range(self.size)):
            return True
        return False

    def is_draw(self):
        return all(self.board[i] != ' ' for i in range(1, self.size * self.size + 1))

    def move_computer(self):
        best_score = -float('inf')
        best_move = 0
        for position in self.board.keys():
            if self.board[position] == ' ':
                self.board[position] = self.computer
                score = self.minimax(0, False)
                self.board[position] = ' '
                if score > best_score:
                    best_score = score
                    best_move = position
        self.board[best_move] = self.computer
        self.check_game_state()

    def minimax(self, depth, is_maximizer):
        if self.is_winning(self.computer):
            return REWARD - depth
        if self.is_winning(self.player):
            return -REWARD + depth
        if self.is_draw():
            return 0
        if is_maximizer:
            best_score = -float('inf')
            for position in self.board.keys():
                if self.board[position] == ' ':
                    self.board[position] = self.computer
                    score = self.minimax(depth + 1, False)
                    self.board[position] = ' '
                    if score > best_score:
                        best_score = score
            return best_score
        else:
            best_score = float('inf')
            for position in self.board.keys():
                if self.board[position] == ' ':
                    self.board[position] = self.player
                    score = self.minimax(depth + 1, True)
                    self.board[position] = ' '
                    if score < best_score:
                        best_score = score
            return best_score


if __name__ == '__main__':
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()
