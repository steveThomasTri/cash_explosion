from flask import Flask, render_template, jsonify, request
from extractorimagetextcopy import extractor
from database import insert_player, get_endgame, update_endgame_results, verify2, totalwinnings

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

@app.route('/endgameresult')
def endgameresult():
    return render_template("endgameresult.html")

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
    update_endgame_results(data)
    return "Proceed with Care"

@app.route('/verify', methods=['POST'])
def verify():
    return jsonify(v = verify2(request.json))

@app.route('/totalwinnings', methods=['POST'])
def totalwinning():
    return jsonify(total = totalwinnings(request.json))

if __name__ == '__main__':
    app.run(debug=True)