import tkinter as tk
import random


questions = [
    "What is the capital of France?Paris,Moscow,Yerevan,Berlin",
    "What is 2 + 2?4,3,5,6",
    "What is the capital of Georgia?Tbilisi,Moscow,Yerevan,Berlin",
    "What is the largest planet in our solar system?Jupiter,Earth,Mars,Venus",
    "What is the main ingredient in guacamole?Avocado,Tomato,Cucumber,Carrot",
    "What is the freezing point of water in Celsius?0,32,-1,100",
    "What is the chemical symbol for gold?Au,Ag,Fe,Pb",
    "Which country is known as the Land of the Rising Sun?Japan,China,India,Armenia",
    "What is the capital of Austria?Vienna,Moscow,Yerevan,Berlin",
    "Who wrote 'Romeo and Juliet'?William Shakespeare,Mark Twain,Charles Dickens,Jane Austen",
    "What is the square root of 16?4,3,5,6",
    "What gas do plants absorb from the atmosphere?Carbon dioxide,Oxygen,Nitrogen,Hydrogen",
    "What is the longest river in the world?Nile,Amazon,Yangtze,Mississippi",
    "Which planet is known as the Red Planet?Mars,Venus,Mercury,Saturn",
    "How many continents are there on Earth?7,5,6,8",
    "What is the main language spoken in Brazil?Portuguese,Spanish,English,French",
    "What is the capital of Italy?Rome,Venice,Milan,Florence",
    "Which element has the atomic number 1?Hydrogen,Helium,Lithium,Oxygen",
    "What is the largest mammal in the world?Blue whale,Elephant,Great white shark,Giraffe",
    "What is the smallest prime number?2,1,3,5",
]


def get_index():
    """
        Description: Choose 10 random numbers and put them into a list

        Returns: List of numbers
    """
    index = []

    while len(index) < 10:
        i = random.randint(0, len(questions) - 1)

        if i not in index:
            index.append(i)

    return index


def get_questions(ind):
    """
        Description: Create list of questions using random indexes

        Parameters: indexes (10 random numbers)

        Returns: List of questions
    """
    quests = []

    for i in ind:
        quests.append(questions[i])

    return quests


def get_questions_dict(quests):
    """
        Description: Separate questions from answers and put them into a dict

        Parameters: list of questions

        Returns: Dictionary of questions
    """
    questions_dict = {}

    for question in quests:
        q, a = question.split("?")
        questions_dict[q] = a.split(",")

    return questions_dict


def on_button_click():
    """
        Description: When user enters their name,
        the first window is closed and the second is opened

        Returns: name of the user
    """
    global name
    name = entry.get()

    if name:
        root.destroy()
        open_second_window()

    return name


def open_second_window():
    """
        Description: Functionality of second window
    """
    global question_label, answer_entry, result_label, score_label, \
        submit_button, questions_list, COUNT, CURRENT_INDEX, help_button1, help_button2, help_button3

    index = get_index()
    questions = get_questions(index)
    questions_dict = get_questions_dict(questions)

    second_window = tk.Tk()
    second_window.geometry('500x300')
    second_window.title("Who Wants To Be A Millionaire?")
    second_window.configure(bg='#142666')

    question_label = tk.Label(second_window, text="", fg='#8392c9', font=('Roboto', 10, 'bold'))
    question_label.pack(pady=20)
    question_label.configure(bg='#142666')

    answer_entry = tk.Entry(second_window, width=30)
    answer_entry.pack(pady=5)

    submit_button = tk.Button(second_window, text="Submit", command=check_answer)
    submit_button.pack(pady=10)
    submit_button.configure(bg='#8392c9')

    result_label = tk.Label(second_window, text="", fg='#8392c9', font=('Roboto', 10, 'bold'))
    result_label.pack(pady=20)
    result_label.configure(bg='#142666')

    score_label = tk.Label(second_window, text="Score: 0", fg='#8392c9', font=('Roboto', 10, 'bold'))
    score_label.pack(pady=10)
    score_label.configure(bg='#142666')

    button_frame = tk.Frame(second_window, bg='#142666')
    button_frame.pack(pady=10)

    help_button1 = tk.Button(button_frame, text='1', command=use_help1, bg='#8392c9')
    help_button1.pack(side=tk.LEFT, padx=5)
    
    help_button2 = tk.Button(button_frame, text='2', command=use_help2, bg='#8392c9')
    help_button2.pack(side=tk.LEFT, padx=5)

    help_button3 = tk.Button(button_frame, text='3', command=use_help3, bg='#8392c9')
    help_button3.pack(side=tk.LEFT, padx=5)

    questions_list = list(questions_dict.items())
    random.shuffle(questions_list)
    COUNT = 0
    CURRENT_INDEX = 0
    next_question()

    second_window.mainloop()


def check_answer():
    """
        Description: Checks the answer user has input
    """
    global COUNT, CURRENT_INDEX, CURRENT_CORRECT_ANSWER
    
    answer = answer_entry.get().strip()

    if answer.lower() == CURRENT_CORRECT_ANSWER.lower():
        result_label.config(text="Correct!")
        COUNT += 1
    else:
        result_label.config(text=f"Wrong. The correct answer was: {CURRENT_CORRECT_ANSWER}")

    score_label.config(text=f"Score: {COUNT}")
    CURRENT_INDEX += 1

    if CURRENT_INDEX < len(questions_list):
        next_question()
    else:
        result_label.config(text=f"You answered {COUNT} questions correctly.")
        answer_entry.config(state=tk.DISABLED)
        submit_button.config(state=tk.DISABLED)
        user_score = COUNT
        save_score_to_file(name, user_score)


def use_help1():
    """
        Description: Remove two incorrect answers from the choices
    """
    global current_answers

    if help_button1.cget('state') == tk.DISABLED:
        return

    incorrect_answers = [ans for ans in current_answers if ans != CURRENT_CORRECT_ANSWER]
    random.shuffle(incorrect_answers)
    answers_to_remove = incorrect_answers[:2]

    current_answers = [ans for ans in current_answers if ans not in answers_to_remove]
    question_label.config(text=f"{questions_list[CURRENT_INDEX][0]} \n {', '.join(current_answers)}")

    help_button1.pack_forget()
    disable_help_buttons()


def use_help2():
    """
        Description: Remove two incorrect answers from the choices
    """
    global current_answers

    if help_button2.cget('state') == tk.DISABLED:
        return

    incorrect_answers = [ans for ans in current_answers if ans != CURRENT_CORRECT_ANSWER]
    random.shuffle(incorrect_answers)
    answers_to_remove = incorrect_answers[:2]

    current_answers = [ans for ans in current_answers if ans not in answers_to_remove]
    question_label.config(text=f"{questions_list[CURRENT_INDEX][0]} \n {', '.join(current_answers)}")

    help_button2.pack_forget()
    disable_help_buttons()


def use_help3():
    """
        Description: Remove two incorrect answers from the choices
    """
    global current_answers

    if help_button3.cget('state') == tk.DISABLED:
        return

    incorrect_answers = [ans for ans in current_answers if ans != CURRENT_CORRECT_ANSWER]
    random.shuffle(incorrect_answers)
    answers_to_remove = incorrect_answers[:2]

    current_answers = [ans for ans in current_answers if ans not in answers_to_remove]
    question_label.config(text=f"{questions_list[CURRENT_INDEX][0]} \n {', '.join(current_answers)}")

    help_button3.pack_forget()
    disable_help_buttons()


def disable_help_buttons():
    help_button1.config(state=tk.DISABLED)
    help_button2.config(state=tk.DISABLED)
    help_button3.config(state=tk.DISABLED)


def next_question():
    """
        Description: The function will run until the questions run out
    """
    global CURRENT_CORRECT_ANSWER, CURRENT_INDEX, current_answers

    q, a = questions_list[CURRENT_INDEX]
    current_question = q
    CURRENT_CORRECT_ANSWER = a[0]
    current_answers = a.copy()
    random.shuffle(a)
    question_label.config(text=f"{current_question} \n {', '.join(a)}")
    answer_entry.delete(0, tk.END)

    help_button1.pack(side=tk.LEFT, padx=5)
    help_button2.pack(side=tk.LEFT, padx=5)
    help_button3.pack(side=tk.LEFT, padx=5)
    help_button1.config(state=tk.NORMAL)
    help_button2.config(state=tk.NORMAL)
    help_button3.config(state=tk.NORMAL)


def save_score_to_file(user_name, user_score):
    """
    Description: Writing and sorting each person's name and score in a file
    """

    try:
        with open("top.txt", "r", encoding="utf-8") as f:
            scores = [line.strip().split(": ") for line in f]
            scores = [(name, int(score)) for name, score in scores]
    except FileNotFoundError:
        scores = []

    scores.append((user_name, user_score))
    scores.sort(key=lambda x: x[1], reverse=True)

    with open("top.txt", "w", encoding="utf-8") as f:
        for name, score in scores:
            f.write(f"{name}: {score}\n")


root = tk.Tk()
root.title("Name Input")
root.configure(bg='#142666')
root.geometry('250x150')

frame = tk.Frame(root)
frame.pack(pady=30, padx=30)
frame.configure(bg='#142666')

label = tk.Label(frame, text="Enter your name", fg='#8392c9', font=('Roboto', 10, 'bold'))
label.pack(pady=1)
label.configure(bg='#142666')

entry = tk.Entry(frame)
entry.pack(pady=10)

button = tk.Button(frame, text="Submit", command=on_button_click)
button.pack(pady=1)
button.configure(bg='#8392c9')


def main():
    """
        The main function
    """
    root.mainloop()


if __name__ == '__main__':
    main()