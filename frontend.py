import mysql.connector
from tabulate import tabulate
from tkinter import *
from datetime import date

# Connect to MySQL Database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="yourpassword",
    database="attendance_db"
)

# Function to show attendance records
def show_attendance():
    cursor = conn.cursor()
    sql = "SELECT student, date FROM attendance"
    cursor.execute(sql)
    result = cursor.fetchall()
    print(tabulate(result, headers=["Student", "Date"]))

# Function to mark attendance
def mark_attendance(name, status):
    cursor = conn.cursor()
    today = date.today().strftime("%Y-%m-%d")
    sql = f"INSERT INTO attendance (student, date, status) VALUES (%s, %s, %s)"
    cursor.execute(sql, (name, today, status))
    conn.commit()

# Tkinter GUI for Attendance Marking
root = Tk()
root.title("Student Attendance System")
root.geometry("300x200")

students = ["Adhvait", "Vikash", "Pratik", "Aditya", "Krishna"]
index = 0

# Function to handle present button
def present():
    global index
    if index < len(students):
        mark_attendance(students[index], "Present")
        index += 1
        update_label()

# Function to handle absent button
def absent():
    global index
    if index < len(students):
        mark_attendance(students[index], "Absent")
        index += 1
        update_label()

# Function to update student label
def update_label():
    if index < len(students):
        student_label.config(text=students[index])
    else:
        student_label.config(text="Attendance Complete")

# UI Elements
student_label = Label(root, text=students[0], font=("Calibri", 15))
student_label.pack()

present_button = Button(root, text="Present", bg="green", command=present)
present_button.pack(side=LEFT, padx=20)

absent_button = Button(root, text="Absent", bg="red", command=absent)
absent_button.pack(side=RIGHT, padx=20)

root.mainloop()

# Close connection
conn.close()
