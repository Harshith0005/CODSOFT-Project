import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import re
from datetime import datetime

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Password Generator")
        self.root.geometry("600x700")
        
        self.password_history = []
        self.setup_gui()

    def setup_gui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(main_frame, text="Password Generator", font=('Helvetica', 16, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)

        self.length_var = tk.StringVar(value="12")
        ttk.Label(main_frame, text="Password Length:").grid(row=1, column=0, sticky=tk.W)
        self.length_entry = ttk.Entry(main_frame, textvariable=self.length_var, width=10)
        self.length_entry.grid(row=1, column=1, sticky=tk.W)

        self.uppercase_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(main_frame, text="Uppercase Letters", variable=self.uppercase_var).grid(row=2, column=0, sticky=tk.W)

        self.lowercase_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(main_frame, text="Lowercase Letters", variable=self.lowercase_var).grid(row=3, column=0, sticky=tk.W)

        self.digits_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(main_frame, text="Numbers", variable=self.digits_var).grid(row=4, column=0, sticky=tk.W)

        self.symbols_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(main_frame, text="Special Characters", variable=self.symbols_var).grid(row=5, column=0, sticky=tk.W)

        self.avoid_similar_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(main_frame, text="Avoid Similar Characters (1, l, I, 0, O)", variable=self.avoid_similar_var).grid(row=6, column=0, columnspan=2, sticky=tk.W)

        ttk.Button(main_frame, text="Generate Password", command=self.generate_password).grid(row=7, column=0, columnspan=2, pady=10)

        self.result_var = tk.StringVar()
        result_entry = ttk.Entry(main_frame, textvariable=self.result_var, font=('Courier', 12), width=40)
        result_entry.grid(row=8, column=0, columnspan=2, pady=5)

        ttk.Button(main_frame, text="Copy to Clipboard", command=self.copy_to_clipboard).grid(row=9, column=0, columnspan=2, pady=5)

        strength_frame = ttk.LabelFrame(main_frame, text="Password Strength", padding="5")
        strength_frame.grid(row=10, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))

        self.strength_var = tk.StringVar(value="")
        self.strength_label = ttk.Label(strength_frame, textvariable=self.strength_var)
        self.strength_label.pack()

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(strength_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, pady=5)

        history_frame = ttk.LabelFrame(main_frame, text="Password History", padding="5")
        history_frame.grid(row=11, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))

        self.history_text = tk.Text(history_frame, height=8, width=50)
        self.history_text.pack()

    def generate_password(self):
        try:
            length = int(self.length_var.get())
            if length < 8:
                messagebox.showerror("Error", "Password length must be at least 8 characters")
                return
            if length > 100:
                messagebox.showerror("Error", "Password length must not exceed 100 characters")
                return

            chars = ""
            if not any([self.uppercase_var.get(), self.lowercase_var.get(), 
                       self.digits_var.get(), self.symbols_var.get()]):
                messagebox.showerror("Error", "Please select at least one character type")
                return

            if self.uppercase_var.get():
                chars += string.ascii_uppercase
            if self.lowercase_var.get():
                chars += string.ascii_lowercase
            if self.digits_var.get():
                chars += string.digits
            if self.symbols_var.get():
                chars += string.punctuation

            if self.avoid_similar_var.get():
                chars = chars.translate(str.maketrans("", "", "1lI0O"))

            password = ""
            while not self.validate_password(password):
                password = "".join(random.choice(chars) for _ in range(length))

            self.result_var.set(password)
            self.evaluate_strength(password)
            self.add_to_history(password)

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for password length")

    def validate_password(self, password):
        if not password:
            return False
            
        requirements = [
            (self.uppercase_var.get(), lambda p: any(c.isupper() for c in p)),
            (self.lowercase_var.get(), lambda p: any(c.islower() for c in p)),
            (self.digits_var.get(), lambda p: any(c.isdigit() for c in p)),
            (self.symbols_var.get(), lambda p: any(c in string.punctuation for c in p))
        ]

        return all(func(password) for req, func in requirements if req)

    def evaluate_strength(self, password):
        score = 0
        feedback = []

        if len(password) >= 12:
            score += 25
            feedback.append("Good length")
        elif len(password) >= 8:
            score += 10
            feedback.append("Minimum length met")

        if any(c.isupper() for c in password):
            score += 20
            feedback.append("Contains uppercase")
        if any(c.islower() for c in password):
            score += 20
            feedback.append("Contains lowercase")
        if any(c.isdigit() for c in password):
            score += 20
            feedback.append("Contains numbers")
        if any(c in string.punctuation for c in password):
            score += 20
            feedback.append("Contains symbols")

        entropy = len(set(password)) / len(password)
        score = min(100, score + int(entropy * 20))

        self.progress_var.set(score)
        strength_text = "Weak"
        if score >= 80:
            strength_text = "Very Strong"
        elif score >= 60:
            strength_text = "Strong"
        elif score >= 40:
            strength_text = "Moderate"

        self.strength_var.set(f"Strength: {strength_text} ({score}%)\n" + "\n".join(feedback))

    def copy_to_clipboard(self):
        password = self.result_var.get()
        if password:
            pyperclip.copy(password)
            messagebox.showinfo("Success", "Password copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "No password to copy!")

    def add_to_history(self, password):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.password_history.append(f"{timestamp}: {password}")
        self.update_history_display()

    def update_history_display(self):
        self.history_text.delete(1.0, tk.END)
        for entry in reversed(self.password_history[-10:]):
            self.history_text.insert(tk.END, entry + "\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()
