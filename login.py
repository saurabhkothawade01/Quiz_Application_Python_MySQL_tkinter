import tkinter as tk
from tkinter import messagebox
import mysql.connector
from teachers import TeacherInterface

# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="saurabh",
    database="mcq_quiz_app"
)
cursor = db.cursor()

# Authentication Window
class AuthWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("MCQ Quiz App - Login")

        # Maximize the window to full screen
        self.root.state('zoomed')

        # Set background color
        self.root.config(bg="#3498db")

        # Create a frame to contain the widgets
        self.frame = tk.Frame(self.root, bg="#3498db")
        self.frame.pack(expand=True)

        # Set title label
        title_label = tk.Label(self.frame, text="MCQ Quiz App", font=("Helvetica", 20, "bold"), bg="#3498db", fg="white")
        title_label.pack(pady=20)

        # Username Label and Entry
        self.username_label = tk.Label(self.frame, text="Username:", font=("Helvetica", 12), bg="#3498db", fg="white")
        self.username_label.pack(pady=10)

        self.username_entry = tk.Entry(self.frame, font=("Helvetica", 12))
        self.username_entry.pack(pady=5)

        # Password Label and Entry
        self.password_label = tk.Label(self.frame, text="Password:", font=("Helvetica", 12), bg="#3498db", fg="white")
        self.password_label.pack(pady=10)

        self.password_entry = tk.Entry(self.frame, show="*", font=("Helvetica", 12))
        self.password_entry.pack(pady=5)

        # Login Button
        self.login_button = tk.Button(self.frame, text="Login", command=self.login, font=("Helvetica", 14, "bold"), bg="#2ecc71", fg="white")
        self.login_button.pack(pady=20)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Check authentication in the database
        query = "SELECT * FROM teachers WHERE username=%s AND password=%s"
        cursor.execute(query, (username, password))
        teacher = cursor.fetchone()

        if teacher:
            # Successful login for teacher
            messagebox.showinfo("Login Successful", "Welcome, Teacher!")

            # Destroy the authentication window
            self.root.destroy()

            # Create and run the TeacherInterface window
            root_teacher_interface = tk.Tk()
            teacher_interface = TeacherInterface(root_teacher_interface, teacher[0])
            root_teacher_interface.mainloop()
        else:
            # Check student authentication
            query = "SELECT * FROM students WHERE username=%s AND password=%s"
            cursor.execute(query, (username, password))
            student = cursor.fetchone()

            if student:
                # Successful login for student
                messagebox.showinfo("Login Successful", "Welcome, Student!")
                # Implement code to open student interface
            else:
                # Failed login
                messagebox.showerror("Login Failed", "Invalid username or password")

# Create and run the authentication window
root = tk.Tk()
auth_window = AuthWindow(root)
root.mainloop()
