from flask import Flask, render_template, jsonify, request
from extractorimagetextcopy import extractor
from database import insert_player, get_endgame, update_endgame_results, verify2, totalwinnings, cities, county, weekdata, numbers

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

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/testdashboard")
def testdashboard():
    return render_template("testdashboard.html")

@app.route("/countymap")
def countymap():
    return render_template("countymapcopy.html")

@app.route("/weeklywinnings")
def weeklydata():
    return render_template("timegraph.html")

@app.route("/numbers")
def number():
    return render_template("numbergrid.html")

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

@app.route('/citydata')
def citydata():
    return jsonify(cities())

@app.route("/countydata")
def countydata():
    return jsonify(county())

@app.route("/weeklydata")
def weekldata():
    return jsonify(weekdata())

@app.route("/numberdata")
def numberdata():
    return jsonify(numbers())

if __name__ == '__main__':
    app.run(debug=True)