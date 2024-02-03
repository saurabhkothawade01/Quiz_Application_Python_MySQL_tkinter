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

        assign_quiz_button = tk.Button(left_frame, text="Assign Quiz", command=self.assign_quiz, font=("Helvetica", 14), bg="#3498db", fg="white")
        assign_quiz_button.pack(pady=20)


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

        # Inside the setup_quizzes_table method, bind the show_quiz_details function to the double-click event on a quiz row:
        quiz_tree.bind("<Double-1>", lambda event: self.show_quiz_details(quiz_tree.item(quiz_tree.selection())['values'][1]))

    def populate_quizzes_table(self, quiz_tree):
      # Fetch data from the database where num_questions is not null
      query = "SELECT subjects.name, quizzes.quiz_name, quizzes.num_questions, quizzes.status " \
                  "FROM subjects " \
                  "JOIN quizzes ON subjects.id = quizzes.subject_id " \
                  "WHERE quizzes.num_questions IS NOT NULL"
      cursor.execute(query)
      data = cursor.fetchall()

      # Insert data into the Treeview
      for quiz in data:
            quiz_tree.insert("", tk.END, values=quiz)



    def setup_add_students_tab(self):
      # Create two frames to divide the "Add Students" tab into two sections
      left_frame = tk.Frame(self.add_students_tab)
      left_frame.pack(side=tk.LEFT, fill=tk.Y)

      right_frame = tk.Frame(self.add_students_tab)
      right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

      # Left Section (Import Students Button)
      import_students_button = tk.Button(left_frame, text="Import Students", command=self.import_students, font=("Helvetica", 14), bg="#2ecc71", fg="white")
      import_students_button.pack(pady=20)

      # Right Section (List of Students and Class Info)
      self.setup_students_and_class_table(right_frame)


    def setup_students_and_class_table(self, parent_frame):
      # Create a Treeview widget for displaying students and class info
      students_and_class_tree = ttk.Treeview(parent_frame, columns=("Class", "No. of Students"), show="headings")

      # Define column headings
      students_and_class_tree.heading("Class", text="Class")
      students_and_class_tree.heading("No. of Students", text="No. of Students")

      # Add a vertical scrollbar
      scroll_y = ttk.Scrollbar(parent_frame, orient=tk.VERTICAL, command=students_and_class_tree.yview)
      students_and_class_tree.configure(yscrollcommand=scroll_y.set)

      # Pack the Treeview and scrollbar
      students_and_class_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
      scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

      # Populate the Treeview with sample data (you'll replace this with your actual data)
      self.populate_students_and_class_table(students_and_class_tree)

    def populate_students_and_class_table(self, students_and_class_tree):
      # Fetch data from the database for class-wise student count
      query = "SELECT class, COUNT(*) as num_students FROM students GROUP BY class"
      cursor.execute(query)
      data = cursor.fetchall()

      # Insert data into the Treeview
      for class_info in data:
            students_and_class_tree.insert("", tk.END, values=class_info)

#     def populate_students_table(self, student_tree):
#         # Fetch data from the database for students
#         query = "SELECT id, username, password FROM students"
#         cursor.execute(query)
#         data = cursor.fetchall()

#         # Insert data into the Treeview
#         for student in data:
#             student_tree.insert("", tk.END, values=student)

    def import_students(self):
      # Create a new window for selecting the class
      import_window = tk.Toplevel(self.root)
      import_window.title("Import Students")

      # Label and dropdown for selecting class
      class_label = tk.Label(import_window, text="Select Class:")
      class_label.pack(pady=10)

      class_var = tk.StringVar()
      classes = ["Class A", "Class B", "Class C"]  # Replace with your actual class names
      class_dropdown = ttk.Combobox(import_window, textvariable=class_var, values=classes)
      class_dropdown.pack(pady=10)

      # Add "OK" and "Cancel" buttons
      ok_button = tk.Button(import_window, text="OK", command=lambda: self.import_students_from_excel(class_var.get(), import_window))
      ok_button.pack(side=tk.LEFT, padx=10)
      cancel_button = tk.Button(import_window, text="Cancel", command=import_window.destroy)
      cancel_button.pack(side=tk.RIGHT, padx=10)

      # Call the mainloop to display the window
      import_window.mainloop()

    def import_students_from_excel(self, selected_class, import_window):
      if selected_class:
            try:
                  # Read Excel file into a Pandas DataFrame
                  file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
                  if file_path:
                        df = pd.read_excel(file_path)

                        # Validate column names
                        required_columns = ["Id", "username", "password"]
                        if set(required_columns).issubset(df.columns):
                              # Insert students into the database with class information
                              students = [(row["Id"], row["username"], row["password"], selected_class) for index, row in df.iterrows()]
                              self.insert_students(students)

                              # Update the Treeview with the new data
                              student_tree = self.add_students_tab.winfo_children()[1].winfo_children()[0]  # Accessing the Treeview widget
                              student_tree.delete(*student_tree.get_children())  # Clear existing data
                              self.populate_students_and_class_table(student_tree)  # Populate Treeview with updated data

                              messagebox.showinfo("Import Successful", "Students imported successfully.")
                        else:
                              messagebox.showerror("Error", "Invalid Excel file format. Please check the column names.")
                  else:
                        messagebox.showwarning("Warning", "No file selected.")
            except Exception as e:
                  messagebox.showerror("Error", f"An error occurred: {str(e)}")
            finally:
                  import_window.destroy()

    def insert_students(self, students):
      # Insert students into the students table
      for student in students:
            query = "INSERT INTO students (id, username, password, class) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, student)

      # Commit the changes to the database
      db.commit()
            

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
      file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
      if file_path:
            try:
                df = pd.read_excel(file_path)

                questions = []
                for index, row in df.iterrows():
                    question_text = row[0]
                    options = row[1:5].tolist()  # Assuming the options are in columns 2 to 6
                    correct_option = row[5]
                    questions.append((question_text, options, correct_option))

                self.insert_questions(subject, quiz, questions)
                num_questions = len(questions)
                self.update_quiz_info(subject, quiz, num_questions)

                # Update the Treeview with the new data
                #quiz_tree = self.notebook.tab(0, "window").winfo_children()[1].winfo_children()[1]  # Accessing the Treeview widget
                quiz_tree = self.add_questions_tab.winfo_children()[1].winfo_children()[0]

                quiz_tree.delete(*quiz_tree.get_children())  # Clear existing data
                self.populate_quizzes_table(quiz_tree)  # Populate Treeview with updated data

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

    def get_quiz_id(self, selected_quiz):
      # Fetch quiz_id based on the provided quiz name
      query = "SELECT id FROM quizzes WHERE quiz_name = %s"
      cursor.execute(query, (selected_quiz,))
      quiz_id = cursor.fetchone()
      if quiz_id:
            return quiz_id[0]
      else:
            # Handle the case where the quiz doesn't exist
            return None
      
    def show_quiz_details(self, selected_quiz):
      # Fetch quiz details from the database
      query = "SELECT question_text, option1, option2, option3, option4, correct_option " \
        "FROM questions WHERE quiz_id = (SELECT id FROM quizzes WHERE quiz_name = %s LIMIT 1)"
      cursor.execute(query, (selected_quiz,))
      quiz_details = cursor.fetchall()


      # Create a new window to display quiz details
      details_window = tk.Toplevel(self.root)
      details_window.title(f"Quiz Details - {selected_quiz}")

      # Create a Treeview to display quiz details
      quiz_details_tree = ttk.Treeview(details_window, columns=("Question", "Option 1", "Option 2", "Option 3", "Option 4", "Correct Option"), show="headings")
      quiz_details_tree.heading("Question", text="Question")
      quiz_details_tree.heading("Option 1", text="Option 1")
      quiz_details_tree.heading("Option 2", text="Option 2")
      quiz_details_tree.heading("Option 3", text="Option 3")
      quiz_details_tree.heading("Option 4", text="Option 4")
      quiz_details_tree.heading("Correct Option", text="Correct Option")

      # Populate the Treeview with quiz details
      for detail in quiz_details:
            quiz_details_tree.insert("", tk.END, values=detail)

      # Add a vertical scrollbar
      scroll_y = ttk.Scrollbar(details_window, orient=tk.VERTICAL, command=quiz_details_tree.yview)
      quiz_details_tree.configure(yscrollcommand=scroll_y.set)

      # Pack the Treeview and scrollbar
      quiz_details_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
      scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
    
    def assign_quiz(self):
      # Get the selected quiz from the Treeview
      selected_quiz = self.get_selected_quiz()

      if selected_quiz:
            # Create a new window for selecting the class to assign the quiz
            assign_window = tk.Toplevel(self.root)
            assign_window.title("Assign Quiz")

            # Label and dropdown for selecting class
            class_label = tk.Label(assign_window, text="Select Class:")
            class_label.pack(pady=10)

            class_var = tk.StringVar()
            classes = ["Class A", "Class B", "Class C"]  # Replace with your actual class names
            class_dropdown = ttk.Combobox(assign_window, textvariable=class_var, values=classes)
            class_dropdown.pack(pady=10)

            # Add "OK" and "Cancel" buttons
            ok_button = tk.Button(assign_window, text="OK", command=lambda: self.assign_quiz_to_class(selected_quiz, class_var.get(), assign_window))
            ok_button.pack(side=tk.LEFT, padx=10)
            cancel_button = tk.Button(assign_window, text="Cancel", command=assign_window.destroy)
            cancel_button.pack(side=tk.RIGHT, padx=10)

            # Call the mainloop to display the window
            assign_window.mainloop()
      else:
            messagebox.showwarning("Warning", "Please select a quiz to assign.")

    def get_selected_quiz(self):
      # Get the selected item from the quizzes Treeview
      quiz_tree = self.add_questions_tab.winfo_children()[1].winfo_children()[0]
      selected_item = quiz_tree.selection()

      if selected_item:
            return quiz_tree.item(selected_item)['values'][1]  # Quiz name is at index 1
      else:
            return None

    def assign_quiz_to_class(self, selected_quiz, selected_class, assign_window):
      if selected_class:
            try:
                  # Get the quiz_id based on the selected quiz name
                  quiz_id = self.get_quiz_id(selected_quiz)

                  # Get the student_ids for the selected class
                  student_ids = self.get_student_ids_by_class(selected_class)

                  # Assign the quiz to each student in the selected class
                  for student_id in student_ids:
                        self.insert_assigned_quiz(student_id, quiz_id)

                        messagebox.showinfo("Assignment Successful", f"The quiz '{selected_quiz}' has been assigned to the students in '{selected_class}'.")
            except Exception as e:
                  messagebox.showerror("Error", f"An error occurred: {str(e)}")
            finally:
                  # Close the assignment window
                  assign_window.destroy()
      else:
            messagebox.showwarning("Warning", "Please select a class to assign the quiz.")

    def get_student_ids_by_class(self, selected_class):
      # Check if there's an open result set and consume it
      if cursor.with_rows:
            cursor.fetchall()

      # Fetch student_ids for the selected class from the database
      query = "SELECT id FROM students WHERE class = %s"
      cursor.execute(query, (selected_class,))
      student_ids = [row[0] for row in cursor.fetchall()]

      return student_ids

    def insert_assigned_quiz(self, student_id, quiz_id):
      print(student_id)
      print(quiz_id)
      # Insert the assigned quiz into the assigned_quizzes table
      query = "INSERT INTO assigned_quizzes (student_id, quiz_id) VALUES (%s, %s)"
      cursor.execute(query, (student_id, quiz_id))

      # Commit the changes to the database
      db.commit()


