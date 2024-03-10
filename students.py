import tkinter as tk
from tkinter import messagebox as mb, IntVar
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

class Quiz:
    def __init__(self, root, quiz_id, student_id):
        self.root = root
        self.quiz_id = quiz_id
        self.student_id = student_id
        

        # self.root.state('zoomed')
        print(self.quiz_id)
        que = "select * from questions where quiz_id=%s"
        cursor.execute(que, (self.quiz_id,))
        quiz_que = cursor.fetchall()

        self.q_l = list()
        self.o_l = list()
        self.a_l = list()
        for question in quiz_que:
            self.q_l.append(question[2])
            self.o_l.append(list(question[3:7]))
            self.a_l.append(question[7])

        # Set the question, options, and answer
        self.question = self.q_l
        self.options = self.o_l
        self.answer = self.a_l

        
        # Create the main frame for the quiz interface
        self.frame = tk.Frame(self.root, bg="#3498db")
        self.frame.pack(expand=True)

        # Fetch questions from the database
        self.fetch_questions()

        # Initialize variables
        self.q_no = 0
        self.correct = 0
        self.time_left = 10  # Timer for each question
        self.timer_running = False


        # Set up the quiz interface
        self.setup_quiz()

    def setup_quiz(self):
        self.q_no = 0
        self.display_title()

        # Create a frame for the question
        self.question_frame = tk.Frame(self.frame)
        self.question_frame.pack(pady=20)  # Adjust padding as needed

        self.display_question()

        self.opt_selected = IntVar()
        self.opts = self.radio_buttons()

        # Create a frame for the buttons
        self.button_frame = tk.Frame(self.frame)
        self.button_frame.pack(pady=10)  # Adjust padding as needed

        self.display_options()
        self.buttons()
        self.display_timer()

        self.data_size = len(self.question)
        self.correct = 0

    def display_timer(self):
        # Display a label for the timer
        self.timer_label = tk.Label(self.frame, text=f"Time left: {self.time_left}s",
                                    font=("Arial", 12))
        self.timer_label.pack()

        # Start the timer countdown
        self.start_timer()

    def start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.update_timer()

    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=f"Time left: {self.time_left}s")
            self.timer_label.after(1000, self.update_timer)
        else:
            self.timer_running = False
            self.next_btn()

    def display_result(self):
        # Calculate the wrong count
        wrong_count = self.data_size - self.correct
        score = int(self.correct / self.data_size * 100)

        # Show result details in a message box
        mb.showinfo("Result", f"Score: {score}%\nCorrect: {self.correct}\nWrong: {wrong_count}")

        # Remove the assigned quiz from the student's cart
        self.remove_assigned_quiz()

        # Store the result in the database
        self.store_result(score)
        

    
    def store_result(self, score):
        # Insert the result into the results table
        query = "INSERT INTO results (student_id, quiz_id, score) VALUES (%s, %s, %s)"
        values = (self.student_id, self.quiz_id, score)
        cursor.execute(query, values)
        db.commit()

    def remove_assigned_quiz(self):
        # Remove the assigned quiz from the assigned_quizzes table
        query = "DELETE FROM assigned_quizzes WHERE student_id = %s AND quiz_id = %s"
        values = (self.student_id, self.quiz_id)
        cursor.execute(query, values)
        db.commit()


    def check_ans(self, q_no):
            # checks for if the selected option is correct
            s = self.opt_selected.get()
            if self.o_l[q_no][s-1] == self.answer[q_no]:
                # if the option is correct it return true
                return True
    

    def next_btn(self):
            self.timer_running = False
            # Check if the answer is correct
            if self.check_ans(self.q_no):
                
                print(self.q_no)
                # if the answer is correct it increments the correct by 1
                self.correct += 1
            
            # Moves to next Question by incrementing the q_no counter
            self.q_no += 1
            print(self.q_no)
            # checks if the q_no size is equal to the data size
            if self.q_no==self.data_size:
                
                # if it is correct then it displays the score
                self.display_result()
                
                # destroys the GUI
                self.frame.destroy()
            else:
                # shows the next question
                self.display_question()
                self.display_options()
                self.time_left = 10
                self.start_timer()
    
    def buttons(self):
        next_button = tk.Button(self.frame, text="Next", command=self.next_btn,
                                width=10, bg="blue", fg="white", font=("ariel", 16, "bold"))
        next_button.pack(pady=10)  # Adjust padding as needed

        quit_button = tk.Button(self.frame, text="Quit", command=self.frame.destroy,
                                width=5, bg="black", fg="white", font=("ariel", 16, "bold"))
        quit_button.pack(pady=10)


    def display_options(self):
        val = 0
        # Deselecting the options
        self.opt_selected.set(0)
        # Looping over the options to be displayed for the
        # text of the radio buttons.
        for option in self.options[self.q_no]:
            
            self.opts[val]['text'] = option
            self.opts[val].pack(anchor="w")  # Adjust anchor as needed
            val += 1
   
    def display_title(self):
        title = tk.Label(self.frame, text="QUIZ",
                         width=50, bg="black", fg="white", font=("ariel", 20, "bold"))
        title.pack(pady=10)  # Adjust padding as needed

    def display_question(self):
        # Clear the existing question label
        for widget in self.question_frame.winfo_children():
            widget.destroy()

        # Display the next question in the question frame
        q_no = tk.Label(self.question_frame, text=self.question[self.q_no], width=60,
                        font=('ariel', 16, 'bold'), anchor='w')
        q_no.pack()  # Adjust padding as needed
    
    def fetch_questions(self):
        # Fetch questions from the database based on quiz_id
        query = "SELECT * FROM questions WHERE quiz_id = %s"
        cursor.execute(query, (self.quiz_id,))
        quiz_questions = cursor.fetchall()

        self.question = []
        self.options = []
        self.answer = []

        for question in quiz_questions:
            self.question.append(question[2])
            self.options.append(list(question[3:7]))
            self.answer.append(question[7])


    def radio_buttons(self):
        q_list = []
        for option in self.options[self.q_no]:
            radio_btn = tk.Radiobutton(self.frame, text=" ", variable=self.opt_selected,
                                        value=len(q_list) + 1, font=("ariel", 14))
            q_list.append(radio_btn)
            radio_btn.pack(anchor="w")  # Adjust anchor as needed
        return q_list   
    
class StudentInterface:
    def __init__(self, root, student_id, username):
        self.root = root
        self.root.title("MCQ Quiz App - Student Interface")

        # Maximize the window to full screen
        self.root.state('zoomed')

        self.student_id = student_id
        self.username = username

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
        # Fetch student_id based on the username
        query_student_id = "SELECT id FROM students WHERE username = %s"
        cursor.execute(query_student_id, (self.username,))
        student_id = cursor.fetchone()[0]

        # Clear any unread result
        cursor.fetchall()

        # Fetch quizzes assigned to the student with upcoming dates and times
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        query = "SELECT quizzes.quiz_name, quizzes.date, quizzes.time " \
                "FROM quizzes " \
                "JOIN assigned_quizzes ON quizzes.id = assigned_quizzes.quiz_id " \
                "JOIN students ON students.id = assigned_quizzes.student_id " \
                "WHERE students.username = %s AND CONCAT(quizzes.date, ' ', quizzes.time) > %s"
        cursor.execute(query, (self.username, now))
        quiz_cart_data = cursor.fetchall()

        # Insert data into the Treeview
        for quiz in quiz_cart_data:
            quiz_cart_tree.insert("", tk.END, values=quiz)
        # Bind a function to the double-click event on a quiz row
        quiz_cart_tree.bind("<Double-1>", self.start_quiz)
      
    def start_quiz(self, event):
        selected_item = event.widget.selection()[0]
        quiz_name = event.widget.item(selected_item, "values")[0]

        # Execute the query to fetch quiz ID
        query = "SELECT id FROM quizzes WHERE quiz_name = %s"
        cursor.execute(query, (quiz_name,))
        quiz_id = cursor.fetchone()[0]  # Fetch single value from the result

        # Open a new window for the selected quiz using Toplevel
        quiz_window = tk.Toplevel(self.root)
        quiz_window.title("Quiz")
        quiz_window.geometry("800x600")  # Adjust the size as needed
        quiz = Quiz(quiz_window, quiz_id, self.student_id)

    

        

