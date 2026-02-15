# Imports
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

# Custom imports
import scraper
import bias
import media

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

@app.route("/fetch-audio", methods=["POST"])
def fetch_audio():
    if "file" not in request.files:
        return jsonify({"status": "error", "message": "No file provided"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"status": "error", "message": "No file selected"}), 400

    filename = file.filename
    save_path = os.path.join(os.path.dirname(__file__), "user_downloads", filename)
    file.save(save_path)

    try:
        text = media.audio_to_text(filename)
        if text.startswith("Error:"):
            return jsonify({"status": "error", "message": text}), 500

        paragraphs = bias.segment_paragraphs(text)
        paragraphs_json = [
            {
                "text": para.text,
                "bias_score": para.bias_score,
                "unbiased_replacement": para.unbiased_replacement,
                "reason_biased": para.reason_biased
            }
            for para in paragraphs
        ]
        return jsonify({"status": "ok", "data": {"text": text, "paragraphs": paragraphs_json}}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/convert-audio", methods=["POST"])
def convert_audio():
    data = request.get_json()
    filename = data.get("filename")
    
    if not filename:
        return jsonify({
            "status": "error",
            "message": "Filename not provided"
        }), 400
    
    try:
        text = media.audio_to_text(filename)
        return jsonify({
            "status": "success",
            "text": text
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    app.run(debug = True, port = 5000)