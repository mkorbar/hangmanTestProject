from flask import Flask, render_template, request, make_response, redirect


import hangman


app = Flask(__name__)


@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        return render_template("index.html")
    elif request.method == 'POST':
        difficulty = int(request.form.get('difficulty'))
        wordlist = hangman.get_wordlist()
        error = hangman.difficulty_check(wordlist, difficulty)
        if error:
            return render_template("index.html", error=error)
        else:
            appropriate_words = hangman.get_appropriate_words(wordlist, difficulty)
            secret_word = hangman.choose_random_word(appropriate_words)
            secret_letters = hangman.word_to_letters(secret_word)
            masked_letters = hangman.mask_word(secret_letters)
            masked_word = "".join(masked_letters)
            response = make_response(render_template("game.html", masked_word=masked_word))
            response.set_cookie("user_difficulty", str(difficulty))
            response.set_cookie("secret_word", secret_word)
            response.set_cookie("masked_word", masked_word)
            return response


@app.route("/game", methods=['POST', 'GET'])
def game():
    if request.method == 'GET':
        return redirect("index.html")
    elif request.method == 'POST':
        guess = request.form.get("guess")
        secret_letters = list(request.cookies.get("secret_word"))
        masked_letters = list(request.cookies.get("masked_word"))
        interface_list = hangman.hangman_guess(secret_letters, masked_letters, guess)
        masked_letters = interface_list.copy()
        masked_word = "".join(masked_letters)
        for letter in masked_letters:
            if letter == "*":
                response = make_response(render_template("game.html", masked_word=masked_word))
                response.set_cookie("masked_word", masked_word)
                return response
            else:
                msg_end = "Congratulations, you've guessed it!"
                response = make_response(render_template("game.html", masked_word=masked_word, msg_end=msg_end))
                return response


if __name__ == '__main__':
    app.run()
