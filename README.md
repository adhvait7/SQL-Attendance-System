# Digitalized Student Attendance System

## Overview
This project is a **Python-based student attendance system** that allows marking attendance using **Tkinter (GUI)** and **MySQL database**.

## Features
✅ **Automated Attendance Tracking** (via GUI or CLI)  
✅ **MySQL Database Integration** (stores attendance records)  
✅ **User-Friendly Interface** (Tkinter-based UI)  
✅ **Command-Line Version** (alternative way to take attendance)  

## Setup

### 1. Install Dependencies
```
pip install mysql-connector-python tabulate
```

### 2. Setup MySQL Database
Run the following SQL commands to create the database:
```sql
CREATE DATABASE attendance_db;
USE attendance_db;
CREATE TABLE attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student VARCHAR(50),
    date DATE,
    status VARCHAR(10)
);
```

### 3. Run the Application
- **For GUI version**: Run `src/frontend.py`  
- **For CLI version**: Run `src/backend.py`  

## Contributing
Feel free to modify and improve the project! 🚀
