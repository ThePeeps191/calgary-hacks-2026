# Imports
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

# Custom imports
import scraper
import bias
import media
from metrics import get_drama_index

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

    # Segment text into paragraphs and analyze bias
    paragraphs = bias.segment_paragraphs(text)

    # Convert paragraphs to JSON representation
    paragraphs_json = []
    reasons = []
    for para in paragraphs:
        paragraphs_json.append({
            "text": para.text,
            "bias_score": para.is_text_biased_enough,
            "unbiased_replacement": para.unbiased_replacement,
            "reason_biased": para.reason_biased
        })
        if para.is_text_biased_enough and para.reason_biased:
            reasons.append(para.reason_biased)

    # Calculate drama index as the bias_score
    try:
        bias_score = get_drama_index(text)
    except Exception:
        bias_score = None

    return jsonify({
        "status": "ok",
        "data": {
            "paragraphs": paragraphs_json,
            "bias_score": bias_score,
            "authors": content.get("authors", []),
            "date": content.get("date", ""),
            "top_image": content.get("top_image", ""),
            "summary": content.get("summary", ""),
            "keywords": content.get("keywords", []),
            "reasons": reasons
        }
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
        paragraphs_json = []
        reasons = []
        for para in paragraphs:
            paragraphs_json.append({
                "text": para.text,
                "bias_score": para.is_text_biased_enough,
                "unbiased_replacement": para.unbiased_replacement,
                "reason_biased": para.reason_biased
            })
            if para.is_text_biased_enough and para.reason_biased:
                reasons.append(para.reason_biased)

        # Calculate drama index as the bias_score
        try:
            bias_score = get_drama_index(text)
        except Exception:
            bias_score = None

        return jsonify({
            "status": "ok",
            "data": {
                "text": text,
                "paragraphs": paragraphs_json,
                "bias_score": bias_score,
                "summary": text,
                "reasons": reasons
            }
        }), 200
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
            "status": "ok",
            "text": text
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
    
@app.route("/fetch-video", methods=["POST"])
def fetch_video():
    data = request.get_json()
    if not data or "url" not in data:
        return jsonify({"status": "error", "message": "No YouTube URL provided"}), 400

    url = data["url"].strip()
    if not url:
        return jsonify({"status": "error", "message": "Empty URL"}), 400

    downloads_dir = os.path.join(os.path.dirname(__file__), "user_downloads")
    os.makedirs(downloads_dir, exist_ok=True)

    try:
        import yt_dlp

        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": os.path.join(downloads_dir, "%(id)s.%(ext)s"),
            "quiet": True,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_id = info["id"]

        audio_filename = f"{video_id}.wav"
        audio_path = os.path.join(downloads_dir, audio_filename)

        text = media.audio_to_text(audio_filename)
        if not text or text.startswith("Error:"):
            return jsonify({"status": "error", "message": text}), 500

        paragraphs = bias.segment_paragraphs(text)
        paragraphs_json = [
            {
                "text": para.text,
                "bias_score": getattr(para, "is_text_biased_enough", None),
                "unbiased_replacement": getattr(para, "unbiased_replacement", None),
                "reason_biased": getattr(para, "reason_biased", None),
            }
            for para in paragraphs
        ]

        return jsonify({
            "status": "ok",
            "data": {
                "text": text,
                "paragraphs": paragraphs_json
            }
        }), 200

    except Exception as e:
        print("FETCH VIDEO ERROR:", e)
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/get-drama-index", methods=["POST"])
def get_drama_index_route():
    data = request.get_json()
    text = data.get("text")
    
    if not text:
        return jsonify({
            "status": "error",
            "message": "Text not provided"
        }), 400
    
    try:
        drama_index = get_drama_index(text)
        return jsonify({
            "status": "success",
            "drama_index": drama_index
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    app.run(debug = True, port = 5000)
