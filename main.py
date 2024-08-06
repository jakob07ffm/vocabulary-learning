import tkinter as tk
from tkinter import messagebox

class VocabularyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vocabulary Learning App")

        self.vocab = {
            "aberration": "a departure from what is normal",
            "cogent": "clear, logical, and convincing",
            "denigrate": "criticize unfairly",
            "enervate": "to weaken or drain energy",
            "facetious": "treating serious issues with humor"
        }
        self.words = list(self.vocab.keys())
        self.current_word = ""

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

        self.next_button = tk.Button(self.root, text="Next", command=self.next_word, font=("Helvetica", 16))
        self.next_button.pack(pady=10)

        self.next_word()

    def next_word(self):
        self.current_word = self.words.pop(0)
        self.word_label.config(text=self.current_word)
        self.entry.delete(0, tk.END)

    def check_answer(self):
        user_answer = self.entry.get().strip().lower()
        correct_answer = self.vocab[self.current_word].strip().lower()

        if user_answer == correct_answer:
            messagebox.showinfo("Correct", "That's correct!")
        else:
            messagebox.showerror("Incorrect", f"Wrong! The correct answer is: {correct_answer}")

        if self.words:
            self.next_word()
        else:
            messagebox.showinfo("Done", "You've gone through all the words!")
            self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = VocabularyApp(root)
    root.mainloop()
