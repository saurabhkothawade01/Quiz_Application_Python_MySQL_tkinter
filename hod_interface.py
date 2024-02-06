import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import mysql.connector
import random
import string

# Add this code at the beginning to connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="saurabh",
    database="mcq_quiz_app"
)
cursor = db.cursor()

class HODInterface:
    def __init__(self, root, hod_id):
        self.root = root
        self.root.title("MCQ Quiz App - HOD Interface")
        
        # Maximize the window to full screen
        self.root.state('zoomed')

        self.hod_id = hod_id

        # Style for tabs
        style = ttk.Style()
        style.configure("TNotebook", background="#ecf0f1")
        style.configure("TNotebook.Tab", background="#3498db", foreground="black", padding=[10, 5])

        # Create a notebook (tabbed interface)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Manage Teachers Tab
        self.manage_teachers_tab = tk.Frame(self.notebook)
        self.notebook.add(self.manage_teachers_tab, text="Manage Teachers")
        self.setup_manage_teachers_tab(hod_id)

        # Results Tab
        self.results_tab = tk.Frame(self.notebook)
        self.notebook.add(self.results_tab, text="Results")
        self.setup_results_tab()

        # Profile Tab
        self.profile_tab = tk.Frame(self.notebook)
        self.notebook.add(self.profile_tab, text="Profile")
        self.setup_profile_tab()

    def setup_manage_teachers_tab(self, hod_id):
        # Create two frames to divide the "Manage Teachers" tab into two sections
        left_frame = tk.Frame(self.manage_teachers_tab)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)

        right_frame = tk.Frame(self.manage_teachers_tab)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Left Section (Buttons)
        add_teacher_button = tk.Button(left_frame, text="Add Teacher", command=self.add_teacher, font=("Helvetica", 14), bg="#2ecc71", fg="white")
        add_teacher_button.pack(pady=20)

        delete_teacher_button = tk.Button(left_frame, text="Delete Teacher", command=self.delete_teacher, font=("Helvetica", 14), bg="#e74c3c", fg="white")
        delete_teacher_button.pack(pady=20)

        logout_button = tk.Button(left_frame, text="Logout", command=self.logout, font=("Helvetica", 14), bg="#e67e22", fg="white")
        logout_button.pack(pady=20)

        # Right Section (Display Teachers and Subjects)
        self.setup_teachers_and_subjects_display(right_frame, hod_id)

    def setup_teachers_and_subjects_display(self, parent_frame, hod_id):
        # Create a Treeview widget for displaying teachers and their subjects
        self.teachers_subjects_tree = ttk.Treeview(parent_frame, columns=("Teacher Name", "Subject"), show="headings")

        # Define column headings
        self.teachers_subjects_tree.heading("Teacher Name", text="Teacher Name")
        self.teachers_subjects_tree.heading("Subject", text="Subject")

        # Add a vertical scrollbar
        scroll_y = ttk.Scrollbar(parent_frame, orient=tk.VERTICAL, command=self.teachers_subjects_tree.yview)
        self.teachers_subjects_tree.configure(yscrollcommand=scroll_y.set)

        # Pack the Treeview and scrollbar
        self.teachers_subjects_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        # Populate the Treeview with teachers and subjects data
        self.populate_teachers_and_subjects_display(hod_id)

    def populate_teachers_and_subjects_display(self, hod_id):
        # Fetch teachers and their subjects from the database
        query = "SELECT teachers.username, subjects.name " \
                "FROM teachers " \
                "JOIN hod_subjects ON teachers.id = hod_subjects.teacher_id " \
                "JOIN subjects ON hod_subjects.subject_id = subjects.id " \
                "WHERE hod_subjects.hod_id = %s"
        cursor.execute(query, (hod_id,))
        data = cursor.fetchall()

        # Clear existing data in the Treeview
        self.teachers_subjects_tree.delete(*self.teachers_subjects_tree.get_children())

        # Insert data into the Treeview
        for teacher_subject in data:
            self.teachers_subjects_tree.insert("", tk.END, values=teacher_subject)

    def add_teacher(self):
        # Create a new window for adding a teacher
        add_teacher_window = tk.Toplevel(self.root)
        add_teacher_window.title("Add Teacher")

        # Create and place labels and entry widgets for username and subject
        username_label = tk.Label(add_teacher_window, text="Username:")
        username_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        username_entry = tk.Entry(add_teacher_window)
        username_entry.grid(row=0, column=1, padx=10, pady=10)

        subject_label = tk.Label(add_teacher_window, text="Subject:")
        subject_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        subject_entry = tk.Entry(add_teacher_window)
        subject_entry.grid(row=1, column=1, padx=10, pady=10)

        # Function to generate a random password
        def generate_random_password():
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
            password_entry.delete(0, tk.END)
            password_entry.insert(0, password)

        # Create and place labels, entry widget, and buttons for the password
        password_label = tk.Label(add_teacher_window, text="Password:")
        password_label.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        password_entry = tk.Entry(add_teacher_window)
        password_entry.grid(row=2, column=1, padx=10, pady=10)
        
        generate_password_button = tk.Button(add_teacher_window, text="Generate Password", command=generate_random_password)
        generate_password_button.grid(row=2, column=2, padx=10, pady=10)

        # Function to add the teacher to the database
        def add_teacher_to_database():
            new_username = username_entry.get()
            new_subject = subject_entry.get()
            new_password = password_entry.get()

            # Check if any field is empty
            if not new_username or not new_subject or not new_password:
                messagebox.showerror("Error", "All fields are compulsory.")
                add_teacher_window.destroy()
                return

            # Check if the teacher already exists for that HOD
            query_check_teacher = "SELECT COUNT(*) FROM teachers WHERE username = %s"
            cursor.execute(query_check_teacher, (new_username,))
            teacher_count = cursor.fetchone()[0]
            if teacher_count > 0:
                messagebox.showerror("Error", f"Teacher '{new_username}' already exists for this HOD.")
                add_teacher_window.destroy()
                return

            # Check if the subject already exists in the subjects table
            query_check_subject = "SELECT COUNT(*) FROM subjects WHERE name = %s"
            cursor.execute(query_check_subject, (new_subject,))
            subject_count = cursor.fetchone()[0]
            if subject_count > 0:
                messagebox.showerror("Error", f"Subject '{new_subject}' already exists.")
                add_teacher_window.destroy()
                return

            # Insert the new subject into the subjects table
            query_insert_subject = "INSERT INTO subjects (name) VALUES (%s)"
            cursor.execute(query_insert_subject, (new_subject,))
            db.commit()

            # Get the ID of the subject from the subjects table
            cursor.execute("SELECT LAST_INSERT_ID()")
            subject_id = cursor.fetchone()[0]

            # Insert the new teacher into the database
            query_insert_teacher = "INSERT INTO teachers (username, password) VALUES (%s, %s)"
            cursor.execute(query_insert_teacher, (new_username, new_password))
            db.commit()

            # Get the ID of the newly inserted teacher
            teacher_id = cursor.lastrowid

            # Add the subject assignment to hod_subjects
            query_assign_subject = "INSERT INTO hod_subjects (hod_id, teacher_id, subject_id) VALUES (%s, %s, %s)"
            cursor.execute(query_assign_subject, (self.hod_id, teacher_id, subject_id))
            db.commit()

            # Refresh the display
            self.populate_teachers_and_subjects_display(self.hod_id)

            # Close the add teacher window
            add_teacher_window.destroy()

            # Show a success message
            messagebox.showinfo("Success", "Teacher added successfully!")

        # Create and place "Add" and "Cancel" buttons
        add_button = tk.Button(add_teacher_window, text="Add", command=add_teacher_to_database, bg="#2ecc71", fg="white")
        add_button.grid(row=3, column=0, padx=10, pady=10)

        cancel_button = tk.Button(add_teacher_window, text="Cancel", command=add_teacher_window.destroy, bg="#e74c3c", fg="white")
        cancel_button.grid(row=3, column=1, padx=10, pady=10)

    def delete_teacher(self):
        # Implement the logic for deleting a teacher
        # You can create a confirmation dialog and proceed with deletion
        pass

    def subject_assign(self):
        # Implement the logic for assigning a subject to a teacher
        # You can create a new window or use an existing one
        pass

    def logout(self):
        # Destroy the current HOD interface window
        self.root.destroy()

         # Import AuthWindow class
        from login import AuthWindow
        # Open the login window again
        root = tk.Tk()
        auth_window = AuthWindow(root)
        root.mainloop()

    def setup_results_tab(self):
        # Add code for "Results" tab here
        pass

    def setup_profile_tab(self):
        # Add code for "Profile" tab here
        pass
   

# Example usage in your login.py after successful HOD login
def open_hod_interface(hod_id):
    # Create and run the HODInterface window
    root_hod_interface = tk.Tk()
    hod_interface = HODInterface(root_hod_interface, hod_id)
    root_hod_interface.mainloop()
