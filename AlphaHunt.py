import tkinter as tk
from tkinter import messagebox, Toplevel
import random

words = ['python', 'hangman', 'interface', 'animation', 'programming', 'banana', 'guitar']

class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🎯 AlphaHunt")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0faff")  # Vibrant sky background

        self.word = random.choice(words)
        self.guesses = []
        self.max_wrong = 6
        self.wrong = 0

        self.title = tk.Label(root, text="AlphaHunt", font=("Trebuchet MS", 30, "bold"),
                              bg="#f0faff", fg="#005377")
        self.title.pack(pady=10)

        self.canvas = tk.Canvas(root, width=350, height=300, bg="white",
                                highlightthickness=4, highlightbackground="#0077b6")
        self.canvas.pack(pady=10)

        self.word_label = tk.Label(root, text='', font=('Courier New', 26, 'bold'),
                                   bg="#f0faff", fg="#111")
        self.word_label.pack(pady=10)

        self.buttons_frame = tk.Frame(root, bg="#f0faff")
        self.buttons_frame.pack(pady=10)

        self.bottom_frame = tk.Frame(root, bg="#f0faff")
        self.bottom_frame.pack(pady=15)

        self.reset_button = self.create_modern_button(self.bottom_frame, "🔄 Restart", self.reset_game, "#48cae4")
        self.reset_button.grid(row=0, column=0, padx=20)

        self.exit_button = self.create_modern_button(self.bottom_frame, "🚪 Exit Game", self.exit_game, "#ff6b6b")
        self.exit_button.grid(row=0, column=1, padx=20)

        self.draw_base()
        self.create_letter_buttons()
        self.update_word_display()

    def create_modern_button(self, parent, text, command, bg_color):
        btn = tk.Button(parent, text=text, command=command,
                        font=("Segoe UI", 12, "bold"),
                        bg=bg_color, fg="white", activebackground="#023e8a",
                        relief="flat", bd=0, padx=20, pady=10, cursor="hand2")
        return btn

    def draw_base(self):
        self.canvas.delete("all")
        self.canvas.create_line(20, 280, 180, 280, width=4)
        self.canvas.create_line(100, 280, 100, 50, width=4)
        self.canvas.create_line(100, 50, 200, 50, width=4)
        self.canvas.create_line(200, 50, 200, 80, width=4)

    def draw_hangman(self):
        if self.wrong == 1:
            self.canvas.create_oval(180, 80, 220, 120, width=3)
        elif self.wrong == 2:
            self.canvas.create_line(200, 120, 200, 180, width=3)
        elif self.wrong == 3:
            self.canvas.create_line(200, 140, 170, 160, width=3)
        elif self.wrong == 4:
            self.canvas.create_line(200, 140, 230, 160, width=3)
        elif self.wrong == 5:
            self.canvas.create_line(200, 180, 170, 220, width=3)
        elif self.wrong == 6:
            self.canvas.create_line(200, 180, 230, 220, width=3)
            self.show_animated_popup(False)

    def create_letter_buttons(self):
        for widget in self.buttons_frame.winfo_children():
            widget.destroy()
        letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        for i, letter in enumerate(letters):
            btn = tk.Button(self.buttons_frame, text=letter, width=4, height=2,
                            font=('Segoe UI', 11, 'bold'), bg="#ffffff", fg="#0077b6",
                            activebackground="#caf0f8", relief="raised", bd=1,
                            command=lambda l=letter: self.make_guess(l.lower()))
            btn.grid(row=i//9, column=i%9, padx=5, pady=5)

    def update_word_display(self):
        display = ''
        for char in self.word:
            if char in self.guesses:
                display += f'{char} '
            else:
                display += '_ '
        self.word_label.config(text=display.strip())

        if '_' not in display:
            self.show_animated_popup(True)

    def make_guess(self, letter):
        if letter in self.guesses:
            return
        self.guesses.append(letter)
        if letter not in self.word:
            self.wrong += 1
            self.draw_hangman()
        self.update_word_display()

    def reset_game(self):
        self.word = random.choice(words)
        self.guesses = []
        self.wrong = 0
        self.draw_base()
        self.update_word_display()
        self.create_letter_buttons()

    def show_animated_popup(self, won):
        msg = "🎉 You won! The word was: " + self.word if won else "💀 You lost! The word was: " + self.word

        popup = Toplevel(self.root)
        popup.geometry("400x200")
        popup.title("Game Over")
        popup.config(bg="#f0faff")
        popup.attributes("-topmost", True)
        popup.attributes("-alpha", 0.0)

        msg_label = tk.Label(popup, text=msg, font=("Segoe UI", 14, "bold"), bg="#f0faff", fg="#333")
        msg_label.pack(pady=30)

        close_btn = self.create_modern_button(popup, "OK", popup.destroy, "#00b4d8")
        close_btn.pack(pady=10)

        # Simulate fade-in animation
        self.fade_in(popup)

        for child in self.buttons_frame.winfo_children():
            child.config(state='disabled')

    def fade_in(self, window, alpha=0.0):
        alpha += 0.05
        if alpha <= 1.0:
            window.attributes("-alpha", alpha)
            self.root.after(30, lambda: self.fade_in(window, alpha))

    def exit_game(self):
        popup = Toplevel(self.root)
        popup.geometry("350x150")
        popup.title("Exit")
        popup.config(bg="#f0faff")
        popup.attributes("-topmost", True)
        popup.attributes("-alpha", 0.0)

        lbl = tk.Label(popup, text="🎮 Thanks for playing!", font=("Segoe UI", 14, "bold"), bg="#f0faff", fg="#444")
        lbl.pack(pady=30)

        exit_btn = self.create_modern_button(popup, "Exit Now", self.root.destroy, "#ef476f")
        exit_btn.pack()

        self.fade_in(popup)

if __name__ == "__main__":
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()
