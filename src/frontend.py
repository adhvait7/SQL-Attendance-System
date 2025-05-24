"""
Attendance Management System (GUI)
Tkinter app to mark attendance, show records, reset data, and set custom date.
Students list loaded from students.csv
"""

import csv
from pymongo import MongoClient
from datetime import date
from tkinter import *
from tkinter import messagebox, simpledialog
from tabulate import tabulate

# MongoDB Atlas connection URI (password URL-encoded)
MONGO_URI = "mongodb+srv://adhvait123:Attendance%21%40%23%24@attendance-system.qffduxu.mongodb.net/?retryWrites=true&w=majority&appName=Attendance-System"

# Initialize MongoDB client and database/collection
client = MongoClient(MONGO_URI)
db = client["attendance_db"]
attendance_collection = db["attendance"]

# Load students from CSV file
def load_students_from_csv(filename="students.csv"):
    students = []
    try:
        with open(filename, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row:  # avoid empty lines
                    students.append(row[0].strip())
    except FileNotFoundError:
        print(f"Error: {filename} not found. Please create the file with student names.")
    return students

students = load_students_from_csv()
if not students:
    print("Student list is empty. Please check your CSV file.")

index = 0  # Tracks which student is currently being marked
selected_date = date.today().strftime("%Y-%m-%d")  # Default to today

def mark_attendance(name: str, status: str, attendance_date: str):
    """Insert an attendance record into MongoDB."""
    record = {"student": name, "date": attendance_date, "status": status}
    attendance_collection.insert_one(record)

def present():
    global index
    if index < len(students):
        mark_attendance(students[index], "Present", selected_date)
        index += 1
        update_label()

def absent():
    global index
    if index < len(students):
        mark_attendance(students[index], "Absent", selected_date)
        index += 1
        update_label()

def update_label():
    """Update the UI label with the current student or completion message."""
    if index < len(students):
        student_label.config(text=f"Mark attendance for:\n{students[index]}\n(Date: {selected_date})")
    else:
        student_label.config(text="✅ Attendance Complete!")
        present_button.config(state=DISABLED)
        absent_button.config(state=DISABLED)
        messagebox.showinfo("Done", "All attendance marked successfully!")

def show_attendance():
    """Fetch all attendance records and display them in a popup."""
    records = list(attendance_collection.find({}, {"_id": 0, "student": 1, "date": 1, "status": 1}))
    if not records:
        messagebox.showinfo("Attendance Records", "No attendance records found.")
        return

    # Format records using tabulate for pretty text table
    table_str = tabulate(records, headers="keys", tablefmt="grid")

    # Show records in a scrollable text popup
    popup = Toplevel(root)
    popup.title("Attendance Records")
    popup.geometry("500x400")

    text = Text(popup, wrap=NONE, font=("Consolas", 10))
    text.insert(END, table_str)
    text.config(state=DISABLED)  # read-only
    text.pack(fill=BOTH, expand=True)

    # Add scrollbar
    scrollbar_y = Scrollbar(popup, orient=VERTICAL, command=text.yview)
    text.configure(yscrollcommand=scrollbar_y.set)
    scrollbar_y.pack(side=RIGHT, fill=Y)

def reset_records():
    """Confirm and delete all attendance records."""
    if messagebox.askyesno("Reset Records", "Are you sure you want to delete ALL attendance records? This cannot be undone."):
        attendance_collection.delete_many({})
        messagebox.showinfo("Reset Records", "All attendance records have been deleted.")
        reset_app()

def reset_app():
    """Reset GUI to initial state."""
    global index
    index = 0
    present_button.config(state=NORMAL)
    absent_button.config(state=NORMAL)
    update_label()

def set_date():
    """Prompt user to enter a date in YYYY-MM-DD format."""
    global selected_date
    input_date = simpledialog.askstring("Set Date", "Enter date (YYYY-MM-DD):", parent=root)
    if input_date:
        # Basic validation for format YYYY-MM-DD
        import re
        if re.match(r"^\d{4}-\d{2}-\d{2}$", input_date):
            selected_date = input_date
            update_label()
            messagebox.showinfo("Date Set", f"Attendance date set to {selected_date}")
        else:
            messagebox.showerror("Invalid Date", "Date must be in YYYY-MM-DD format.")

# Dark mode and light mode colors
LIGHT_BG = "#f0f4f8"
LIGHT_FG = "#333"
DARK_BG = "#2e2e2e"
DARK_FG = "#f0f0f0"

current_theme = "light"

def apply_theme(theme):
    global current_theme
    current_theme = theme
    bg = LIGHT_BG if theme == "light" else DARK_BG
    fg = LIGHT_FG if theme == "light" else DARK_FG

    root.configure(bg=bg)
    title_label.config(bg=bg, fg=fg)
    student_label.config(bg=bg, fg=fg)
    button_frame.config(bg=bg)
    options_frame.config(bg=bg)
    footer_label.config(bg=bg, fg=fg)

    # Buttons colors for light/dark modes
    def style_button(btn, bg_color, fg_color):
        btn.config(bg=bg_color, fg=fg_color, activebackground=bg_color)

    style_button(present_button, "#4CAF50" if theme == "light" else "#357a38", "white")
    style_button(absent_button, "#F44336" if theme == "light" else "#a93226", "white")
    style_button(show_button, "#2196F3" if theme == "light" else "#145a86", "white")
    style_button(reset_button, "#9C27B0" if theme == "light" else "#6a1b74", "white")
    style_button(date_button, "#FF9800" if theme == "light" else "#b26a00", "white")
    style_button(toggle_theme_button, "#607D8B" if theme == "light" else "#455a64", "white")

def toggle_theme():
    if current_theme == "light":
        apply_theme("dark")
    else:
        apply_theme("light")

# Setup the main Tkinter window
root = Tk()
root.title("Student Attendance System")
root.geometry("500x320")
root.resizable(False, False)
root.configure(bg=LIGHT_BG)

# Title label
title_label = Label(root, text="Attendance Marking System", font=("Segoe UI", 20, "bold"), bg=LIGHT_BG, fg=LIGHT_FG)
title_label.pack(pady=(15, 10))

# Student label
if students:
    student_label = Label(root, text=f"Mark attendance for:\n{students[0]}\n(Date: {selected_date})", font=("Segoe UI", 16), bg=LIGHT_BG, fg="#444")
else:
    student_label = Label(root, text="No students loaded. Check students.csv", font=("Segoe UI", 16), bg=LIGHT_BG, fg="red")
student_label.pack(pady=15)

# Attendance buttons frame
button_frame = Frame(root, bg=LIGHT_BG)
button_frame.pack(pady=10)

present_button = Button(
    button_frame, text="Present", width=14, bg="#4CAF50", fg="white",
    font=("Segoe UI", 12, "bold"), activebackground="#45a049", cursor="hand2",
    relief=FLAT, command=present
)
present_button.pack(side=LEFT, padx=20)

absent_button = Button(
    button_frame, text="Absent", width=14, bg="#F44336", fg="white",
    font=("Segoe UI", 12, "bold"), activebackground="#e53935", cursor="hand2",
    relief=FLAT, command=absent
)
absent_button.pack(side=RIGHT, padx=20)

# Additional options frame
options_frame = Frame(root, bg=LIGHT_BG)
options_frame.pack(pady=20)

show_button = Button(
    options_frame, text="Show Attendance", width=18, bg="#2196F3", fg="white",
    font=("Segoe UI", 11, "bold"), activebackground="#1976D2", cursor="hand2",
    relief=FLAT, command=show_attendance
)
show_button.pack(side=LEFT, padx=10)

reset_button = Button(
    options_frame, text="Reset Records", width=18, bg="#9C27B0", fg="white",
    font=("Segoe UI", 11, "bold"), activebackground="#7B1FA2", cursor="hand2",
    relief=FLAT, command=reset_records
)
reset_button.pack(side=LEFT, padx=10)

date_button = Button(
    options_frame, text="Set Date", width=12, bg="#FF9800", fg="white",
    font=("Segoe UI", 11, "bold"), activebackground="#F57C00", cursor="hand2",
    relief=FLAT, command=set_date
)
date_button.pack(side=LEFT, padx=10)

# Dark mode toggle button
toggle_theme_button = Button(
    options_frame, text="Toggle Dark Mode", width=14, bg="#607D8B", fg="white",
    font=("Segoe UI", 11, "bold"), activebackground="#455a64", cursor="hand2",
    relief=FLAT, command=toggle_theme
)
toggle_theme_button.pack(side=LEFT, padx=10)

# Footer
footer_label = Label(root, text="© 2025 Attendance System", font=("Segoe UI", 9), bg=LIGHT_BG, fg="#999")
footer_label.pack(side=BOTTOM, pady=10)

# Initialize theme
apply_theme("light")

root.mainloop()

# Close MongoDB client connection on GUI exit
client.close()
