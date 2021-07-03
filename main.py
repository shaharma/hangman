from hangman_photos import HANGMAN_PHOTOS
import re
import random


def welcome_screen():
    HANGMAN_ASCII_ART = """Welcome to the game Hangman!!\n
      _    _                                         
     | |  | |                                        
     | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __  
     |  __  |/ _` | '_ \ / _` | '_ ` _ \ / _` | '_ \ 
     | |  | | (_| | | | | (_| | | | | | | (_| | | | |
     |_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                          __/ |                      
                         |___/\n"""
    MAX_TRIES = 6
    print(HANGMAN_ASCII_ART, "You have got " + str(MAX_TRIES) + " tries\n")


def print_hangman(num_of_tries):
    for i in HANGMAN_PHOTOS:
        if str(num_of_tries) in i:
            return HANGMAN_PHOTOS[i]
    if str(num_of_tries) not in i:
        return "Better luck next time"


def choose_word(file_path, index):
    my_list = []
    edit_list = []
    file_input = open(file_path, "r")
    for line in file_input:
        words = line.split(" ")
        edit_list += words
    for i in edit_list:
        if i not in my_list:
            my_list.append(i)

    if index >= len(edit_list):
        edit_list += edit_list * index
    secret_word = edit_list[index]
    return secret_word


def show_hidden_word(secret_word, old_letters_guessed):
    for i in range(len(secret_word)):
        if secret_word[i] not in old_letters_guessed:
            secret_word = secret_word.replace(secret_word[i], "_")
    secret_word = " ".join(secret_word)
    return secret_word


def check_win(secret_word, old_letters_guessed):
    if "_" in show_hidden_word(secret_word, old_letters_guessed):
        return False
    else:
        return True


def check_valid_input(letter_guessed, old_letters_guessed):
    if len(letter_guessed) >= 2:
        return False
    elif not re.search('[a-zA-Z]', letter_guessed):
        return False
    elif (letter_guessed.lower() or letter_guessed.upper()) in old_letters_guessed:
        return False
    else:
        return True


def try_update_letter_guessed(letter_guessed, old_letters_guessed):
    if check_valid_input(letter_guessed, old_letters_guessed) is True:
        old_letters_guessed.append(letter_guessed)
        return True
    elif check_valid_input(letter_guessed, old_letters_guessed) is False:
        str1 = " -> ".join(old_letters_guessed)
        print("X\n" + str1)
        return False


def get_file_length(file_location):
    file = open(file_location, "rt")
    data = file.read()
    words = data.split()
    return len(words)


def main():
    red = lambda text: '\033[0;31m' + text + '\033[0m'
    green = lambda text: '\033[0;32m' + text + '\033[0m'
    cyan = lambda text: '\033[0;36m' + text + '\033[0m'

    old_letters_guessed = []
    num_of_tries = 1
    MAX_TRIES = 6
    randomize_index = random.randint(1, get_file_length("words_for_hangman.txt"))
    secret_word = choose_word("words_for_hangman.txt", randomize_index)
    welcome_screen()
    print("Please choose a file directory with words and a certain index!")
    print("\n")
    print("This is your hangman status, your first try:")
    print(print_hangman(num_of_tries))
    print("First hint: ")
    print(show_hidden_word(secret_word, old_letters_guessed))

    for i in range(MAX_TRIES):
        input_game = input("Please enter a valid char:")

        if try_update_letter_guessed(input_game, old_letters_guessed) is True and input_game in secret_word:
            print(show_hidden_word(secret_word, old_letters_guessed))
            num_of_tries += 1
            if check_win(secret_word, old_letters_guessed) is True:
                print(green("YOU WIN"))
            else:
                pass
        else:
            num_of_tries += 1
            try_update_letter_guessed(input_game, old_letters_guessed)
            print(print_hangman(num_of_tries))
            if check_win(secret_word, old_letters_guessed) is False and num_of_tries >= 7:
                print(red("YOU LOSE"))
                print("Secret word is...... " + cyan(secret_word))
            else:
                pass


if __name__ == '__main__':
    main()
