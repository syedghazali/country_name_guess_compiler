import tkinter as tk
from tkinter import ttk, messagebox
from lexer import Lexer
from compiler import Compiler

class GameGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Country Guess: Cute UI")
        self.master.geometry("480x360")
        self.master.resizable(False, False)

        self.style = ttk.Style()
        self.style.theme_use('clam')  # nicer theme

        # cute colors
        self.bg = '#FFEFD5'  # papaya whip
        self.card = '#FFF8DC'  # cornsilk
        self.accent = '#FF7F50'  # coral

        self.master.configure(bg=self.bg)

        self.create_widgets()
        self.reset_game_state()

    def create_widgets(self):
        # Title
        self.title_label = tk.Label(self.master, text="Country Guess", font=("Comic Sans MS", 20, 'bold'), bg=self.bg, fg=self.accent)
        self.title_label.pack(pady=10)

        # Frame for content
        self.card_frame = tk.Frame(self.master, bg=self.card, bd=2, relief=tk.RIDGE)
        self.card_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        # Game Title (from file)
        self.game_title_var = tk.StringVar(value="---")
        self.game_title_lbl = tk.Label(self.card_frame, textvariable=self.game_title_var, bg=self.card, font=("Segoe UI", 14, 'bold'))
        self.game_title_lbl.pack(pady=(8, 4))
        # Current level label
        self.level_var = tk.StringVar(value='Level: -')
        self.level_lbl = tk.Label(self.card_frame, textvariable=self.level_var, bg=self.card, font=("Segoe UI", 10))
        self.level_lbl.pack()

        # Hint
        self.hint_var = tk.StringVar(value="Hint: ...")
        self.hint_lbl = tk.Label(self.card_frame, textvariable=self.hint_var, bg=self.card, font=("Segoe UI", 12))
        self.hint_lbl.pack(pady=4)

        # Lives
        self.lives_var = tk.StringVar(value="Lives: 0")
        self.lives_lbl = tk.Label(self.card_frame, textvariable=self.lives_var, bg=self.card, font=("Segoe UI", 11))
        self.lives_lbl.pack(pady=4)

        # Guess Entry
        self.entry_var = tk.StringVar()
        self.guess_entry = ttk.Entry(self.card_frame, textvariable=self.entry_var, font=("Segoe UI", 12))
        self.guess_entry.pack(pady=8)
        self.guess_entry.bind('<Return>', lambda e: self.submit_guess())

        # Buttons frame
        btn_frame = tk.Frame(self.card_frame, bg=self.card)
        btn_frame.pack(pady=6)

        self.submit_btn = ttk.Button(btn_frame, text="Submit", command=self.submit_guess)
        self.submit_btn.grid(row=0, column=0, padx=8)
        self.reset_btn = ttk.Button(btn_frame, text="Reset", command=self.reset_state_from_file)
        self.reset_btn.grid(row=0, column=1, padx=8)
        self.exit_btn = ttk.Button(btn_frame, text="Exit", command=self.master.quit)
        self.exit_btn.grid(row=0, column=2, padx=8)

        # Feedback
        self.feedback_var = tk.StringVar(value="Good luck! ✨")
        self.feedback_lbl = tk.Label(self.card_frame, textvariable=self.feedback_var, bg=self.card, font=("Segoe UI", 11), fg='black')
        self.feedback_lbl.pack(pady=(6,10))

        # Footer
        footer = tk.Label(self.master, text="Tip: Press Enter to submit your guess.", bg=self.bg, font=("Segoe UI", 9), fg='#6b6b6b')
        footer.pack(pady=(0, 6))

    def reset_game_state(self):
        self.source = None
        self.lexer = None
        self.compiler = None
        self.title = "Country Guess"
        self.max_lives = 1
        self.hint = ""
        self.target = ""
        self.levels = []
        self.current_level_index = 0
        self.lives = 1
        self.update_ui()

    def reset_state_from_file(self):
        try:
            with open('game.cgs', 'r') as f:
                self.source = f.read()
        except FileNotFoundError:
            messagebox.showerror("Missing file", "Could not find 'game.cgs' in the working directory.")
            return

        try:
            self.lexer = Lexer(self.source)
            self.compiler = Compiler(self.lexer)
            # parse only (do not invoke CLI runtime for SOLVE)
            self.compiler.run(execute_on_solve=False)
            state = self.compiler.get_state()

            self.title = state.get('title') or 'Country Guess'
            self.max_lives = state.get('max_lives') or 1
            self.hint = state.get('hint') or ''
            self.target = state.get('target') or ''
            self.levels = state.get('levels') or []
            self.current_level_index = 0

            # If levels are present, prefer them; otherwise fall back to single target
            if self.levels:
                lvl = self.levels[self.current_level_index]
                self.target = lvl.get('target') or self.target
                self.hint = lvl.get('hint') or self.hint

            self.lives = self.max_lives
            self.feedback_var.set('Game loaded. Good luck! ✨')
            self.update_ui()
        except Exception as e:
            messagebox.showerror("Parse Error", f"Could not parse 'game.cgs' file:\n{e}")

    def update_ui(self):
        self.game_title_var.set(self.title)
        # show level number
        total_levels = len(self.levels) if hasattr(self, 'levels') else 0
        if total_levels:
            lvl_num = self.levels[self.current_level_index].get('level')
            self.level_var.set(f'Level: {lvl_num} of {total_levels}')
        else:
            self.level_var.set('Level: -')
        hearts = ' '.join(['❤️'] * max(0, self.lives))
        self.lives_var.set(f"Lives: {self.lives}  {hearts}")
        self.hint_var.set(f"Hint: {self.hint}")
        # Enable/disable controls depending on whether a target is present
        if not self.target:
            self.submit_btn.state(['disabled'])
            self.guess_entry.state(['disabled'])
            self.feedback_var.set('No level target loaded. Use Reset to reload file.')
        else:
            self.submit_btn.state(['!disabled'])
            self.guess_entry.state(['!disabled'])
            self.guess_entry.focus_set()

    def submit_guess(self):
        guess = self.entry_var.get().strip()
        if not guess:
            self.feedback_var.set('Please type a guess!')
            return

        # Compare case-insensitive
        if guess.lower() == (self.target or '').lower():
            self.feedback_var.set('>>> CORRECT! 🎉 You passed this level. <<<')
            messagebox.showinfo('Well done!', f'✅ CORRECT! The answer was\n{self.target}')
            self.entry_var.set('')
            # Advance to next level if any
            if hasattr(self, 'levels') and self.levels and self.current_level_index < len(self.levels) - 1:
                self.current_level_index += 1
                lvl = self.levels[self.current_level_index]
                self.target = lvl.get('target') or ''
                self.hint = lvl.get('hint') or ''
                self.lives = self.max_lives
                self.feedback_var.set('New level loaded!')
                self.update_ui()
            else:
                # No more levels; ask to restart
                res = messagebox.askyesno('Victory', 'You finished all levels! Play again?')
                if res:
                    self.reset_state_from_file()
                else:
                    self.master.quit()
        else:
            self.lives -= 1
            if self.lives <= 0:
                self.update_ui()
                self.feedback_var.set('GAME OVER. ☹️')
                messagebox.showinfo('Game Over', f'Game over. The answer was {self.target}')
                # Reset to allow replay
                self.reset_state_from_file()
            else:
                self.feedback_var.set('>>> WRONG! Try again!')
                self.entry_var.set('')
                self.update_ui()


if __name__ == '__main__':
    root = tk.Tk()
    app = GameGUI(root)
    # load states
    app.reset_state_from_file()
    root.mainloop()
