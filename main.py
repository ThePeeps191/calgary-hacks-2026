# Imports
from flask import Flask, request, jsonify
from flask_cors import CORS

# Scraper imports
import scraper
import bias

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
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
    
    text = content['text']
    
    # Segment text into paragraphs
    paragraphs = bias.segment_paragraphs(text)
    
    # Convert paragraphs to JSON representation
    paragraphs_json = []
    for para in paragraphs:
        paragraphs_json.append({
            "text": para.text,
            "bias_score": para.bias_score,
            "unbiased_replacement": para.unbiased_replacement,
            "reason_biased": para.reason_biased
        })
    
    return jsonify({
        "status": "success",
        "paragraphs": paragraphs_json
    }), 200

if __name__ == "__main__":
    app.run(debug = True, port = 5000)