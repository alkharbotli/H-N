import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Modern Color Scheme
BG_COLOR = "#f5f7fa"
ENTRY_COLOR = "#ffffff"
TEXT_COLOR = "#2d3436"
ACCENT_COLOR = "#6c5ce7"
ERROR_COLOR = "#ff7675"
SUCCESS_COLOR = "#00b894"
FONT_LABEL = ("Roboto", 10, "bold")
FONT_ENTRY = ("Roboto", 10)
FONT_RESULT = ("Roboto", 9)

class GradeCalculator:
    def __init__(self, root):
        self.root = root
        self.setup_ui()
        self.setup_bindings()
        
    def setup_ui(self):
        self.root.title("Grade Target Calculator")
        self.root.geometry("550x800")
        self.root.config(bg=BG_COLOR)
        self.root.resizable(False, False)
        
        style = ttk.Style()
        style.configure("Rounded.TFrame", background=BG_COLOR)
        style.configure("Rounded.TEntry", 
                       foreground=TEXT_COLOR,
                       fieldbackground=ENTRY_COLOR,
                       relief="flat",
                       borderwidth=5,
                       padding=5,
                       font=FONT_ENTRY)

        main_frame = ttk.Frame(self.root, style="Rounded.TFrame")
        main_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        self.create_label(main_frame, "Target GPA (0-100):")
        self.entry_target = self.create_entry(main_frame)
        
        self.create_label(main_frame, "Baccalaureate Grade (225-240):")
        self.entry_baccalaureate = self.create_entry(main_frame)
        
        self.create_label(main_frame, "First Term Grades:", pady=10)
        
        self.subject_entries = []
        for i in range(5):
            self.create_label(main_frame, f"Subject {i+1}:", pady=2)
            entry = self.create_entry(main_frame)
            self.subject_entries.append(entry)
        
        self.create_label(main_frame, "First Term Average:", pady=10)
        self.entry_first_term = self.create_entry(main_frame, state="normal")
        
        self.result_text = tk.Text(
            main_frame,
            height=8,
            width=50,
            wrap=tk.WORD,
            font=FONT_RESULT,
            state="disabled",
            bg=ENTRY_COLOR,
            fg=TEXT_COLOR,
            relief="flat",
            bd=0,
            padx=10,
            pady=10,
            highlightthickness=1,
            highlightbackground="#dfe6e9"
        )
        self.result_text.pack(pady=20, fill="x")

        # رسالة الشكر والمؤلف
        footer_frame = tk.Frame(self.root, bg=BG_COLOR)
        footer_frame.pack(side="bottom", fill="x", pady=(5, 0))

        footer_label = tk.Label(
            footer_frame,
            text="Thank you for using this app\nCreated by Nakour",
            font=("Roboto", 9),
            bg=BG_COLOR,
            fg="#636e72",
            justify="center"
        )
        footer_label.pack(anchor="center")
        
        self.status_var = tk.StringVar()
        self.status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            bg=ACCENT_COLOR,
            fg="white",
            anchor="w",
            font=("Roboto", 9)
        )
        self.status_bar.pack(fill="x", side="bottom")
        self.update_status("Ready")
    
    def create_label(self, parent, text, pady=5):
        label = tk.Label(
            parent,
            text=text,
            font=FONT_LABEL,
            bg=BG_COLOR,
            fg=TEXT_COLOR
        )
        label.pack(pady=pady, anchor="w")
        return label
    
    def create_entry(self, parent, state="normal"):
        entry = ttk.Entry(
            parent,
            style="Rounded.TEntry",
            font=FONT_ENTRY,
            justify="center",
            state=state
        )
        entry.pack(pady=5, ipady=5, fill="x")
        return entry
    
    def setup_bindings(self):
        for entry in self.subject_entries:
            entry.bind("<FocusIn>", self.lock_first_term_entry)

        all_entries = [self.entry_target, self.entry_baccalaureate, self.entry_first_term] + self.subject_entries
        for entry in all_entries:
            entry.bind("<KeyRelease>", self.calculate_required_grade)
    
    def lock_first_term_entry(self, event):
        for entry in self.subject_entries:
            if entry.get().strip():
                self.entry_first_term.config(state="disabled")
                self.update_status("Entering Subjects - First Term Average locked")
                return

        all_empty = all(entry.get().strip() == "" for entry in self.subject_entries)
        if all_empty:
            self.entry_first_term.config(state="normal")
            self.update_status("You can now modify the First Term Average.")

    def update_status(self, message):
        self.status_var.set(f"{message}")
    
    def validate_entry(self, entry, min_val, max_val):
        try:
            value = float(entry.get())
            if value < min_val or value > max_val:
                entry.config(foreground=ERROR_COLOR)
                return None
            else:
                entry.config(foreground=TEXT_COLOR)
                return value
        except:
            if entry.get().strip() == "":
                entry.config(foreground=TEXT_COLOR)
            else:
                entry.config(foreground=ERROR_COLOR)
            return None
    
    def calculate_required_grade(self, event=None):
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        
        final_target = self.validate_entry(self.entry_target, 0, 100)
        baccalaureate_grade = self.validate_entry(self.entry_baccalaureate, 225, 240)
        
        if final_target is None or baccalaureate_grade is None:
            self.result_text.insert(tk.END, "Please enter valid values in all fields!")
            self.result_text.config(state="disabled")
            return

        subject_grades = []
        subjects_filled = 0
        for entry in self.subject_entries:
            val = self.validate_entry(entry, 0, 100)
            if val is not None:
                subject_grades.append(val)
                subjects_filled += 1
            else:
                subject_grades.append(0)
        
        if subjects_filled == 5:
            first_term_avg = sum(subject_grades) / 5
            self.entry_first_term.config(state="normal")
            self.entry_first_term.delete(0, tk.END)
            self.entry_first_term.insert(0, f"{first_term_avg:.2f}")
            self.entry_first_term.config(state="readonly")
            self.update_status("First term average calculated from subjects")
        else:
            first_term_avg = self.validate_entry(self.entry_first_term, 0, 100)
            if first_term_avg is None:
                self.result_text.insert(tk.END, "Please enter all subject grades OR first term average!")
                self.result_text.config(state="disabled")
                return
        
        bac_percent = (baccalaureate_grade / 240) * 100
        required_grade_second = max(0, (final_target - (bac_percent * 0.40) - (first_term_avg * 0.30)) / 0.30)

        result = f"Required 2nd Term GPA: {required_grade_second:.2f}\n\n"
        result += self.get_motivational_message(required_grade_second, final_target)
        
        self.result_text.insert(tk.END, result)
        self.result_text.config(state="disabled")
    
    def get_motivational_message(self, required_grade, target):
        if required_grade > 100:
            return "Impossible target! Please adjust your expectations."
        elif required_grade > 90:
            return "Challenging but achievable! Give it your best shot!"
        elif required_grade >= 75:
            return "Doable with consistent effort. Stay focused!"
        else:
            if target >= 95:
                return "You're already excellent! Just maintain your performance."
            else:
                return "You can aim higher! This target is too easy."

if __name__ == "__main__":
    root = tk.Tk()
    app = GradeCalculator(root)
    root.mainloop()
