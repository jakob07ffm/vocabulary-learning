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
        self.load_user_data()
        
        self.setup_gui()
        self.update_timer()

    def setup_gui(self):
        self.user_frame = tk.Frame(self.root)
        self.user_frame.pack(pady=10)

        self.user_label = tk.Label(self.user_frame, text="User:", font=("Helvetica", 16))
        self.user_label.pack(side=tk.LEFT, padx=5)

        self.user_entry = tk.Entry(self.user_frame, font=("Helvetica", 16))
        self.user_entry.pack(side=tk.LEFT, padx=5)
        
        self.user_button = tk.Button(self.user_frame, text="Load User", command=self.load_user, font=("Helvetica", 16))
        self.user_button.pack(side=tk.LEFT, padx=5)
        
        self.label = tk.Label(self.root, text="Guess the meaning of the word:", font=("Helvetica", 16))
        self.label.pack(pady=10)

        self.word_label = tk.Label(self.root, text="", font=("Helvetica", 24))
        self.word_label.pack(pady=10)

        self.option_buttons = []
        for i in range(4):
            button = tk.Button(self.root, text="", font=("Helvetica", 16), command=lambda b=i: self.check_answer(b))
            button.pack(pady=5)
            self.option_buttons.append(button)

        self.hint_button = tk.Button(self.root, text="Hint", command=self.show_hint, font=("Helvetica", 16))
        self.hint_button.pack(pady=10)

        self.next_button = tk.Button(self.root, text="Next", command=self.next_word, font=("Helvetica", 16))
        self.next_button.pack(pady=10)

        self.review_button = tk.Button(self.root, text="Review Incorrect", command=self.review_incorrect, font=("Helvetica", 16))
        self.review_button.pack(pady=10)

        self.score_label = tk.Label(self.root, text=f"Score: {self.score}", font=("Helvetica", 16))
        self.score_label.pack(pady=10)

        self.timer_label = tk.Label(self.root, text=f"Time left: {self.time_left} seconds", font=("Helvetica", 16))
        self.timer_label.pack(pady=10)

        self.stats_label = tk.Label(self.root, text="", font=("Helvetica", 14))
        self.stats_label.pack(pady=10)

        self.next_word()

    def next_word(self):
        if self.words:
            self.current_word = self.words.pop(0)
            self.word_label.config(text=self.current_word)
            self.time_left = 30
            self.set_options()
        else:
            messagebox.showinfo("Done", "You've gone through all the words!")
            self.save_user_data()
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
            self.correct_answers += 1
            messagebox.showinfo("Correct", "That's correct!")
        else:
            self.incorrect_answers.append(self.current_word)
            messagebox.showerror("Incorrect", f"Wrong! The correct answer is: {correct_answer}")

        self.update_stats()
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

    def load_user(self):
        self.user_name = self.user_entry.get().strip()
        if self.user_name:
            self.load_user_data()
            self.update_stats()
            messagebox.showinfo("User Loaded", f"User {self.user_name} loaded successfully!")

    def load_user_data(self):
        self.user_name = self.user_entry.get().strip() or "default"
        self.score = 0
        self.correct_answers = 0
        self.incorrect_answers = []
        self.time_left = 30
        self.stats = {
            'total_words_attempted': 0,
            'correct_answers': 0,
            'accuracy': 0.0
        }
        if os.path.exists(f'{self.user_name}_data.json'):
            with open(f'{self.user_name}_data.json', 'r') as file:
                data = json.load(file)
                self.score = data.get('score', 0)
                self.correct_answers = data.get('correct_answers', 0)
                self.incorrect_answers = data.get('incorrect_answers', [])
                self.stats = data.get('stats', self.stats)

    def save_user_data(self):
        data = {
            'score': self.score,
            'correct_answers': self.correct_answers,
            'incorrect_answers': self.incorrect_answers,
            'stats': self.stats
        }
        with open(f'{self.user_name}_data.json', 'w') as file:
            json.dump(data, file)

    def review_incorrect(self):
        if self.incorrect_answers:
            self.words = self.incorrect_answers + self.words
            self.incorrect_answers = []
            messagebox.showinfo("Review", "You will now review the words you answered incorrectly.")
            self.next_word()
        else:
            messagebox.showinfo("Review", "No incorrect words to review!")

    def update_stats(self):
        self.stats['total_words_attempted'] += 1
        self.stats['correct_answers'] = self.correct_answers
        if self.stats['total_words_attempted'] > 0:
            self.stats['accuracy'] = (self.correct_answers / self.stats['total_words_attempted']) * 100
        self.stats_label.config(
            text=f"Words Attempted: {self.stats['total_words_attempted']}, "
                 f"Correct: {self.correct_answers}, "
                 f"Accuracy: {self.stats['accuracy']:.2f}%"
        )

if __name__ == "__main__":
    root = tk.Tk()
    app = VocabularyApp(root)
    root.mainloop()
