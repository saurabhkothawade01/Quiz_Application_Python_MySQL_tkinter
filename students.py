import tkinter as tk
from tkinter import messagebox, IntVar
import mysql.connector
from tkinter import ttk
from datetime import datetime

# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="saurabh",
    database="mcq_quiz_app"
)
cursor = db.cursor()

class QuizWindow:
    def __init__(self, root, quiz_id, student_id):
        self.root = root
        self.root.title("MCQ Quiz App - Quiz")

        # Maximize the window to full screen
        self.root.state('zoomed')

        self.quiz_id = quiz_id
        self.student_id = student_id

        # Create a frame to contain the widgets
        self.frame = tk.Frame(self.root)
        self.frame.pack(expand=True)

        # Set the current question index
        self.current_question_index = 0

        # Load quiz questions and options
        self.load_quiz_questions()

        # Add navigation buttons
        self.add_navigation_buttons()

    def load_quiz_questions(self):
        # Fetch questions and options for the selected quiz
        query = "SELECT * FROM questions WHERE quiz_id = %s"
        cursor.execute(query, (self.quiz_id,))
        self.questions_data = cursor.fetchall()

        # Create labels and radio buttons for the current question
        self.create_question_widgets()

    def create_question_widgets(self):
        # Destroy existing question widgets
        for widget in self.frame.winfo_children():
            widget.destroy()

        # Get the current question
        current_question = self.questions_data[self.current_question_index]

        # Create labels and radio buttons for the current question
        question_label = tk.Label(self.frame, text=current_question[2], font=("Helvetica", 12))
        question_label.pack(pady=5)

        # Options start from index 3 in the retrieved data
        options = current_question[3:7]

        # Create IntVar variables to track selected option for each question
        self.selected_options_vars = [IntVar() for _ in range(len(options))]

        for i, option in enumerate(options):
            option_radio = tk.Radiobutton(self.frame, text=option, value=i + 1, variable=self.selected_options_vars[i])
            option_radio.pack()

    def add_navigation_buttons(self):
        # Create navigation buttons based on the current question index
        if self.current_question_index < len(self.questions_data) - 1:
            next_button = tk.Button(self.frame, text="Next", command=self.next_question)
            next_button.pack(side=tk.LEFT, padx=10)
        else:
            submit_button = tk.Button(self.frame, text="Submit", command=self.submit_quiz)
            submit_button.pack(side=tk.LEFT, padx=10)

        if self.current_question_index > 0:
            previous_button = tk.Button(self.frame, text="Previous", command=self.previous_question)
            previous_button.pack(side=tk.LEFT, padx=10)

        clear_button = tk.Button(self.frame, text="Clear", command=self.clear_answer)
        clear_button.pack(side=tk.LEFT, padx=10)

    def next_question(self):
        # Move to the next question if available
        if self.current_question_index < len(self.questions_data) - 1:
            self.current_question_index += 1
            self.create_question_widgets()
            self.add_navigation_buttons()

    def previous_question(self):
        # Move to the previous question if available
        if self.current_question_index > 0:
            self.current_question_index -= 1
            self.create_question_widgets()
            self.add_navigation_buttons()

    def clear_answer(self):
        # Clear the selected option for the current question
        for var in self.selected_options_vars:
            var.set(0)

    def submit_quiz(self):
        # Add your logic here to handle the submitted quiz answers
        # You can compare selected options with the correct answers from the database
        # Update the student's score and perform any other necessary actions

        messagebox.showinfo("Quiz Submitted", "Quiz submitted successfully!")
        self.root.destroy()

class StudentInterface:
    def __init__(self, root, student_id):
        self.root = root
        self.root.title("MCQ Quiz App - Student Interface")

        # Maximize the window to full screen
        self.root.state('zoomed')

        self.student_id = student_id

        # Create a frame to contain the widgets
        self.frame = tk.Frame(self.root)
        self.frame.pack(expand=True)

        # Set up the quiz cart
        self.setup_quiz_cart()

    def setup_quiz_cart(self):
        # Create a Treeview widget for displaying quiz details
        quiz_cart_tree = ttk.Treeview(self.frame, columns=("Quiz Name", "Date", "Time"), show="headings")
        quiz_cart_tree.heading("Quiz Name", text="Quiz Name")
        quiz_cart_tree.heading("Date", text="Date")
        quiz_cart_tree.heading("Time", text="Time")

        # Add a vertical scrollbar
        scroll_y = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=quiz_cart_tree.yview)
        quiz_cart_tree.configure(yscrollcommand=scroll_y.set)

        # Pack the Treeview and scrollbar
        quiz_cart_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        # Populate the quiz cart
        self.populate_quiz_cart(quiz_cart_tree)

    def populate_quiz_cart(self, quiz_cart_tree):
        # Fetch quizzes assigned to the student with upcoming dates and times
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        query = "SELECT quizzes.quiz_name, quizzes.date, quizzes.time " \
                "FROM quizzes " \
                "JOIN assigned_quizzes ON quizzes.id = assigned_quizzes.quiz_id " \
                "WHERE assigned_quizzes.student_id = %s AND CONCAT(quizzes.date, ' ', quizzes.time) > %s"
        cursor.execute(query, (self.student_id, now))
        quiz_cart_data = cursor.fetchall()

        # Insert data into the Treeview
        for quiz in quiz_cart_data:
            quiz_cart_tree.insert("", tk.END, values=quiz)
        # Bind a function to the double-click event on a quiz row
        quiz_cart_tree.bind("<Double-1>", self.start_quiz)
      
    def start_quiz(self, event):
        # Get the selected quiz_id from the Treeview
        selected_item = event.widget.selection()[0]
        quiz_id = event.widget.item(selected_item, "values")[0]

        # Open a new window for the selected quiz
        root_quiz_window = tk.Tk()
        quiz_window = QuizWindow(root_quiz_window, 10, self.student_id)
        root_quiz_window.mainloop()
