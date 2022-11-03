from tkinter import *
from tkinter import messagebox
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"
LOWER_MEDIAN_CHANCE = 0.7
DATA_PATH = "./data/german_words.csv"
LANGUAGE = "German"


class FlashCard(Tk):

    def __init__(self):
        super(FlashCard, self).__init__()
        self.data_model = DataModel(self)

        self.title("Flashy Flashcards")
        self.config(padx=60, pady=60, bg=BACKGROUND_COLOR)

        right_button_image = PhotoImage(file='./images/right.png')
        wrong_button_image = PhotoImage(file='./images/wrong.png')
        self.__flashcard_front_image = PhotoImage(file='./images/card_front.png')
        self.__flashcard_back_image = PhotoImage(file='./images/card_back.png')
        self.is_front = True

        self.right_button = Button(image=right_button_image, highlightthickness=0, command=self.print_next_card)
        self.wrong_button = Button(image=wrong_button_image, highlightthickness=0, command=self.flip_card)

        self.flashcard = Canvas(self, width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
        self.flashcard_image = self.flashcard.create_image(0, 0, image=self.__flashcard_front_image, anchor='nw')
        self.top_text = self.flashcard.create_text(400, 150, text=LANGUAGE, font=("Ariel", 40, "italic"))
        self.bottom_text = self.flashcard.create_text(400, 263, text=self.data_model.get_german_word(),
                                                      font=("Ariel", 60, "bold"))
        self.timer_text = self.flashcard.create_text(50, 50, text="", font=("Ariel", 30))

        self.flashcard.grid(row=0, column=0, columnspan=2)
        self.wrong_button.grid(row=1, column=0)
        self.right_button.grid(row=1, column=1)

        menubar = Menu(self)
        self.config(menu=menubar)
        file_menu = Menu(menubar)
        file_menu.add_command(label="Clear Scores", command=self.clear_scores_prompt)
        menubar.add_cascade(label="File", menu=file_menu)

        self.mainloop()

    def print_next_card(self):
        if self.is_front:
            self.data_model.save_score(1)
        self.data_model.randomize_word()
        self.flashcard.itemconfig(self.flashcard_image, image=self.__flashcard_front_image)
        self.flashcard.itemconfig(self.top_text, text=LANGUAGE, fill='#000')
        self.flashcard.itemconfig(self.bottom_text, text=self.data_model.get_german_word(), fill='#000')
        self.is_front = True

    def flip_card(self):
        if self.is_front:
            self.data_model.save_score(-1)
        self.flashcard.itemconfig(self.flashcard_image, image=self.__flashcard_back_image)
        self.flashcard.itemconfig(self.top_text, text="English", fill='#fff')
        self.flashcard.itemconfig(self.bottom_text, text=self.data_model.get_english_word(), fill='#fff')
        self.is_front = False

    def clear_scores_prompt(self):
        answer = messagebox.askyesno("Clear Scores",
                                     "Would you like to clear your scores? This action cannot be reversed.")
        if answer:
            self.data_model.clear_scores()


class DataModel:

    def __init__(self, ui: FlashCard):
        self.ui = ui

        self.data = pd.read_csv(DATA_PATH)
        self.__current_word = self.data[LANGUAGE].sample().values[0]
        if "Score" not in self.data:
            self.data["Score"] = 0

    def get_german_word(self) -> str:
        return self.__current_word

    def get_english_word(self) -> str:
        try:
            return self.data.loc[self.data[LANGUAGE] == self.__current_word]["English"].iloc[0].lower()
        except KeyError:
            return "KeyError"
        except IndexError:
            return "IndexError"

    def randomize_word(self):
        if random.random() <= LOWER_MEDIAN_CHANCE:
            # DEBUG: print(f"lower median word, median = {self.data['Score'].median()}")
            self.__current_word = (self.data.loc[self.data["Score"] <= self.data["Score"].median(), LANGUAGE]
                                   .sample().values[0])
        else:
            # DEBUG: print("true random")
            self.__current_word = self.data[LANGUAGE].sample().values[0]

    def save_score(self, x: int):
        # DEBUG: print(f"giving word {self.__current_word} a score of {x}")
        self.data.loc[self.data[LANGUAGE] == self.__current_word, "Score"] += x
        self.data.to_csv(DATA_PATH, index=False)
        words_to_learn = self.data.loc[self.data["Score"] < self.data["Score"].median()]
        words_to_learn.to_csv("./data/to_learn.csv", index=False)

    def clear_scores(self):
        self.data["Score"] = 0
        self.data.to_csv(DATA_PATH, index=False)


def main():
    FlashCard()


if __name__ == '__main__':
    main()
