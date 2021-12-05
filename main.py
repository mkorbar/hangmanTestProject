from flask import Flask, render_template, request, make_response, redirect
# from flask_sqlalchemy import SQLAlchemy
from sqla_wrapper import SQLAlchemy

import hangman
import os
import hashlib
import uuid
import datetime


app = Flask(__name__)

# the replace method is needed due to this issue:
# https://help.heroku.com/ZKNTJQSK/why-is-sqlalchemy-1-4-x-not-connecting-to-heroku-postgres

db_url = os.getenv("DATABASE_URL", "sqlite:///db.sqlite").replace("postgres://", "postgresql://", 1)
db = SQLAlchemy(db_url)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String, unique=True)
    user_email = db.Column(db.String, unique=True)
    user_password = db.Column(db.String, unique=False)
    session_token = db.Column(db.String, unique=True)
    session_word = db.Column(db.String, unique=False)


db.create_all()


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    elif request.method == 'POST':
        user_name = request.form.get("user_name")
        user_email = request.form.get("user_email")
        user_password = request.form.get("user_password")
        hashed_password = hashlib.sha256(user_password.encode()).hexdigest()

        user = User.query.filter_by(user_email=user_email).first()

        if not user:
            user = User(user_name=user_name, user_email=user_email, user_password=hashed_password)
            message = "New user created!"
        else:
            if user.user_password != hashed_password:
                return render_template("/login.html", error="Password is incorrect")
            if user.user_name != user_name:
                return render_template("/login.html", error="Username is incorrect")
            else:
                message = "Welcome back!"

        user.session_token = str(uuid.uuid4())
        db.session.add(user)
        db.session.commit()

        response = make_response(render_template('/index.html', message=message))
        response.set_cookie(
            'session_token', user.session_token, expires=(datetime.datetime.now() + datetime.timedelta(days=1))
        )
        return response


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
            guess_list = ""

            response = make_response(render_template("game.html", masked_word=masked_word))
            response.set_cookie("user_difficulty", str(difficulty))
            response.set_cookie("masked_word", masked_word)
            response.set_cookie("guess_list", guess_list)

            session_token = request.cookies.get("session_token")

            if not session_token:
                response.set_cookie("secret_word", secret_word)

            else:
                user = User.query.filter_by(session_token=session_token).first()
                user.session_word = secret_word
                db.session.add(user)
                db.session.commit()

            return response


@app.route("/game", methods=['POST', 'GET'])
def game():
    if request.method == 'GET':
        return redirect("index.html")
    elif request.method == 'POST':
        guess = request.form.get("guess")
        masked_letters = list(request.cookies.get("masked_word"))
        guess_list = request.cookies.get("guess_list")
        guess_list += guess
        print_guess_list = list(guess_list)

        session_token = request.cookies.get("session_token")

        if not session_token:
            secret_letters = list(request.cookies.get("secret_word"))

        else:
            user = User.query.filter_by(session_token=session_token).first()
            secret_letters = list(user.session_word)

        interface_list = hangman.hangman_guess(secret_letters, masked_letters, guess)
        masked_letters = interface_list.copy()
        masked_word = "".join(masked_letters)
        for letter in masked_letters:
            if letter == "*":
                response = make_response(render_template("game.html",
                                                         masked_word=masked_word,
                                                         guesses=print_guess_list))
                response.set_cookie("masked_word", masked_word)
                response.set_cookie("guess_list", guess_list)
                return response

        msg_end = "Congratulations, you've guessed it!"
        response = make_response(render_template("game.html",
                                                 masked_word=masked_word,
                                                 guesses=print_guess_list,
                                                 msg_end=msg_end))
        return response


if __name__ == "__main__":
    app.run(use_reloader=True)
