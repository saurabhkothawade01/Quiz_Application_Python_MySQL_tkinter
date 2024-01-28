import tkinter as tk
import pandas as pd
from tkinter import filedialog, ttk, messagebox
import mysql.connector

# Add this code at the beginning to connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="saurabh",
    database="mcq_quiz_app"
)
cursor = db.cursor()

class TeacherInterface:
    def __init__(self, root, teacher_id):
        self.root = root  # Store the root window in an instance variable
        self.root.title("MCQ Quiz App - Teacher Interface")
        
        # Maximize the window to full screen
        self.root.state('zoomed')

        self.teacher_id = teacher_id

      #   self.import_button = tk.Button(root, text="Import Questions", command=self.import_questions)
      #   self.import_button.pack(pady=20)
        
        # Style for tabs
        style = ttk.Style()
        style.configure("TNotebook", background="#ecf0f1")
        style.configure("TNotebook.Tab", background="#3498db", foreground="black", padding=[10, 5])

        # Create a notebook (tabbed interface)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Add Questions Tab
        self.add_questions_tab = tk.Frame(self.notebook)
        self.notebook.add(self.add_questions_tab, text="Add Questions")
        self.setup_add_questions_tab()

        # Add Students Tab
        self.add_students_tab = tk.Frame(self.notebook)
        self.notebook.add(self.add_students_tab, text="Add Students")
        self.setup_add_students_tab()

        # See Results Tab
        self.see_results_tab = tk.Frame(self.notebook)
        self.notebook.add(self.see_results_tab, text="See Results")
        self.setup_see_results_tab()

        # Manage Profile Tab
        self.manage_profile_tab = tk.Frame(self.notebook)
        self.notebook.add(self.manage_profile_tab, text="Manage Profile")
        self.setup_manage_profile_tab()
      
    
    def setup_add_questions_tab(self):
        # Create two frames to divide the "Add Questions" tab into two sections
        left_frame = tk.Frame(self.add_questions_tab)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)

        right_frame = tk.Frame(self.add_questions_tab)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Left Section (Import Questions Button)
        import_button = tk.Button(left_frame, text="Import Questions", command=self.import_questions, font=("Helvetica", 14), bg="#2ecc71", fg="white")
        import_button.pack(pady=20)

        # Right Section (List of Quizzes)
        self.setup_quizzes_table(right_frame)

    def setup_quizzes_table(self, parent_frame):
        # Create a Treeview widget for displaying quizzes
        quiz_tree = ttk.Treeview(parent_frame, columns=("Subject", "Quiz Name", "No. of Questions", "Status"), show="headings")

        # Define column headings
        quiz_tree.heading("Subject", text="Subject")
        quiz_tree.heading("Quiz Name", text="Quiz Name")
        quiz_tree.heading("No. of Questions", text="No. of Questions")
        quiz_tree.heading("Status", text="Status")

        # Add a vertical scrollbar
        scroll_y = ttk.Scrollbar(parent_frame, orient=tk.VERTICAL, command=quiz_tree.yview)
        quiz_tree.configure(yscrollcommand=scroll_y.set)

        # Pack the Treeview and scrollbar
        quiz_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        # Populate the Treeview with sample data (you'll replace this with your actual data)
        self.populate_quizzes_table(quiz_tree)

    def populate_quizzes_table(self, quiz_tree):
      # Fetch data from the database
      query = "SELECT subjects.name, quizzes.quiz_name, quizzes.num_questions, quizzes.status " \
                  "FROM subjects " \
                  "JOIN quizzes ON subjects.id = quizzes.subject_id"
      cursor.execute(query)
      data = cursor.fetchall()

      # Insert data into the Treeview
      for quiz in data:
            quiz_tree.insert("", tk.END, values=quiz)


    def setup_add_students_tab(self):
        # Add code for "Add Students" tab here
        pass

    def setup_see_results_tab(self):
        # Add code for "See Results" tab here
        pass

    def setup_manage_profile_tab(self):
        # Add code for "Manage Profile" tab here
        pass
    
    def import_questions(self):
        # Create a new window for selecting subjects and quizzes
        import_window = tk.Toplevel(self.root)
        import_window.title("Import Questions")

        # Add labels and dropdowns for subjects and quizzes
        subject_label = tk.Label(import_window, text="Select Subject:")
        subject_label.pack(pady=10)
        subject_var = tk.StringVar()
        subjects = self.get_subjects()
        subject_dropdown = ttk.Combobox(import_window, textvariable=subject_var, values=subjects)
        subject_dropdown.pack(pady=10)

        quiz_label = tk.Label(import_window, text="Select Quiz:")
        quiz_label.pack(pady=10)
        quiz_var = tk.StringVar()
        quizzes = []  # Empty list initially
        quiz_dropdown = ttk.Combobox(import_window, textvariable=quiz_var, values=quizzes)
        quiz_dropdown.pack(pady=10)

        # Event handler for subject dropdown selection change
        def update_quizzes_dropdown(event):
            selected_subject = subject_var.get()
            quizzes = self.get_quizzes(selected_subject)
            quiz_dropdown['values'] = quizzes  # Update quiz dropdown values

        # Bind the event handler to the <<ComboboxSelected>> event
        subject_dropdown.bind("<<ComboboxSelected>>", update_quizzes_dropdown)

        # Add "OK" and "Cancel" buttons
        ok_button = tk.Button(import_window, text="OK", command=lambda: self.import_from_excel(subject_var.get(), quiz_var.get(), import_window))
        ok_button.pack(side=tk.LEFT, padx=10)
        cancel_button = tk.Button(import_window, text="Cancel", command=import_window.destroy)
        cancel_button.pack(side=tk.RIGHT, padx=10)

        

        # Call the mainloop to display the window
        import_window.mainloop()

    def import_from_excel(self, subject, quiz, import_window):
        # Use file dialog to select the Excel sheet
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])

        if file_path:
            try:
                # Read the Excel sheet
                df = pd.read_excel(file_path)

                # Extract questions and options
                questions = []
                for index, row in df.iterrows():
                    question_text = row[0]
                    options = row[1:5].tolist()  # Assuming the options are in columns 2 to 6
                    correct_option = row[5]
                    questions.append((question_text, options, correct_option))

                # Insert questions into the database
                self.insert_questions(subject, quiz, questions)

                # Update quiz information in the quizzes table
                num_questions = len(questions)
                self.update_quiz_info(subject, quiz, num_questions)

                messagebox.showinfo("Import Successful", "Questions imported successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
            finally:
                import_window.destroy()

    def update_quiz_info(self, subject, quiz, num_questions):
        # Get subject_id and quiz_id based on the provided subject and quiz names
        subject_id = self.get_subject_id(subject)
        quiz_id = self.get_quiz_id(quiz, subject_id)

        # Update the "num_questions" and "status" columns in the quizzes table
        query = "UPDATE quizzes SET num_questions = %s, status = %s WHERE id = %s"
        cursor.execute(query, (num_questions, "Not Given", quiz_id))

        # Commit the changes to the database
        db.commit()

    def get_subjects(self):
        # Fetch subjects from the database
        query = "SELECT name FROM subjects"
        cursor.execute(query)
        subjects = [row[0] for row in cursor.fetchall()]
        return subjects

    def get_quizzes(self, subject_name):
        # Fetch quizzes for the selected subject from the database
        query = "SELECT quiz_name FROM quizzes WHERE subject_id IN (SELECT id FROM subjects WHERE name = %s)"
        cursor.execute(query, (subject_name,))
        quizzes = [row[0] for row in cursor.fetchall()]
        return quizzes

    def insert_questions(self, subject, quiz, questions):
        # Get subject_id and quiz_id based on the provided subject and quiz names
        subject_id = self.get_subject_id(subject)
        quiz_id = self.get_quiz_id(quiz, subject_id)

        # Insert questions into the questions table
        for question_text, options, correct_option in questions:
            query = "INSERT INTO questions (quiz_id, question_text, option1, option2, option3, option4, correct_option) " \
                    "VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (quiz_id, question_text, *options, correct_option))
        
        # Commit the changes to the database
        db.commit()

    

    def get_subject_id(self, subject_name):
        # Fetch subject_id based on the provided subject name
        query = "SELECT id FROM subjects WHERE name = %s"
        cursor.execute(query, (subject_name,))
        subject_id = cursor.fetchone()
        if subject_id:
            return subject_id[0]
        else:
            # Handle the case where the subject doesn't exist
            return None

    def get_quiz_id(self, quiz_name, subject_id):
        # Fetch quiz_id based on the provided quiz name and subject_id
        query = "SELECT id FROM quizzes WHERE quiz_name = %s AND subject_id = %s"
        cursor.execute(query, (quiz_name, subject_id))
        quiz_id = cursor.fetchone()
        if quiz_id:
            return quiz_id[0]
        else:
            # Handle the case where the quiz doesn't exist
            return None