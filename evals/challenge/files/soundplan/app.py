from flask import Flask, jsonify, request

from notes import create_note
from validators import ValidationError

app = Flask(__name__)


@app.errorhandler(ValidationError)
def bad_request(error):
    return jsonify(error=str(error)), 400


@app.post("/notes")
def post_note():
    data = request.get_json()
    return jsonify(create_note(data.get("title"), data.get("body", ""))), 201
