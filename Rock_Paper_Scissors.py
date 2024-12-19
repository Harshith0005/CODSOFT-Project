import tkinter as tk
from tkinter import ttk, messagebox
import random
from datetime import datetime
import json
import os

class RockPaperScissors:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock Paper Scissors")
        self.root.geometry("800x600")
        
        self.choices = ["Rock", "Paper", "Scissors"]
        self.user_score = 0
        self.computer_score = 0
        self.rounds_played = 0
        self.game_history = []
        
        self.load_high_score()
        self.setup_gui()
        self.load_statistics()
        
    def setup_gui(self):
        style = ttk.Style()
        style.configure("GameButton.TButton", padding=10, font=("Arial", 12, "bold"))
        style.configure("Score.TLabel", font=("Arial", 14, "bold"))
        style.configure("Result.TLabel", font=("Arial", 16, "bold"))
        
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.setup_score_board(main_frame)
        self.setup_game_area(main_frame)
        self.setup_history_area(main_frame)
        self.setup_statistics_area(main_frame)
        
    def setup_score_board(self, parent):
        score_frame = ttk.LabelFrame(parent, text="Score Board", padding="10")
        score_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        self.user_score_var = tk.StringVar(value="Player: 0")
        self.computer_score_var = tk.StringVar(value="Computer: 0")
        self.high_score_var = tk.StringVar(value=f"High Score: {self.high_score}")
        
        ttk.Label(score_frame, textvariable=self.user_score_var, style="Score.TLabel").grid(row=0, column=0, padx=20)
        ttk.Label(score_frame, textvariable=self.computer_score_var, style="Score.TLabel").grid(row=0, column=1, padx=20)
        ttk.Label(score_frame, textvariable=self.high_score_var, style="Score.TLabel").grid(row=0, column=2, padx=20)
        
    def setup_game_area(self, parent):
        game_frame = ttk.LabelFrame(parent, text="Game Area", padding="10")
        game_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        self.result_var = tk.StringVar()
        ttk.Label(game_frame, textvariable=self.result_var, style="Result.TLabel").grid(row=0, column=0, columnspan=3, pady=10)
        
        self.player_choice_var = tk.StringVar()
        self.computer_choice_var = tk.StringVar()
        
        ttk.Label(game_frame, text="Your Choice:", font=("Arial", 12)).grid(row=1, column=0, columnspan=3, pady=5)
        
        for i, choice in enumerate(self.choices):
            btn = ttk.Button(game_frame, text=choice, style="GameButton.TButton",
                           command=lambda c=choice: self.play_round(c))
            btn.grid(row=2, column=i, padx=10, pady=10)
            
        self.choice_display = ttk.Label(game_frame, text="", font=("Arial", 14))
        self.choice_display.grid(row=3, column=0, columnspan=3, pady=10)
        
    def setup_history_area(self, parent):
        history_frame = ttk.LabelFrame(parent, text="Game History", padding="10")
        history_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10, padx=10)
        
        self.history_text = tk.Text(history_frame, width=30, height=10, font=("Arial", 10))
        self.history_text.pack(fill=tk.BOTH, expand=True)
        
    def setup_statistics_area(self, parent):
        stats_frame = ttk.LabelFrame(parent, text="Statistics", padding="10")
        stats_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        self.stats_vars = {
            "Rounds Played": tk.StringVar(),
            "Win Rate": tk.StringVar(),
            "Most Picked": tk.StringVar(),
            "Best Streak": tk.StringVar()
        }
        
        for i, (stat, var) in enumerate(self.stats_vars.items()):
            ttk.Label(stats_frame, text=stat + ":", font=("Arial", 11)).grid(row=i//2, column=i%2*2, padx=5, pady=5, sticky=tk.E)
            ttk.Label(stats_frame, textvariable=var, font=("Arial", 11, "bold")).grid(row=i//2, column=i%2*2+1, padx=5, pady=5, sticky=tk.W)
            
    def play_round(self, player_choice):
        computer_choice = random.choice(self.choices)
        
        self.player_choice_var.set(player_choice)
        self.computer_choice_var.set(computer_choice)
        
        self.choice_display.config(text=f"You chose {player_choice} - Computer chose {computer_choice}")
        
        result = self.determine_winner(player_choice, computer_choice)
        self.update_scores(result)
        self.update_history(player_choice, computer_choice, result)
        self.update_statistics()
        self.save_statistics()
        
    def determine_winner(self, player_choice, computer_choice):
        if player_choice == computer_choice:
            self.result_var.set("It's a Tie!")
            return "Tie"
            
        winning_combinations = {
            "Rock": "Scissors",
            "Paper": "Rock",
            "Scissors": "Paper"
        }
        
        if winning_combinations[player_choice] == computer_choice:
            self.result_var.set("You Win!")
            return "Win"
        else:
            self.result_var.set("Computer Wins!")
            return "Loss"
            
    def update_scores(self, result):
        if result == "Win":
            self.user_score += 1
        elif result == "Loss":
            self.computer_score += 1
            
        self.rounds_played += 1
        self.user_score_var.set(f"Player: {self.user_score}")
        self.computer_score_var.set(f"Computer: {self.computer_score}")
        
        if self.user_score > self.high_score:
            self.high_score = self.user_score
            self.high_score_var.set(f"High Score: {self.high_score}")
            self.save_high_score()
            
    def update_history(self, player_choice, computer_choice, result):
        timestamp = datetime.now().strftime("%H:%M:%S")
        history_entry = f"{timestamp} - {player_choice} vs {computer_choice}: {result}\n"
        self.game_history.append(history_entry)
        self.history_text.insert(tk.END, history_entry)
        self.history_text.see(tk.END)
        
        if len(self.game_history) > 10:
            self.game_history.pop(0)
            self.history_text.delete("1.0", "2.0")
            
    def update_statistics(self):
        win_rate = (self.user_score / self.rounds_played * 100) if self.rounds_played > 0 else 0
        
        choice_counts = {}
        for entry in self.game_history:
            choice = entry.split(" - ")[1].split(" vs ")[0]
            choice_counts[choice] = choice_counts.get(choice, 0) + 1
            
        most_picked = max(choice_counts.items(), key=lambda x: x[1])[0] if choice_counts else "None"
        
        self.stats_vars["Rounds Played"].set(str(self.rounds_played))
        self.stats_vars["Win Rate"].set(f"{win_rate:.1f}%")
        self.stats_vars["Most Picked"].set(most_picked)
        self.stats_vars["Best Streak"].set(str(self.calculate_best_streak()))
        
    def calculate_best_streak(self):
        current_streak = 0
        best_streak = 0
        
        for entry in self.game_history:
            result = entry.split(": ")[1].strip()
            if result == "Win":
                current_streak += 1
                best_streak = max(best_streak, current_streak)
            else:
                current_streak = 0
                
        return best_streak
        
    def load_high_score(self):
        try:
            with open("rps_high_score.txt", "r") as file:
                self.high_score = int(file.read())
        except FileNotFoundError:
            self.high_score = 0
            
    def save_high_score(self):
        with open("rps_high_score.txt", "w") as file:
            file.write(str(self.high_score))
            
    def load_statistics(self):
        try:
            with open("rps_statistics.json", "r") as file:
                stats = json.load(file)
                self.rounds_played = stats.get("rounds_played", 0)
                self.game_history = stats.get("game_history", [])
                self.update_statistics()
                for entry in self.game_history:
                    self.history_text.insert(tk.END, entry)
        except FileNotFoundError:
            pass
            
    def save_statistics(self):
        stats = {
            "rounds_played": self.rounds_played,
            "game_history": self.game_history
        }
        with open("rps_statistics.json", "w") as file:
            json.dump(stats, file)

if __name__ == "__main__":
    root = tk.Tk()
    app = RockPaperScissors(root)
    root.mainloop()
