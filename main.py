import random

# import list of words

with open('wordlist.txt', 'r') as word_file:
    wordlist = word_file.read().splitlines()

# ask player for their name and how difficult the game should be (number of letters)

user_name = input("Hi! Let's play hangman. What's your name? ")
user_difficulty = int(input("How long do you want the word to be? "))

# check if length of word is even in the list of words

counter = 1
for word in wordlist:
    if len(word) == user_difficulty:
        break
    counter += 1
    if counter == len(wordlist):
        print("Sorry, our list doesn't have any words of that length!")
        print("Please restart the program and try again.")
        exit()

# choose word of that length from list

appropriate_words = []
for word in wordlist:
    if len(word) == user_difficulty:
        appropriate_words.append(word)

# choose random word from list

word = random.choice(appropriate_words)
print("Let's play hangman!")

# break down word, make a masked list and make function that shows correct guesses

letters = list(word)
masked_letters = letters.copy()
for i, letter in enumerate(masked_letters):
    masked_letters[i] = "*"

guess = ""
interface = ""
finished = False

# print(word)  # for debugging, remove afterwards
# print(letters)  # for debugging, remove afterwards


while not finished:

    for i, letter in enumerate(letters):
        if guess == letters[i]:
            masked_letters[i] = guess

    print(interface.join(masked_letters))  # print out new interface after guess

    for i, letter in enumerate(masked_letters):  # check if the whole word has been guessed yet
        if masked_letters[i] == "*":
            break
        if i == (len(masked_letters) - 1):
            print("Congratulations, you've guessed it!")
            finished = True

    if finished:
        break

    guess = input("Guess a letter: ")
