import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="saurabh",
    database="mcq_quiz_app"
)
db_cursor = db.cursor()

class HODRegistrationWindow:
    def __init__(self, root, auth_window):
        self.root = root
        self.root.title("HOD Registration")

        # Maximize the window to full screen
        self.root.state('zoomed')

        self.auth_window = auth_window

        # Set background color
        self.root.config(bg="#3498db")

        self.frame = tk.Frame(self.root, bg="#3498db")
        self.frame.pack(expand=True)

        # Registration Form
        title_label = tk.Label(self.frame, text="HOD Registration", font=("Helvetica", 20, "bold"), bg="#3498db", fg="white")
        title_label.pack(pady=20)

        # Registration Form
        self.name_label = tk.Label(self.frame, text="Name:", font=("Helvetica", 12), bg="#3498db", fg="white")
        self.name_label.pack(pady=10)
        self.name_entry = tk.Entry(self.frame, font=("Helvetica", 12))
        self.name_entry.pack(pady=5)

        self.mob_label = tk.Label(self.frame, text="Mobile:", font=("Helvetica", 12), bg="#3498db", fg="white")
        self.mob_label.pack(pady=10)
        self.mob_entry = tk.Entry(self.frame, font=("Helvetica", 12))
        self.mob_entry.pack(pady=5)

        self.email_label = tk.Label(self.frame, text="Email ID:", font=("Helvetica", 12), bg="#3498db", fg="white")
        self.email_label.pack(pady=10)
        self.email_entry = tk.Entry(self.frame, font=("Helvetica", 12))
        self.email_entry.pack(pady=5)

        self.college_label = tk.Label(self.frame, text="College Name:", font=("Helvetica", 12), bg="#3498db", fg="white")
        self.college_label.pack(pady=10)
        self.college_entry = tk.Entry(self.frame, font=("Helvetica", 12))
        self.college_entry.pack(pady=5)

        self.username_label = tk.Label(self.frame, text="Username:", font=("Helvetica", 12), bg="#3498db", fg="white")
        self.username_label.pack(pady=10)
        self.username_entry = tk.Entry(self.frame, font=("Helvetica", 12))
        self.username_entry.pack(pady=5)

        self.password_label = tk.Label(self.frame, text="Password:", font=("Helvetica", 12), bg="#3498db", fg="white")
        self.password_label.pack(pady=10)
        self.password_entry = tk.Entry(self.frame, show="*", font=("Helvetica", 12))
        self.password_entry.pack(pady=5)

        self.register_button = tk.Button(self.frame, text="Register", command=self.register, font=("Helvetica", 14, "bold"), bg="#2ecc71", fg="white")
        self.register_button.pack(pady=20)

    def register(self):
        # Get values from the registration form
        name = self.name_entry.get()
        mob = self.mob_entry.get()
        email = self.email_entry.get()
        college = self.college_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Insert HOD details into the database
        query = "INSERT INTO hods (name, mob, email, college, username, password) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (name, mob, email, college, username, password)

        try:
            db_cursor.execute(query, values)
            db.commit()
            messagebox.showinfo("Registration Successful", "HOD registered successfully!")
            self.root.withdraw()
            self.auth_window.show_login_window()  
        except mysql.connector.Error as err:
            messagebox.showerror("Registration Failed", f"Error: {err}")

