import mysql.connector
from datetime import date
from tabulate import tabulate

# Connect to MySQL Database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="yourpassword",
    database="attendance_db"
)

def show_attendance():
    cursor = conn.cursor()
    sql = "SELECT student, date, status FROM attendance"
    cursor.execute(sql)
    result = cursor.fetchall()
    print(tabulate(result, headers=["Student", "Date", "Status"]))

def mark_attendance(name, status):
    cursor = conn.cursor()
    today = date.today().strftime("%Y-%m-%d")
    sql = "INSERT INTO attendance (student, date, status) VALUES (%s, %s, %s)"
    cursor.execute(sql, (name, today, status))
    conn.commit()

# Command-line interface for attendance
while True:
    print("
1. Take Attendance")
    print("2. Show Database")
    print("3. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        students = ["Adhvait", "Vikash", "Pratik", "Aditya", "Krishna"]
        for student in students:
            status = input(f"Is {student} Present? (Y/N): ").strip().lower()
            mark_attendance(student, "Present" if status == "y" else "Absent")
    elif choice == "2":
        show_attendance()
    elif choice == "3":
        conn.close()
        break
    else:
        print("Invalid choice, try again.")
