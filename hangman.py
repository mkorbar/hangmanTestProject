import random


# define writing file if you need one

def write_to_score_file(name, chosen_word, guesses):
    with open('hangman_scores.txt', 'a') as score_file:
        score_file.write(f"{name} {chosen_word} {str(guesses)}")


# HANGMAN GAME FUNCTION


# import list of words
def get_wordlist():
    with open('wordlist.txt', 'r') as word_file:
        wordlist = word_file.read().splitlines()
        return wordlist


# check if length of word is even in the list of words
def difficulty_check(wordlist, user_difficulty):
    if user_difficulty < 4:
        return "Please choose a length of 4 letters or more"
    else:
        for counter, word in enumerate(wordlist, start=1):
            if len(word) == user_difficulty:
                return False
            counter += 1
            if counter == len(wordlist):
                return "Sorry, our list doesn't have any words of that length"


# choose word of that length from list
def get_appropriate_words(wordlist, user_difficulty):
    appropriate_words = []
    for word in wordlist:
        if len(word) == user_difficulty:
            appropriate_words.append(word)
    return appropriate_words


# choose random word and make it a list
def choose_random_word(appropriate_words):
    word = random.choice(appropriate_words)
    letters = list(word)
    return letters


# break down word, make a masked list
def mask_word(letters):
    masked_letters = letters.copy()
    for i, letter in enumerate(masked_letters):
        masked_letters[i] = "*"
    return masked_letters


# what happens when user guesses
def hangman_guess(letters, masked_letters, guess):
    interface = ""
    for i, letter in enumerate(letters):
        if guess == letters[i]:
            masked_letters[i] = guess
    return interface.join(masked_letters)  # print out new interface after guess


# check if entire word has been guessed yet
def hangman_check(masked_letters):
    finished = False
    for i, letter in enumerate(masked_letters):
        if masked_letters[i] == "*":
            break
        if i == (len(masked_letters) - 1):
            finished = True
        return finished
