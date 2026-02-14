from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return jsonify({
        "status": "ok",
        "message": "Backend running"
    })

if __name__ == "__main__":
    app.run(debug = True, port = 5000)