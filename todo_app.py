import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime
import os

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced To-Do List")
        self.root.geometry("800x600")
        self.tasks = []
        self.load_tasks()
        self.style = ttk.Style()
        self.style.configure("Priority.High.TLabel", foreground="red")
        self.style.configure("Priority.Medium.TLabel", foreground="orange")
        self.style.configure("Priority.Low.TLabel", foreground="green")
        self.setup_gui()

    def setup_gui(self):
        left_panel = ttk.Frame(self.root, padding="10")
        left_panel.pack(side=tk.LEFT, fill=tk.Y)
        
        ttk.Label(left_panel, text="Task Title:").pack(pady=5)
        self.title_entry = ttk.Entry(left_panel, width=30)
        self.title_entry.pack(pady=5)
        
        ttk.Label(left_panel, text="Description:").pack(pady=5)
        self.desc_text = tk.Text(left_panel, width=30, height=5)
        self.desc_text.pack(pady=5)
        
        ttk.Label(left_panel, text="Due Date (YYYY-MM-DD):").pack(pady=5)
        self.date_entry = ttk.Entry(left_panel, width=30)
        self.date_entry.pack(pady=5)
        
        ttk.Label(left_panel, text="Priority:").pack(pady=5)
        self.priority_var = tk.StringVar(value="Medium")
        priorities = ["High", "Medium", "Low"]
        self.priority_combo = ttk.Combobox(left_panel, textvariable=self.priority_var, values=priorities)
        self.priority_combo.pack(pady=5)
        
        ttk.Label(left_panel, text="Category:").pack(pady=5)
        self.category_entry = ttk.Entry(left_panel, width=30)
        self.category_entry.pack(pady=5)
        
        ttk.Button(left_panel, text="Add Task", command=self.add_task).pack(pady=10)
        ttk.Button(left_panel, text="Update Selected", command=self.update_task).pack(pady=5)
        ttk.Button(left_panel, text="Delete Selected", command=self.delete_task).pack(pady=5)
        
        right_panel = ttk.Frame(self.root, padding="10")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        search_frame = ttk.Frame(right_panel)
        search_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda name, index, mode: self.filter_tasks())
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        self.tree = ttk.Treeview(right_panel, columns=("Title", "Due Date", "Priority", "Category", "Status"), show="headings")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Due Date", text="Due Date")
        self.tree.heading("Priority", text="Priority")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Status", text="Status")
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        
        self.refresh_task_list()

    def add_task(self):
        title = self.title_entry.get().strip()
        if not title:
            messagebox.showerror("Error", "Title is required!")
            return
            
        description = self.desc_text.get("1.0", tk.END).strip()
        due_date = self.date_entry.get().strip()
        priority = self.priority_var.get()
        category = self.category_entry.get().strip()
        
        task = {
            "title": title,
            "description": description,
            "due_date": due_date,
            "priority": priority,
            "category": category,
            "status": "Pending",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.tasks.append(task)
        self.save_tasks()
        self.refresh_task_list()
        self.clear_inputs()

    def update_task(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a task to update!")
            return
            
        index = self.tree.index(selection[0])
        title = self.title_entry.get().strip()
        if not title:
            messagebox.showerror("Error", "Title is required!")
            return
            
        description = self.desc_text.get("1.0", tk.END).strip()
        due_date = self.date_entry.get().strip()
        priority = self.priority_var.get()
        category = self.category_entry.get().strip()
        
        self.tasks[index].update({
            "title": title,
            "description": description,
            "due_date": due_date,
            "priority": priority,
            "category": category
        })
        
        self.save_tasks()
        self.refresh_task_list()
        self.clear_inputs()

    def delete_task(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a task to delete!")
            return
            
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this task?"):
            index = self.tree.index(selection[0])
            self.tasks.pop(index)
            self.save_tasks()
            self.refresh_task_list()
            self.clear_inputs()

    def on_select(self, event):
        selection = self.tree.selection()
        if selection:
            index = self.tree.index(selection[0])
            task = self.tasks[index]
            
            self.title_entry.delete(0, tk.END)
            self.title_entry.insert(0, task["title"])
            
            self.desc_text.delete("1.0", tk.END)
            self.desc_text.insert("1.0", task["description"])
            
            self.date_entry.delete(0, tk.END)
            self.date_entry.insert(0, task["due_date"])
            
            self.priority_var.set(task["priority"])
            
            self.category_entry.delete(0, tk.END)
            self.category_entry.insert(0, task["category"])

    def clear_inputs(self):
        self.title_entry.delete(0, tk.END)
        self.desc_text.delete("1.0", tk.END)
        self.date_entry.delete(0, tk.END)
        self.priority_var.set("Medium")
        self.category_entry.delete(0, tk.END)

    def filter_tasks(self):
        search_term = self.search_var.get().lower()
        self.refresh_task_list(search_term)

    def refresh_task_list(self, search_term=""):
        self.tree.delete(*self.tree.get_children())
        for task in self.tasks:
            if search_term.lower() in task["title"].lower() or search_term.lower() in task["category"].lower():
                self.tree.insert("", tk.END, values=(
                    task["title"],
                    task["due_date"],
                    task["priority"],
                    task["category"],
                    task["status"]
                ))

    def load_tasks(self):
        try:
            with open("tasks.json", "r") as file:
                self.tasks = json.load(file)
        except FileNotFoundError:
            self.tasks = []

    def save_tasks(self):
        with open("tasks.json", "w") as file:
            json.dump(self.tasks, file, indent=2)

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
