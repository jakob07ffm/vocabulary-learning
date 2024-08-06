import tkinter as tk
from tkinter import messagebox
import random

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
        self.score = 0

        self.setup_gui()

    def setup_gui(self):
        self.label = tk.Label(self.root, text="Guess the meaning of the word:", font=("Helvetica", 16))
        self.label.pack(pady=10)

        self.word_label = tk.Label(self.root, text="", font=("Helvetica", 24))
        self.word_label.pack(pady=10)

        self.entry = tk.Entry(self.root, font=("Helvetica", 16))
        self.entry.pack(pady=10)

        self.check_button = tk.Button(self.root, text="Check", command=self.check_answer, font=("Helvetica", 16))
        self.check_button.pack(pady=10)

        self.hint_button = tk.Button(self.root, text="Hint", command=self.show_hint, font=("Helvetica", 16))
        self.hint_button.pack(pady=10)

        self.next_button = tk.Button(self.root, text="Next", command=self.next_word, font=("Helvetica", 16))
        self.next_button.pack(pady=10)

        self.score_label = tk.Label(self.root, text=f"Score: {self.score}", font=("Helvetica", 16))
        self.score_label.pack(pady=10)

        self.next_word()

    def next_word(self):
        if self.words:
            self.current_word = self.words.pop(0)
            self.word_label.config(text=self.current_word)
            self.entry.delete(0, tk.END)
        else:
            messagebox.showinfo("Done", "You've gone through all the words!")
            self.root.quit()

    def check_answer(self):
        user_answer = self.entry.get().strip().lower()
        correct_answer = self.vocab[self.current_word].strip().lower()

        if user_answer == correct_answer:
            self.score += 1
            messagebox.showinfo("Correct", "That's correct!")
        else:
            messagebox.showerror("Incorrect", f"Wrong! The correct answer is: {correct_answer}")

        self.score_label.config(text=f"Score: {self.score}")
        self.next_word()

    def show_hint(self):
        hint = f"Hint: The word starts with '{self.current_word[0]}' and ends with '{self.current_word[-1]}'"
        messagebox.showinfo("Hint", hint)

if __name__ == "__main__":
    root = tk.Tk()
    app = VocabularyApp(root)
    root.mainloop()
