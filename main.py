from tkinter import *
from tkinter.font import ITALIC
from turtle import xcor, ycor
import random 
import pandas 

GREEN = "#B1DDC6"

# Flash Cards - - - - - - - - - - - - - - - - - - - - - - - -

try:
    # Check to see if words_to_learn.csv exists
    data = pandas.read_csv("./data/words_to_learn.csv")

except (FileNotFoundError, pandas.errors.EmptyDataError):
    # If file not found, then copy the contents of french_words.csv to new file.
    # If new file exists, check if its empty and if so, copy the contents. 
    with open ("./data/french_words.csv", "r") as all_word_list, open("./data/words_to_learn.csv", "w") as words_to_learn:
        for line in all_word_list:
            words_to_learn.write(line)
    data = pandas.read_csv("./data/words_to_learn.csv")
    
# Convert to a list of dictionaries: 
data_dict = data.to_dict(orient='records')

# Modify the output of the key/value pairs:
translations = [{row["English"]:row["French"]} for row in data_dict]

# Define the words/things so they can be used globally 
english_word = ""
french_word = ""
random_translation = {}

def next_card():
    # Define global variable so it can be used in flip_cards()
    global english_word
    global french_word
    global random_translation

    # Get a random dictionary (which is the translation pair) inside the list 
    random_translation = translations[random.randint(0, len(translations) - 1)]
    
    # Access each word 
    for key, value in random_translation.items():
        english_word = key
        french_word = value

    # Show the language name and word on the card:
    canvas.itemconfig(language_name, text="French")
    canvas.itemconfig(word, text=french_word)

    reset_timer()
    flip_cards_front()

def flip_cards_back():
    global window 
    # Change card image: 
    canvas.itemconfig(front_image, image=card_back_img)

    # Change the words: 
    canvas.itemconfig(language_name, text="English", fill="white")
    canvas.itemconfig(word, text=english_word, fill="white")
    
    reset_timer()
    global change_card_timer
    change_card_timer = window.after(3000, flip_cards_front)

def flip_cards_front():
    global window 
    # Change card image: 
    canvas.itemconfig(front_image, image=card_front_img)
    
    # Change the words: 
    canvas.itemconfig(language_name, text="French", fill="black")
    canvas.itemconfig(word, text=french_word, fill="black")

    reset_timer()
    global change_card_timer
    change_card_timer = window.after(3000, flip_cards_back)
    
def reset_timer():
    global change_card_timer
    window.after_cancel(change_card_timer)

def learn_word():
    # Translation list - words we hit check on

    new_random_translation = {}
    for key, value in random_translation.items():
        new_random_translation['English'] = key
        new_random_translation['French'] = value

    # remove from translations list so it doesn't show up in cards
    translations.remove(random_translation)

    # remove from data_dict and overwrite csv with new data_dict
    data_dict.remove(new_random_translation)
    new_data = pandas.DataFrame(data_dict)
    new_data.to_csv("./data/words_to_learn.csv", index=False)


    
    



# UI Setup - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=GREEN)

change_card_timer = window.after(3000, flip_cards_back)

# Incorrect button 
incorrect_image = PhotoImage(file="./images/newest_x.png")
incorrect_button = Button(image=incorrect_image, highlightthickness=0, highlightbackground=GREEN, fg=GREEN, command=next_card)
incorrect_button.grid(column=0, row=1)

# Correct button 
correct_image = PhotoImage(file="./images/newest_check.png")
correct_button = Button(image=correct_image, highlightthickness=0, highlightbackground=GREEN, fg=GREEN, command=lambda: [learn_word(), next_card()])
correct_button.grid(column=1, row=1)
 
# Canvas
canvas = Canvas(width=800, height=526, bg=GREEN, highlightthickness=0)

card_front_img = PhotoImage(file="./images/card_front.png")
card_back_img = PhotoImage(file="./images/card_back.png")
front_image = canvas.create_image(400, 263, image=card_front_img)
canvas.grid(column=0, row=0, columnspan=2)

language_name = canvas.create_text(400, 150, text="", fill="black", font=("Ariel", 40, "italic"))
word = canvas.create_text(400, 263, text="", fill="black", font=("Ariel", 60, "bold"))

next_card()

window.mainloop()