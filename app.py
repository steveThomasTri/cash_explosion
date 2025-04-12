from flask import Flask, render_template, jsonify, request
from extractorimagetextcopy import extractor
from database import insert_player, get_endgame

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/splash')
def splash():
    return render_template("splash.html")

@app.route('/endgame')
def endgame():
    return render_template("endgame.html")

@app.route('/about')
def about():
    return 'This is the about page'

@app.route('/profile/<username>')
def profile(username):
    return f'This is the profile page for {username}'

@app.route('/getname', methods=['GET'])
def getName():
    return jsonify(message=extractor())

@app.route("/data", methods=["POST"])
def insert_data():
    data = request.json
    insert_player(data)
    return 'This is the about page'

@app.route("/endgamedata", methods=["POST"])
def end_game_data():
    data = request.json
    return jsonify(players = get_endgame(data))

@app.route("/endgameresults", methods=["POST"])
def end_game_results():
    data = request.json
    return data

if __name__ == '__main__':
    app.run(debug=True)