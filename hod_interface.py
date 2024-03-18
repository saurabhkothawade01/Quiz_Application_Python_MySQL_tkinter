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
            query_insert_teacher = "INSERT INTO teachers (username, password, hod_id) VALUES (%s, %s, %s)"
            cursor.execute(query_insert_teacher, (new_username, new_password, self.hod_id))
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
        # Check if any teacher is selected in the Treeview
        selected_item = self.teachers_subjects_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a teacher to delete.")
            return

        # Get the teacher's username and ID from the selected item
        teacher_username = self.teachers_subjects_tree.item(selected_item, "values")[0]
        teacher_id = self.get_teacher_id_by_username(teacher_username)

        # Ask for confirmation before deletion
        confirmation = messagebox.askyesno("Confirmation", f"Are you sure you want to delete teacher '{teacher_username}'?")

        if confirmation:
            try:
                # Get quizzes belonging to the teacher
                query_get_quizzes = "SELECT id FROM quizzes WHERE teacher_id = %s"
                cursor.execute(query_get_quizzes, (teacher_id,))
                quizzes = cursor.fetchall()

                # Delete results associated with each quiz
                for quiz in quizzes:
                    quiz_id = quiz[0]
                    query_delete_results = "DELETE FROM results WHERE quiz_id = %s"
                    cursor.execute(query_delete_results, (quiz_id,))
                    db.commit()

                # Delete related records from the quizzes table
                query_delete_quizzes = "DELETE FROM quizzes WHERE teacher_id = %s"
                cursor.execute(query_delete_quizzes, (teacher_id,))
                db.commit()

                # Delete related records from the hod_subjects table
                query_delete_hod_subjects = "DELETE FROM hod_subjects WHERE teacher_id = %s"
                cursor.execute(query_delete_hod_subjects, (teacher_id,))
                db.commit()

                # Delete related records from the assigned_quizzes table
                query_delete_assigned_quizzes = "DELETE FROM assigned_quizzes WHERE teacher_id = %s"
                cursor.execute(query_delete_assigned_quizzes, (teacher_id,))
                db.commit()

                # Delete the teacher from the teachers table
                query_delete_teacher = "DELETE FROM teachers WHERE username = %s AND hod_id = %s"
                cursor.execute(query_delete_teacher, (teacher_username, self.hod_id))
                db.commit()

                # Refresh the display
                self.populate_teachers_and_subjects_display(self.hod_id)

                # Show a success message
                messagebox.showinfo("Success", f"Teacher '{teacher_username}' deleted successfully.")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"An error occurred: {err}")

    def get_teacher_id_by_username(self, username):
        # Get the ID of the teacher based on the username
        query = "SELECT id FROM teachers WHERE username = %s AND hod_id = %s"
        cursor.execute(query, (username, self.hod_id))
        result = cursor.fetchone()
        if result:
            return result[0]
        return None





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
        # Create a frame for displaying teachers list and student marks
        results_frame = tk.Frame(self.results_tab)
        results_frame.pack(fill=tk.BOTH, expand=True)

        # First Section: Display list of teachers
        teachers_frame = tk.Frame(results_frame, bg="white")
        teachers_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Fetch teachers added by the HOD
        query = "SELECT id, username FROM teachers WHERE hod_id = %s"
        cursor.execute(query, (self.hod_id,))
        teachers = cursor.fetchall()

        # Create a listbox to display teachers
        teachers_listbox = tk.Listbox(teachers_frame, width=30, height=20)
        teachers_listbox.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Populate the listbox with teachers
        for teacher in teachers:
            teacher_id, teacher_name = teacher
            teachers_listbox.insert(tk.END, f"{teacher_id}: {teacher_name}")

        # Second Section: Display student marks
        marks_frame = tk.Frame(results_frame)
        marks_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        def show_teacher_quizzes(event):
            # Get the selected teacher from the listbox
            selected_teacher_index = teachers_listbox.curselection()
            if selected_teacher_index:
                selected_teacher_id = int(teachers_listbox.get(selected_teacher_index)[0].split(":")[0])

                # Fetch quizzes created by the selected teacher
                query = "SELECT id, quiz_name FROM quizzes WHERE teacher_id = %s"
                cursor.execute(query, (selected_teacher_id,))
                quizzes = cursor.fetchall()

                if not quizzes:
                    messagebox.showwarning("Warning", "No quizzes found for this teacher.")
                    return

                # Create a new window to display the list of quizzes
                quizzes_window = tk.Toplevel(self.root)
                quizzes_window.title("Quizzes")

                # Create a listbox to display quizzes
                quizzes_listbox = tk.Listbox(quizzes_window, width=50, height=20)
                quizzes_listbox.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

                # Populate the listbox with quizzes
                for quiz in quizzes:
                    quiz_id, quiz_name = quiz
                    quizzes_listbox.insert(tk.END, f"{quiz_id}: {quiz_name}")

                def show_quiz_results(event):
                    # Get the selected quiz from the listbox
                    selected_quiz_index = quizzes_listbox.curselection()
                    if selected_quiz_index:
                        selected_quiz_id = int(quizzes_listbox.get(selected_quiz_index)[0].split(":")[0])

                        # Fetch students' results associated with the selected quiz and teacher
                        query = "SELECT students.username, results.score FROM students " \
                                "INNER JOIN results ON students.id = results.student_id " \
                                "WHERE students.teacher_id = %s AND results.quiz_id = %s"
                        cursor.execute(query, (selected_teacher_id, selected_quiz_id))
                        student_results = cursor.fetchall()

                        if not student_results:
                            messagebox.showwarning("Warning", "No results found for this quiz.")
                            return

                        # Clear existing data in the Treeview
                        for child in marks_frame.winfo_children():
                            child.destroy()

                        # Create a Treeview widget to display the results in tabular format
                        results_tree = ttk.Treeview(marks_frame, columns=("Student Name", "Score"), show="headings")
                        results_tree.heading("Student Name", text="Student Name")
                        results_tree.heading("Score", text="Score")

                        # Insert the student results into the Treeview
                        for student_result in student_results:
                            results_tree.insert("", tk.END, values=student_result)

                        # Add a vertical scrollbar to the Treeview
                        scroll_y = ttk.Scrollbar(marks_frame, orient=tk.VERTICAL, command=results_tree.yview)
                        results_tree.configure(yscrollcommand=scroll_y.set)

                        # Pack the Treeview and scrollbar
                        results_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

                # Bind click event to show results for selected quiz
                quizzes_listbox.bind("<<ListboxSelect>>", show_quiz_results)

        # Bind click event to show quizzes for selected teacher
        teachers_listbox.bind("<<ListboxSelect>>", show_teacher_quizzes)



    def setup_profile_tab(self):
        # Fetch HOD details from the database
        query = "SELECT name, mob, email, college, username FROM hods WHERE id = %s"
        cursor.execute(query, (self.hod_id,))
        hod_details = cursor.fetchone()

        if hod_details:
            # Unpack HOD details
            name, mob, email, college, username = hod_details

            # Create labels and entry widgets for displaying HOD details
            name_label = tk.Label(self.profile_tab, text="Name:")
            name_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
            self.name_entry = tk.Entry(self.profile_tab)
            self.name_entry.grid(row=0, column=1, padx=10, pady=10)
            self.name_entry.insert(0, name)  # Populate name entry with current name

            mob_label = tk.Label(self.profile_tab, text="Mobile:")
            mob_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
            self.mob_entry = tk.Entry(self.profile_tab)
            self.mob_entry.grid(row=1, column=1, padx=10, pady=10)
            self.mob_entry.insert(0, mob)  # Populate mob entry with current mob

            email_label = tk.Label(self.profile_tab, text="Email:")
            email_label.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
            self.email_entry = tk.Entry(self.profile_tab)
            self.email_entry.grid(row=2, column=1, padx=10, pady=10)
            self.email_entry.insert(0, email)  # Populate email entry with current email

            college_label = tk.Label(self.profile_tab, text="College:")
            college_label.grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)
            self.college_entry = tk.Entry(self.profile_tab)
            self.college_entry.grid(row=3, column=1, padx=10, pady=10)
            self.college_entry.insert(0, college)  # Populate college entry with current college

            username_label = tk.Label(self.profile_tab, text="Username:")
            username_label.grid(row=4, column=0, padx=10, pady=10, sticky=tk.W)
            self.username_entry = tk.Entry(self.profile_tab)
            self.username_entry.grid(row=4, column=1, padx=10, pady=10)
            self.username_entry.insert(0, username)  # Populate username entry with current username

            password_label = tk.Label(self.profile_tab, text="Password:")
            password_label.grid(row=5, column=0, padx=10, pady=10, sticky=tk.W)
            self.password_entry = tk.Entry(self.profile_tab)
            self.password_entry.grid(row=5, column=1, padx=10, pady=10)

            # Button to save changes
            save_button = tk.Button(self.profile_tab, text="Save Changes", command=self.save_profile_changes, bg="#3498db", fg="white")
            save_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)
        else:
            messagebox.showwarning("Warning", "No HOD details found.")

    def save_profile_changes(self):
        # Retrieve updated HOD details from entry widgets
        new_name = self.name_entry.get()
        new_mob = self.mob_entry.get()
        new_email = self.email_entry.get()
        new_college = self.college_entry.get()
        new_username = self.username_entry.get()
        new_password = self.password_entry.get()

        # Update HOD details in the database
        query = "UPDATE hods SET name = %s, mob = %s, email = %s, college = %s, username = %s, password = %s WHERE id = %s"
        cursor.execute(query, (new_name, new_mob, new_email, new_college, new_username, new_password, self.hod_id))
        db.commit()

        # Show success message
        messagebox.showinfo("Success", "Profile updated successfully!")


   

# Example usage in your login.py after successful HOD login
def open_hod_interface(hod_id):
    # Create and run the HODInterface window
    root_hod_interface = tk.Tk()
    hod_interface = HODInterface(root_hod_interface, hod_id)
    root_hod_interface.mainloop()
