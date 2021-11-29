from flask import Flask, render_template, request, make_response

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
        if error is False:
            response = make_response(render_template("/game"))
            response.set_cookie("user_difficulty", str(difficulty))
            return response
        else:
            return render_template("index.html", error=error)


@app.route("/game", methods=['POST', 'GET'])
def game():
    if request.method == 'GET':
        return render_template("game.html")
    if request.method == 'POST':
        return render_template("game.html")


if __name__ == '__main__':
    app.run()
