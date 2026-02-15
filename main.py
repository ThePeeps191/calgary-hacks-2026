# Imports
from flask import Flask, request, jsonify
from flask_cors import CORS

# Scraper imports
import scraper

app = Flask(__name__)
CORS(app)

@app.route("/fetch-url", methods=["POST"])
def fetch_url():
    data = request.get_json()
    url = data.get("url")
    
    if not url:
        return jsonify({
            "status": "error",
            "message": "URL not provided"
        }), 400
    
    try:
        content = scraper.get_content(url)
        return jsonify({
            "status": "ok",
            "data": content
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    app.run(debug = True, port = 5000)