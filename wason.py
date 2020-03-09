from tkinter import Tk, Label, Button, Frame, messagebox, StringVar, Canvas, Radiobutton, IntVar, Entry, BOTH, TRUE
from PIL.ImageTk import PhotoImage
from PIL import Image
from datetime import datetime
from os import listdir
from os.path import isfile, join

class WasonAppGUI:
    # TODO: time measurement overall
    # TODO: time measurement for each question
    def __init__(self, master):
        self.master = master
        self.master.geometry("800x600")
        master.title("Wason Selection Task")
        self.questions_folder = "./images/"
        self.question_index = 0
        self.questions_total = 0
        self.questions_text = []
        self.current_question_text = StringVar()
        self.current_question_index_text = StringVar()
        self.answer_1_radio = StringVar()
        self.answer_2_radio = StringVar()
        self.answer_3_radio = StringVar()
        self.answer_4_radio = StringVar()
        self.answer_5_radio = StringVar()
        self.answer_6_radio = StringVar()
        self.selected_answer = IntVar()
        self.question_image = Image.new('RGB',(0,0))
        self.question_image_pil = PhotoImage(self.question_image)
        self.questions_image_file = []
        self.load_questions()
        self.answers = [0] * len(self.questions_text)
        self.first_name = ""
        self.last_name = ""
        self.time_total = 0
        self.time_average_per_question = 0
        self.time_per_question = [0] * len(self.questions_text)
        self.font = ('Helvetica', 20)

        # Create intro frame
        self.intro_frame = Frame(self.master)
        self.intro_frame.pack()
        self.intro_label = Label(self.intro_frame, text="Welcome!", font=self.font)
        self.intro_label.grid(row=0, column = 1)

        self.first_name_label = Label(self.intro_frame, text="First name", font=self.font)
        self.first_name_label.grid(row=1, column=0)
        self.last_name_label = Label(self.intro_frame, text="Last name", font=self.font)
        self.last_name_label.grid(row=2, column=0)

        self.first_name_entry = Entry(self.intro_frame, text="First name", font=self.font)
        self.first_name_entry.grid(row=1, column=1)
        self.last_name_entry = Entry(self.intro_frame, text="Last name", font=self.font)
        self.last_name_entry.grid(row=2, column=1)

        self.greet_button = Button(self.intro_frame, text="Greet", command=self.greet, font=self.font)
        self.greet_button.grid(row=3, column=1)

        self.start_button = Button(self.intro_frame, text="Start", command=self.clicked_start, font=self.font)
        self.start_button.grid(row=4, column=1)

        self.close_button = Button(self.intro_frame, text="Close", command=master.quit, font=self.font)
        self.close_button.grid(row=5, column=1)

        # Create question frame
        self.question_frame = Frame(self.master)
        self.q_text_label = Label(self.question_frame, textvariable=self.current_question_text, font=self.font)
        self.q_text_label.pack()

        self.q_cards_canvas = Canvas(self.question_frame, width=800, height=400)
        self.q_cards_canvas.pack(fill=BOTH, expand=TRUE)
        self.q_image_on_canvas = self.q_cards_canvas.create_image(400, 200, image = PhotoImage(self.question_image))

        self.q_answers_frame = Frame(self.question_frame)
        self.q_answers_frame.pack()
        self.answer_1_radio = Radiobutton(self.q_answers_frame, text="1 & 2", variable = self.selected_answer, 
                                            value=1, command=self.clicked_answer, font=self.font)
        self.answer_2_radio = Radiobutton(self.q_answers_frame, text="1 & 3", variable = self.selected_answer, 
                                            value=2, command=self.clicked_answer, font=self.font)
        self.answer_3_radio = Radiobutton(self.q_answers_frame, text="1 & 4", variable = self.selected_answer, 
                                            value=3, command=self.clicked_answer, font=self.font)
        self.answer_4_radio = Radiobutton(self.q_answers_frame, text="2 & 3", variable = self.selected_answer, 
                                            value=4, command=self.clicked_answer, font=self.font)
        self.answer_5_radio = Radiobutton(self.q_answers_frame, text="2 & 4", variable = self.selected_answer, 
                                            value=5, command=self.clicked_answer, font=self.font)
        self.answer_6_radio = Radiobutton(self.q_answers_frame, text="3 & 4", variable = self.selected_answer, 
                                            value=6, command=self.clicked_answer, font=self.font)
        self.answer_1_radio.grid(row=0, column=0)
        self.answer_2_radio.grid(row=1, column=0)
        self.answer_3_radio.grid(row=2, column=0)
        self.answer_4_radio.grid(row=0, column=1)
        self.answer_5_radio.grid(row=1, column=1)
        self.answer_6_radio.grid(row=2, column=1)

        self.q_buttons_frame = Frame(self.question_frame)
        self.q_buttons_frame.pack()
        self.previous_button = Button(self.q_buttons_frame, text="Previous", command=self.clicked_previous, font=self.font)
        self.previous_button.grid(row=0, column=0)
        self.q_count_label = Label(self.q_buttons_frame, textvariable=self.current_question_index_text, font=self.font)
        self.q_count_label.grid(row=0, column=1)
        self.next_button = Button(self.q_buttons_frame, text="Next", command=self.clicked_next, font=self.font)
        self.next_button.grid(row=0, column=2)

        # End frame
        self.end_frame = Frame(self.master)
        self.end_label = Label(self.end_frame, text="Test finished! Well done! \n \
                                You can press BACK and review your answers or FINISH the test.", font=self.font)
        self.end_label.pack()
        self.end_buttons_frame = Frame(self.end_frame)
        self.end_buttons_frame.pack()
        self.back_button = Button(self.end_buttons_frame, text="BACK", command=self.clicked_previous, font=self.font)
        self.back_button.grid(row=0, column=0)
        self.end_label = Label(self.end_buttons_frame, text="", font=self.font)
        self.end_label.grid(row=0, column=1)
        self.end_button = Button(self.end_buttons_frame, text="FINISH", command=self.clicked_finish, font=self.font)
        self.end_button.grid(row=0, column=2)

    def clicked_finish(self):
        now = datetime.now()
        file = open("./results/{}_{}_{} \r\n".format(now.strftime("%Y_%m_%d_%H_%M_%S"), self.last_name, self.first_name),"w+")
        file.write("{} {} \r\n".format(self.first_name, self.last_name))
        file.write("Date: {} \r\n".format(now.strftime("%d.%m.%Y, %H:%M:%S")))
        file.write("Total time: {} seconds \r\n".format(self.time_total))
        file.write("Average time per question: {} seconds \r\n".format(self.time_average_per_question))
        for index in range(self.questions_total):
            file.write("Question {}: Answer {}, Time {} seconds \r\n".format(index, self.answers[index], 
                                                                            self.time_per_question[index]))
        file.close()
        self.master.quit()

    def clicked_answer(self):
        self.answers[self.question_index] = self.selected_answer.get()

    def clicked_start(self):
        self.question_index = 0
        self.first_name = self.first_name_entry.get()
        self.last_name = self.last_name_entry.get()
        self.update_question_frame()
        self.intro_frame.pack_forget()
        self.question_frame.pack()

    def clicked_next(self):
        self.question_index = min(self.questions_total, self.question_index+1)
        if self.question_index == self.questions_total:
            self.question_frame.pack_forget()
            self.end_frame.pack()
        else:
            self.update_question_frame()

    def clicked_previous(self):
        if self.question_index == self.questions_total:
            self.question_frame.pack()
            self.end_frame.pack_forget()
        self.question_index = max(0, self.question_index-1)
        self.update_question_frame()

    def update_question_frame(self):
        self.selected_answer.set(self.answers[self.question_index])
        #self.current_question_text.set(self.questions_text[self.question_index])
        if self.question_index == 0:
            self.current_question_text.set("Example question:")
        else:
            self.current_question_text.set("Question {}".format(self.question_index))
        self.current_question_index_text.set("Question {} / {}".format(self.question_index,self.questions_total-1))
        self.question_image = Image.open(self.questions_image_file[self.question_index])
        self.question_image = self.question_image.resize((800,400))
        self.question_image.show()
        self.question_image_pil = PhotoImage(self.question_image)
        self.q_cards_canvas.itemconfig(self.q_image_on_canvas, image=self.question_image_pil)

    def greet(self):
        print("Greetings!")

    def load_questions(self):
        # Dummy questions
        self.questions_text.append("How was your day?")
        self.questions_text.append("Wie war dein Tag?")
        self.questions_text.append("Como estas tu dia?")
        self.questions_text.append("Cum a fost astazi?")
        self.questions_text.append("Comment ca va?")

        # Dummy images
        self.questions_image_file = [self.questions_folder + f for f in listdir(self.questions_folder) if isfile(join(self.questions_folder, f)) and f.split('.')[-1] == "jpg"]
        self.questions_image_file.sort()
        #self.questions_image_file.append("./images/00000.jpg")
        #self.questions_image_file.append("./images/00001.jpg")
        #self.questions_image_file.append("./images/00002.jpg")
        
        self.questions_total = len(self.questions_text)

if __name__ == "__main__":
    root = Tk()
    wason_app = WasonAppGUI(root)
    root.mainloop()