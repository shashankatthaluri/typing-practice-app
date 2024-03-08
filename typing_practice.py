import random
import time
from tkinter import Tk, Label, Entry, Button, StringVar, OptionMenu

class TypingPracticeApp:
    def __init__(self, root, word_list):
        self.root = root
        self.word_list = word_list
        self.total_attempts = 0
        self.successful_attempts = 0
        self.total_wpm = 0
        self.total_accuracy = 0
        self.session_count = 0
        self.in_session = False

        self.current_word = StringVar()
        self.user_input = StringVar()
        self.practice_duration = StringVar()
        self.practice_duration.set("15")  # Default duration is 15 seconds

        self.create_widgets()

    def create_widgets(self):
        # Labels
        Label(self.root, text="Type the word and press Enter:").pack(pady=10)
        Label(self.root, textvariable=self.current_word, font=("Helvetica", 18)).pack(pady=20)

        # Entry for user input
        entry = Entry(self.root, textvariable=self.user_input, font=("Helvetica", 18), state="normal")
        entry.pack(pady=10)

        # Dropdown menu for practice duration
        Label(self.root, text="Select practice duration:").pack(pady=10)
        duration_options = ["15", "30", "60"]
        OptionMenu(self.root, self.practice_duration, *duration_options).pack()

        # Stopwatch display
        self.stopwatch_label = Label(self.root, text="", font=("Helvetica", 14))
        self.stopwatch_label.pack(pady=10)

        # Submit/Stop/Restart button
        self.action_button = Button(self.root, text="Start Practice", command=self.toggle_practice, font=("Helvetica", 14))
        self.action_button.pack(pady=10)

        # Stats display
        self.stats_label = Label(self.root, text="", font=("Helvetica", 14))
        self.stats_label.pack(pady=20)

    def toggle_practice(self):
        if not self.in_session:
            self.start_practice()
        else:
            self.stop_practice()

    def start_practice(self):
        self.in_session = True
        self.total_attempts = 0
        self.successful_attempts = 0
        self.root.unbind("<Return>")
        self.root.bind("<Return>", self.check_input)
        self.remaining_time = int(self.practice_duration.get())
        self.root.after(1000, self.update_stopwatch)
        self.root.after(self.remaining_time * 1000, self.end_practice)
        self.next_word()
        self.action_button.config(text="Stop Practice", command=self.stop_practice)

    def stop_practice(self):
        self.in_session = False
        self.root.after_cancel(self.root.after_id)
        self.root.unbind("<Return>")
        self.user_input.set("")
        self.calculate_statistics()
        self.display_stats()
        self.action_button.config(text="Restart Practice", command=self.restart_practice)
        # Remove the user input entry box
        self.root.focus_set()
        self.root.bind("<Return>", lambda event: "break")

    def restart_practice(self):
        self.action_button.config(text="Stop Practice", command=self.stop_practice)
        self.stats_label.config(text="")
        self.start_practice()

    def update_stopwatch(self):
        self.remaining_time -= 1
        self.stopwatch_label.config(text=f"Time left: {self.remaining_time}s")

        if self.remaining_time > 0:
            self.root.after(1000, self.update_stopwatch)
        else:
            self.stop_practice()

    def next_word(self):
        self.user_input.set("")  # Clear the user input
        self.current_word.set(random.choice(self.word_list))
        self.start_time = time.time()

    def check_input(self, event=None):
        self.total_attempts += 1
        user_input = self.user_input.get().strip().lower()
        correct_word = self.current_word.get().lower()

        if user_input == correct_word:
            self.successful_attempts += 1

        if self.remaining_time > 0:
            self.next_word()

    def end_practice(self):
        self.in_session = False
        self.root.unbind("<Return>")
        self.user_input.set("")
        self.calculate_statistics()
        self.display_stats()
        self.action_button.config(text="Restart Practice", command=self.restart_practice)
        # Remove the user input entry box
        self.root.focus_set()
        self.root.bind("<Return>", lambda event: "break")

    def calculate_statistics(self):
        wpm = (len(self.word_list) / (time.time() - self.start_time)) * 60 if time.time() - self.start_time > 0 else 0
        accuracy = (self.successful_attempts / self.total_attempts) * 100 if self.total_attempts > 0 else 0

        self.total_wpm += wpm
        self.total_accuracy += accuracy
        self.session_count += 1

    def display_stats(self):
        if self.session_count > 0:
            average_wpm = self.total_wpm / self.session_count
            average_accuracy = self.total_accuracy / self.session_count
            stats_text = f"Average Words per minute: {average_wpm:.2f} | Average Accuracy: {average_accuracy:.2f}%"
            self.stats_label.config(text=stats_text)

if __name__ == "__main__":
    # Example word list, you can replace it with your own unique word list
    word_list = ["apple", "banana", "cherry", "orange", "grape", "kiwi", "mango", "pear", "strawberry", "watermelon"]

    # Create the Tkinter window
    root = Tk()
    root.title("Typing Practice App")
    root.geometry("400x500")

    # Create the TypingPracticeApp instance
    typing_app = TypingPracticeApp(root, word_list)

    # Run the Tkinter event loop
    root.mainloop()
