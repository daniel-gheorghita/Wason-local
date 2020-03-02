from tkinter import *
from tkinter import messagebox
import numpy as np

window = Tk()
status = "introduction"
instructions_string = "Information about Wason here. Frère Jacques Frère Jacques Dormez-vous \
        Dormez-vous Sonnez les matines Sonnez les matines \
        Ding, ding, dong \
        Ding, ding, dong \
        Frère Jacques\
        Frère Jacques\
        Dormez-vous\
        Dormez-vous\
        Sonnez les matines\
        Sonnez les matines\
        Ding, ding, dong\
        Ding, ding, dong\
        Ding, ding, dong\
        Ding, ding, dong"

questions = []
question_index = 0
correct_answers = []
subject_answers = []
question_text = StringVar()
card_1_text = StringVar()
card_2_text = StringVar()
card_3_text = StringVar()
card_4_text = StringVar()

def clicked_card_1():
    pass

def clicked_card_2():
    pass

def clicked_card_3():
    pass

def clicked_card_4():
    pass

def clicked_instructions():
    messagebox.showinfo( title="Info", message=instructions_string)

def clicked_start():
    status = "running"
    # Place testing window items
    card_1.grid(column=1, row=1)
    card_2.grid(column=2, row=1)
    card_3.grid(column=3, row=1)
    card_4.grid(column=4, row=1)
    instructions.grid(column=0,row=2)
    short_instructions_fr.grid(column=0, row=1)

    # Hide start window 
    start_test.place_forget()
    greeting.grid_forget()
    long_instructions_fr.grid_forget()


# Inits
for i in range(10):
    questions.append("Question {}".format(i))
    correct_answers.append([i%4,int(i/4)])

print(questions)
print(correct_answers)

window.title("Wason Test for Reasoning Tasks")
window.geometry('600x400')
question_text.set('')
card_1_text.set('')
card_2_text.set('')
card_3_text.set('')
card_4_text.set('')

# Start window
font = ('Helvetica', 20)
start_test = Button(window, text="Commencer!", command=clicked_start, font=font)
greeting = Label(window, text="Bonjour!")
long_instructions_fr = Label(window, text=instructions_string)

# Testing window
short_instructions_fr = Label(window, text="Presez les dous cardeaux pour ajuter tester la proposition.")
card_1 = Button(window, textvariable=card_1_text, command=clicked_card_1, font=font)
card_2 = Button(window, textvariable=card_2_text, command=clicked_card_2, font=font)
card_3 = Button(window, textvariable=card_3_text, command=clicked_card_3, font=font)
card_4 = Button(window, textvariable=card_4_text, command=clicked_card_4, font=font)
instructions = Button(window, text="Instructableaux", command=clicked_instructions, font=font)

# Place starting window items
greeting.grid(column=0, row=0)
start_test.place(x=400,y=200)
long_instructions_fr.grid(column=0,row=1)

# Run application
window.mainloop()