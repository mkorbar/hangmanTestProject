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
        if error:
            return render_template("index.html", error=error)
        else:
            response = make_response(render_template("game.html"))
            response.set_cookie("user_difficulty", str(difficulty))
            return response


@app.route("/game", methods=['POST', 'GET'])
def game():
    if request.method == 'GET':
        return render_template("game.html")
    elif request.method == 'POST':
        return render_template("game.html")


if __name__ == '__main__':
    app.run()
