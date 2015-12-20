__author__ = 'Charles Engen'

import tkinter as tk
from os.path import join, exists
from os import getcwd, makedirs
from random import randint, choice
from math import floor

path_history = join(getcwd(), "History")
path_old_problems = join(path_history, "Problems")

# This is all the output given to our player
output_data = [
    "Welcome to the Arithmetic Test Machine!",
    "What is: %s %s %s = ",
    "Please Enter your answer[Round Down to a whole number]",
    "You answered Correctly",
    "You failed to correctly answer!",
    "Not implemented!"
]

# These are the operators the game works with.
random_problem = [
    "/",
    "+",
    "*",
    "-"
]


class MainGUI(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        # Font Data
        self.font_data_display = ('times', 20)
        self.font_data_menu = ('times', 14)
        # This is the constant difficulty modifier
        self.__mod_diff = 1.35
        # This is the current Difficulty level
        if exists(join(path_history, "difficulty.dif")):
            with open(join(path_history, "difficulty.dif"), 'r') as file:
                file.seek(0)
                for line in file:
                    self.current_difficulty = eval(line.strip('\n'))
        else:
            self.current_difficulty = 5.0
        # This is the current Difficulty level
        if exists(join(path_history, "game_data.bin")):
            self.history = dict()
            with open(join(path_history, "game_data.bin"), 'rb') as file:
                file.seek(0)
                self.history = eval(file.read().decode('utf-8').strip('\n'))
        else:
            self.history = {'correct': 0, 'wrong': 0}

        # This overrides the default behavior of the 'x' out button
        self.protocol('WM_DELETE_WINDOW', self.quit_game)

        # This is the holder for the current answer
        self.__current_answer = 0

        # All the following are for the display
        self.display_area_text_var = tk.StringVar()
        self.question_field_var = tk.StringVar()

        self.main_file_menu = tk.Menu(self)
        self.config(menu=self.main_file_menu)

        self.resizable(width=False, height=False)
        self.geometry('{}x{}'.format(660, 220))

        # Drop-down menu
        self.first_file_menu = tk.Menu(self.main_file_menu, tearoff=0)
        self.sub_ffm_Start = tk.Menu(self.first_file_menu)
        self.main_file_menu.add_cascade(label="File", menu=self.sub_ffm_Start, font=self.font_data_menu)

        self.sub_ffm_Start.add_separator()

        self.sub_ffm_Start.add_command(label="Start Game", command=self.start_game, font=self.font_data_menu)

        self.sub_ffm_Start.add_separator()

        self.sub_ffm_Start.add_command(label="Convert History to CSV",
                                       command=self.convert_history_csv, font=self.font_data_menu)

        self.sub_ffm_Start.add_separator()

        self.sub_ffm_Start.add_command(label="Quit Game", command=self.quit_game, font=self.font_data_menu)
        # End Drop-down

        # Display Text
        self.display_area_text_var.set(output_data[0])

        self.display_area_text = tk.Label(self, textvariable=self.display_area_text_var, font=self.font_data_display)
        self.question_field = tk.Label(self, textvariable=self.question_field_var, font=self.font_data_display)

        self.cur_diff_var = tk.StringVar()
        self.cur_diff = tk.Label(self, textvariable=self.cur_diff_var, font=self.font_data_display)

        self.cur_diff_var.set("Current Difficulty: %s" % self.current_difficulty)

        self.cur_diff.grid(row=4, column=0, sticky='S')

        self.display_area_text.grid(row=0, columnspan=2, sticky='S')
        self.question_field.grid(row=1, columnspan=2, sticky='S')

        self.right_var = tk.StringVar()
        self.right = tk.Label(self, textvariable=self.right_var, font=self.font_data_display)

        self.wrong_var = tk.StringVar()
        self.wrong = tk.Label(self, textvariable=self.wrong_var, font=self.font_data_display)

        self.right.grid(row=5, column=0, sticky='ES')
        self.wrong.grid(row=5, column=1, sticky='WS')
        # End Display

        # Input Entry
        self.input_var = tk.StringVar()
        self.input_entry = tk.Entry(self, textvariable=self.input_var, font=self.font_data_display)
        self.input_entry.grid(row=2, columnspan=2, sticky='S')

        self.input_entry.bind('<Return>', self.check_guess)
        # End Input Entry

    def start_game(self):
        """
        This method starts the game
        """
        self.ask_question()

    def quit_game(self):
        """
        This method controls the quiting of the game.
        """
        try:
            self.save_history()
            self.save_difficulty()
            self.quit()
        except FileNotFoundError:
            self.quit()

    def ask_question(self):
        """
        This method has all the functionality of our question asking.
        """
        self.input_var.set("")
        self.display_area_text_var.set(output_data[2])
        # Sets Question field
        temp_1 = randint(1, int(self.current_difficulty**self.__mod_diff))
        temp_2 = randint(1, int(self.current_difficulty**self.__mod_diff))
        temp_choice = choice(random_problem)
        self.question_field_var.set(output_data[1] % (temp_1, temp_choice, temp_2))
        self.__current_answer = floor(eval("%s%s%s" % (temp_1, temp_choice, temp_2)))
        self.save_problem("[%s, '%s', %s]\n" % (temp_1, temp_choice, temp_2))
        self.display_area_text_var.set(output_data[2])

    def check_guess(self, *args):
        """
        This method checks the players guess.
        :param args: This argument is only to catch what tkinter passes to this method.
        """
        try:
            self.input_var.set(self.input_entry.get())
            if self.__current_answer == int(self.input_var.get()):
                self.input_var.set(output_data[3])
                self.current_difficulty += 0.1
                self.history['correct'] += 1
                self.save_history()
                self.save_difficulty()
            else:
                self.input_var.set(output_data[4])
                self.current_difficulty -= 0.1

                self.history['wrong'] += 1
            self.after(250, self.ask_question)
        except ValueError:
            pass
        self.cur_diff_var.set("Current Difficulty: %s, Max:%s"
                              % ("{0:.1f}".format(self.current_difficulty),
                                 int(self.current_difficulty**self.__mod_diff)-1))
        self.right_var.set("Correct: %s" % self.history['correct'])
        self.wrong_var.set("Wrong: %s" % self.history['wrong'])

    def save_history(self):
        """
        This method saves the game history.
        """
        if exists(path_history):
            with open(join(path_history, "game_data.bin"), 'wb') as file:
                file.write(str(self.history).encode('utf-8'))
        else:
            makedirs(path_history)
            self.save_history()

    def save_problem(self, data):
        """
        This method saves the problem as they are done.
        :param data: pass the problem to be saved, has to be in the format of
            [int(), operator, int()]
        """
        if exists(path_old_problems):
            with open(join(path_old_problems, "problems.txt"), "a+") as file:
                file.write(str(data))
        else:
            makedirs(path_old_problems)
            self.save_problem(data)

    def save_difficulty(self):
        """
        This method saves the game difficulty level.
        """
        if exists(path_history):
            with open(join(path_history, "difficulty.dif"), "w+") as file:
                file.write(str(self.current_difficulty))
        else:
            makedirs(path_history)
            self.save_difficulty()

    def convert_history_csv(self):
        """
        Yet to be implemented.
        """
        self.display_area_text_var.set(output_data[5])
        pass


if __name__ == "__main__":
    root = MainGUI()
    root.mainloop()