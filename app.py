from flask import Flask, render_template, jsonify, request
from extractorimagetextcopy import extractor
from database import insert_player

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

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

if __name__ == '__main__':
    app.run(debug=True)