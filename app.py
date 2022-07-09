from boggle import Boggle
from flask import Flask, jsonify, render_template, request, session
from flask_debugtoolbar import DebugToolbarExtension

boggle_game = Boggle()

app = Flask(__name__)
app.config['SECRET_KEY'] = "supasecret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

@app.route('/')
def default_route():
    initializeSession()
    return render_template("board.html", board=session["board"], plays=session["plays"], highscore=session["highscore"])

@app.route('/guess/<word>')
def guess_word(word):
    """handles when a word is guessed and returns a string based on that word
        - ok - the word was found in the table, dictionary, and is unique
        - repeat - the word has already been found in a prior guess
        - not-word - the word wasn't found in the dictionary
        - not-on-board - the word wasn't found on the table but was found in the dictionary
    """
    result = boggle_game.check_valid_word(session["board"], word)
    if result == "ok":
        if word in session["words"]:
            result = "repeat"
        updateWords(word)
    return jsonify(result)

@app.route('/complete', methods=["post"])
def finish_game():
    """updates the counter for games played that session, """
    score = request.json["scored"]
    session["plays"] = session["plays"] + 1
    if score > session["highscore"]:
        session["highscore"] = score
    return "ok" 

def initializeSession():
    """builds a new board and zeroes or updates the session variables"""
    session["board"] = boggle_game.make_board()
    session["plays"] = session.get("plays", 0)
    session["highscore"] = session.get("highscore", 0)
    session["words"] = []

def updateWords(word):
    """tracks correctly guessed words to avoid repeat guesses"""
    updated_words = session["words"]
    updated_words.append(word)
    session["words"] = updated_words