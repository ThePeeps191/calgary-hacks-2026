# Imports
from flask import Flask, request, jsonify
from flask_cors import CORS

# Scraper imports
import scraper

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>URL Content Fetcher</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }
            .container {
                background: white;
                border-radius: 10px;
                box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
                padding: 40px;
                max-width: 600px;
                width: 100%;
            }
            h1 {
                color: #333;
                margin-bottom: 30px;
                text-align: center;
            }
            .input-group {
                display: flex;
                gap: 10px;
                margin-bottom: 20px;
            }
            input[type="text"] {
                flex: 1;
                padding: 12px;
                border: 2px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
                transition: border-color 0.3s;
            }
            input[type="text"]:focus {
                outline: none;
                border-color: #667eea;
            }
            button {
                padding: 12px 30px;
                background: #667eea;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                cursor: pointer;
                transition: background 0.3s;
            }
            button:hover {
                background: #5568d3;
            }
            button:disabled {
                background: #ccc;
                cursor: not-allowed;
            }
            .loading {
                display: none;
                text-align: center;
                margin: 30px 0;
            }
            .spinner {
                border: 4px solid #f3f3f3;
                border-top: 4px solid #667eea;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                animation: spin 1s linear infinite;
                margin: 0 auto;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            .result {
                margin-top: 30px;
                padding: 20px;
                background: #f9f9f9;
                border-radius: 5px;
                display: none;
                max-height: 400px;
                overflow-y: auto;
            }
            .result h2 {
                color: #667eea;
                margin-bottom: 15px;
                font-size: 18px;
            }
            .result p {
                color: #555;
                line-height: 1.6;
                font-size: 14px;
            }
            .error {
                color: #e74c3c;
                padding: 15px;
                background: #fdeaea;
                border-radius: 5px;
                margin-top: 20px;
                display: none;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📰 URL Content Fetcher</h1>
            <div class="input-group">
                <input type="text" id="urlInput" placeholder="Paste your URL here..." />
                <button onclick="fetchContent()">Fetch</button>
            </div>
            
            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p>Loading...</p>
            </div>
            
            <div class="error" id="error"></div>
            
            <div class="result" id="result">
                <h2>Article Content</h2>
                <p id="contentText"></p>
            </div>
        </div>

        <script>
            function fetchContent() {
                const url = document.getElementById('urlInput').value.trim();
                
                if (!url) {
                    showError('Please enter a URL');
                    return;
                }
                
                document.getElementById('loading').style.display = 'block';
                document.getElementById('error').style.display = 'none';
                document.getElementById('result').style.display = 'none';
                document.querySelector('button').disabled = true;
                
                fetch('/fetch-url', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ url: url })
                })
                .then(response => response.json())
                .then(data => {
                    document.getElementById('loading').style.display = 'none';
                    document.querySelector('button').disabled = false;
                    
                    if (data.status === 'ok') {
                        document.getElementById('contentText').textContent = data.data.text;
                        document.getElementById('result').style.display = 'block';
                    } else {
                        showError(data.message || 'Error fetching content');
                    }
                })
                .catch(error => {
                    document.getElementById('loading').style.display = 'none';
                    document.querySelector('button').disabled = false;
                    showError('Network error: ' + error.message);
                });
            }
            
            function showError(message) {
                const errorDiv = document.getElementById('error');
                errorDiv.textContent = message;
                errorDiv.style.display = 'block';
            }
            
            document.getElementById('urlInput').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    fetchContent();
                }
            });
        </script>
    </body>
    </html>
    """
    return html

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