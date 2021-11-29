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
            return render_template("index.html", error=error)
        else:
            return render_template("index.html", error=error)


if __name__ == '__main__':
    app.run()
