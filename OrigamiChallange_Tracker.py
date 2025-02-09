import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime
import os

class OrigamiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Origami Learning System 🎯")
        self.root.geometry("1000x700")
   
        self.progress_data = self.load_progress()
        self.current_design = None
        
        self.origami_designs = {
            "beginner": {
                "title": "Beginner Level",
                "designs": {
                    "crane": {
                        "name": "Paper Crane",
                        "time": "15 minutes",
                        "completed": False,
                        "steps": [
                            "Start with a square piece of paper, colored side down",
                            "Fold in half diagonally to make a triangle",
                            "Fold in half again to make a smaller triangle",
                            "Open up to the first triangle",
                            "Fold the top triangle down to the bottom edge",
                            "Fold the sides in to the center line",
                            "Fold the top down and bottom up to make preliminary base",
                            "Fold the wings down",
                            "Fold the head down and shape"
                        ]
                    },
                    "boat": {
                        "name": "Simple Boat",
                        "time": "10 minutes",
                        "completed": False,
                        "steps": [
                            "Start with a rectangular piece of paper",
                            "Fold in half lengthwise",
                            "Fold the top corners to the center line",
                            "Fold up the bottom edges",
                            "Pull the sides apart and flatten"
                        ]
                    },
                    "heart": {
                        "name": "Simple Heart",
                        "time": "10 minutes",
                        "completed": False,
                        "steps": [
                            "Start with a square paper",
                            "Fold diagonally to make a triangle",
                            "Fold the top point down about halfway",
                            "Fold the bottom corners up to meet at the top",
                            "Fold the outer edges inward slightly to round them"
                        ]
                    }
                }
            },
            "intermediate": {
                "title": "Intermediate Level",
                "designs": {
                    "butterfly": {
                        "name": "Butterfly",
                        "time": "25 minutes",
                        "completed": False,
                        "steps": [
                            "Start with a square piece of paper",
                            "Create a preliminary base",
                            "Fold the top point down about halfway",
                            "Fold the wings back",
                            "Create the body by folding in the center",
                            "Shape the wings and adjust"
                        ]
                    },
                    "lily": {
                        "name": "Lily Flower",
                        "time": "30 minutes",
                        "completed": False,
                        "steps": [
                            "Start with a square paper",
                            "Make a preliminary base",
                            "Form the petals by folding corners",
                            "Shape each petal carefully",
                            "Create the stem by folding the remaining paper",
                            "Adjust and spread petals evenly"
                        ]
                    },
                    "star": {
                        "name": "Modular Star",
                        "time": "35 minutes",
                        "completed": False,
                        "steps": [
                            "Prepare 5 square pieces of paper",
                            "Create individual units",
                            "Fold each unit into a triangle",
                            "Interlock the units",
                            "Secure the connections",
                            "Shape into final star form"
                        ]
                    }
                }
            },
            "advanced": {
                "title": "Advanced Level",
                "designs": {
                    "dragon": {
                        "name": "Dragon",
                        "time": "60 minutes",
                        "completed": False,
                        "steps": [
                            "Create a bird base",
                            "Form the head and neck",
                            "Create the tail section",
                            "Form the legs and claws",
                            "Shape the wings",
                            "Add final details and adjustments"
                        ]
                    },
                    "lotus": {
                        "name": "Complex Lotus",
                        "time": "45 minutes",
                        "completed": False,
                        "steps": [
                            "Start with a square paper",
                            "Create multiple petal layers",
                            "Form the base and center",
                            "Shape individual petals",
                            "Assemble all layers",
                            "Add final touches"
                        ]
                    },
                    "unicorn": {
                        "name": "Unicorn",
                        "time": "75 minutes",
                        "completed": False,
                        "steps": [
                            "Create a complex base",
                            "Form the body structure",
                            "Create the head and horn",
                            "Shape the legs and hooves",
                            "Form the mane and tail",
                            "Add final details"
                        ]
                    }
                }
            }
        }
        
        self.create_gui()
        
    def create_gui(self):
        
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(expand=True, fill='both', padx=10, pady=5)
        
       
        self.notebook = ttk.Notebook(self.main_container)
        self.notebook.pack(expand=True, fill='both')
        
    
        self.designs_frame = ttk.Frame(self.notebook)
        self.instructions_frame = ttk.Frame(self.notebook)
        self.progress_frame = ttk.Frame(self.notebook)
        
        self.notebook.add(self.designs_frame, text='Origami Designs')
        self.notebook.add(self.instructions_frame, text='Instructions')
        self.notebook.add(self.progress_frame, text='Progress Tracker')
        
        self.setup_designs_tab()
        self.setup_instructions_tab()
        self.setup_progress_tab()
    
    def setup_designs_tab(self):
        
        for difficulty in self.origami_designs:
            frame = ttk.LabelFrame(self.designs_frame, text=self.origami_designs[difficulty]["title"])
            frame.pack(fill='x', padx=5, pady=5)
            
         
            for design_id, design in self.origami_designs[difficulty]["designs"].items():
                btn = ttk.Button(frame, text=f"{design['name']} ({design['time']})",
                               command=lambda d=design_id, diff=difficulty: self.show_design(d, diff))
                btn.pack(side='left', padx=5, pady=5)
    
    def setup_instructions_tab(self):
        self.instruction_text = tk.Text(self.instructions_frame, height=20, width=60)
        self.instruction_text.pack(pady=10, padx=10)
        
        self.complete_btn = ttk.Button(self.instructions_frame, text="Mark as Complete",
                                     command=self.mark_complete)
        self.complete_btn.pack(pady=5)
        self.complete_btn.config(state='disabled')
    
    def setup_progress_tab(self):
        self.progress_tree = ttk.Treeview(self.progress_frame, columns=('Level', 'Design', 'Status', 'Completed'),
                                        show='headings')
        self.progress_tree.heading('Level', text='Difficulty Level')
        self.progress_tree.heading('Design', text='Design Name')
        self.progress_tree.heading('Status', text='Status')
        self.progress_tree.heading('Completed', text='Completion Date')
        self.progress_tree.pack(pady=10, padx=10, fill='both', expand=True)
        
        self.update_progress_display()
    
    def show_design(self, design_id, difficulty):
        self.current_design = (difficulty, design_id)
        design = self.origami_designs[difficulty]["designs"][design_id]
        
        self.instruction_text.delete(1.0, tk.END)
        self.instruction_text.insert(tk.END, f"Design: {design['name']}\n")
        self.instruction_text.insert(tk.END, f"Difficulty: {self.origami_designs[difficulty]['title']}\n")
        self.instruction_text.insert(tk.END, f"Estimated Time: {design['time']}\n\n")
        self.instruction_text.insert(tk.END, "Steps:\n")
        for i, step in enumerate(design['steps'], 1):
            self.instruction_text.insert(tk.END, f"{i}. {step}\n")
        
        self.complete_btn.config(state='normal')
        self.notebook.select(1)  
    
    def mark_complete(self):
        if self.current_design:
            difficulty, design_id = self.current_design
            design = self.origami_designs[difficulty]["designs"][design_id]
            
            if not design["completed"]:
                design["completed"] = True
                self.progress_data.append({
                    "difficulty": difficulty,
                    "design": design["name"],
                    "completed_date": datetime.now().strftime("%Y-%m-%d %H:%M")
                })
                self.save_progress()
                self.update_progress_display()
                messagebox.showinfo("Success", f"Congratulations! You've completed the {design['name']}!")
                self.complete_btn.config(state='disabled')
    
    def update_progress_display(self):
      
        for item in self.progress_tree.get_children():
            self.progress_tree.delete(item)
       
        for difficulty in self.origami_designs:
            for design_id, design in self.origami_designs[difficulty]["designs"].items():
                completion_date = ""
                status = "Not Started"
            
                for progress in self.progress_data:
                    if progress["design"] == design["name"]:
                        status = "Completed"
                        completion_date = progress["completed_date"]
                        break
                
                self.progress_tree.insert('', 'end', values=(
                    self.origami_designs[difficulty]["title"],
                    design["name"],
                    status,
                    completion_date
                ))
    
    def load_progress(self):
        try:
            with open("origami_progress.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def save_progress(self):
        with open("origami_progress.json", "w") as f:
            json.dump(self.progress_data, f)

if __name__ == "__main__":
    root = tk.Tk()
    app = OrigamiApp(root)
    root.mainloop()
