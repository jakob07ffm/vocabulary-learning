import tkinter as tk
from tkinter import messagebox
import random
import json
import os

class VocabularyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vocabulary Learning App")
        
        self.vocab = {
            "aberration": "a departure from what is normal",
            "cogent": "clear, logical, and convincing",
            "denigrate": "criticize unfairly",
            "enervate": "to weaken or drain energy",
            "facetious": "treating serious issues with humor",
            "laconic": "using very few words",
            "munificent": "larger or more generous than usual",
            "obdurate": "stubbornly refusing to change one's opinion",
            "pulchritudinous": "beautiful",
            "quixotic": "exceedingly idealistic; unrealistic and impractical",
            "sagacious": "having good judgment; wise"
        }
        self.words = list(self.vocab.keys())
        random.shuffle(self.words)
        self.current_word = ""
        self.score = self.load_score()
        self.time_left = 30

        self.setup_gui()
        self.update_timer()

    def setup_gui(self):
        self.label = tk.Label(self.root, text="Guess the meaning of the word:", font=("Helvetica", 16))
        self.label.pack(pady=10)

        self.word_label = tk.Label(self.root, text="", font=("Helvetica", 24))
        self.word_label.pack(pady=10)

        self.option_buttons = []
        for _ in range(4):
            button = tk.Button(self.root, text="", font=("Helvetica", 16), command=lambda b=_: self.check_answer(b))
            button.pack(pady=5)
            self.option_buttons.append(button)

        self.hint_button = tk.Button(self.root, text="Hint", command=self.show_hint, font=("Helvetica", 16))
        self.hint_button.pack(pady=10)

        self.next_button = tk.Button(self.root, text="Next", command=self.next_word, font=("Helvetica", 16))
        self.next_button.pack(pady=10)

        self.score_label = tk.Label(self.root, text=f"Score: {self.score}", font=("Helvetica", 16))
        self.score_label.pack(pady=10)

        self.timer_label = tk.Label(self.root, text=f"Time left: {self.time_left} seconds", font=("Helvetica", 16))
        self.timer_label.pack(pady=10)

        self.next_word()

    def next_word(self):
        if self.words:
            self.current_word = self.words.pop(0)
            self.word_label.config(text=self.current_word)
            self.time_left = 30
            self.set_options()
        else:
            messagebox.showinfo("Done", "You've gone through all the words!")
            self.save_score()
            self.root.quit()

    def set_options(self):
        correct_answer = self.vocab[self.current_word]
        options = [correct_answer] + random.sample(
            [meaning for word, meaning in self.vocab.items() if word != self.current_word], 3)
        random.shuffle(options)
        for button, option in zip(self.option_buttons, options):
            button.config(text=option)

    def check_answer(self, button_index):
        user_answer = self.option_buttons[button_index].cget("text")
        correct_answer = self.vocab[self.current_word]

        if user_answer == correct_answer:
            self.score += 1
            messagebox.showinfo("Correct", "That's correct!")
        else:
            messagebox.showerror("Incorrect", f"Wrong! The correct answer is: {correct_answer}")

        self.score_label.config(text=f"Score: {self.score}")
        self.next_word()

    def show_hint(self):
        correct_answer = self.vocab[self.current_word]
        hint = f"Hint: {correct_answer[:len(correct_answer)//2]}..."
        messagebox.showinfo("Hint", hint)

    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=f"Time left: {self.time_left} seconds")
            self.root.after(1000, self.update_timer)
        else:
            self.time_left = 30
            messagebox.showinfo("Time's up", "You ran out of time!")
            self.next_word()

    def load_score(self):
        if os.path.exists('score.json'):
            with open('score.json', 'r') as file:
                return json.load(file).get('score', 0)
        return 0

    def save_score(self):
        with open('score.json', 'w') as file:
            json.dump({'score': self.score}, file)

if __name__ == "__main__":
    root = tk.Tk()
    app = VocabularyApp(root)
    root.mainloop()
