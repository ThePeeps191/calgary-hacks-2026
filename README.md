# SpinFilter

A comprehensive bias detection and content analysis platform built in 24 hours for the **2026 Calgary Hacks hackathon**.

SpinFilter analyzes articles, audio, and text content to identify political bias, emotional manipulation, and inflammatory language. It provides detailed bias scores, unbiased alternatives, and a "drama index" to help users consume media more critically.

---

## Features

- **URL Content Scraping**: Extract and analyze news articles from any URL
- **YouTube Audio Download & Analysis**: Download audio from YouTube videos, transcribe with chunked processing, and analyze for bias
- **Audio Transcription**: Convert audio files (MP3, M4A, WAV) to text with automatic punctuation correction using Google Speech Recognition and Gemini
- **Chunked Audio Processing**: Splits long audio files into ~50s chunks to avoid API limits
- **Bias Detection**: AI-powered analysis using Gemini to identify biased language
- **Outlet Bias Lookup**: Determine media outlet bias ratings from URL
- **Paragraph Segmentation**: Break down content into analyzable chunks
- **Drama Index**: Emotional intensity and manipulative language scoring (1-100 scale) with emotion breakdown
- **Unbiased Alternatives**: LLM-generated suggestions for neutral rephrasing with HTML diff highlighting
- **Similar Article Search**: Find related articles via News API by topic and URL
- **Automatic Cleanup**: Downloaded files automatically removed after processing to save disk space
- **Real-time Processing**: Streaming results from backend to React frontend

---

## Technology Stack

### Backend
- **Flask** - REST API framework
- **Python 3.x** - Core language
- **Gemini API** - LLM for bias detection and correction
- **Google Speech Recognition** - Audio transcription
- **Newspaper4k** - Web scraping
- **Transformers (Hugging Face)** - Emotion detection models (RoBERTa-based)
- **PyDub** - Audio processing and chunking
- **yt-dlp** - YouTube video/audio downloading
- **FFmpeg** - Audio format conversion (WAV extraction)
- **News API** - Article search and discovery

### Frontend
- **React** - UI framework
- **Framer Motion** - Animations
- **Custom CSS** - Vanilla CSS with CSS variables for styling (no utility framework)

### APIs & Libraries
- **python-dotenv** - Environment variables
- **flask-cors** - Cross-origin requests
- **torch/transformers** - ML models

---

## Project Structure

```
calgary-hacks-2026/
├── main.py                 # Flask app with API endpoints
├── requirements.txt        # Python dependencies
├── .env                    # API keys (Gemini, etc.)
├── README.md               # This file
│
├── scraper/                # Web scraping module
│   ├── __init__.py
│   ├── get_content.py     # Extract article text, authors, date, keywords
│   ├── search_content.py  # Search for related articles via News API
│   └── __pycache__/
│
├── bias/                   # Bias detection & correction
│   ├── __init__.py
│   ├── bias_detection.py  # Detect biased language
│   ├── bias_correction.py # Generate unbiased alternatives
│   ├── text_replacement.py # Paragraph segmentation and analysis
│   ├── testing.py         # Local testing utilities
│   ├── bias_detection_prompt.txt   # System prompt for detection
│   └── bias_correction_prompt.txt  # System prompt for correction
│
├── media/                  # Audio processing
│   ├── __init__.py
│   ├── audio.py           # Audio to text transcription with chunking
│   └── yt.py              # YouTube audio download
│
├── metrics/                # Content analysis metrics
│   ├── __init__.py
│   └── metrics.py         # Drama index calculation
│
├── llm_api/                # LLM integration
│   ├── __init__.py
│   └── prompt.py          # Gemini API wrapper with context retention
│
├── user_downloads/        # Temporary audio file storage
│
├── react/                  # Frontend React app
│   ├── src/
│   │   ├── App.js         # Main React component
│   │   ├── App.css        # Styling
│   │   ├── index.js       # Entry point
│   │   └── ...
│   ├── package.json
│   └── public/
│
└── tests/
    └── test_api.py        # Flask API tests
```

## API Endpoints

### Content Analysis

- `POST /fetch-url` - Analyze article from URL
  - Input: `{ "url": "article_url" }`
  - Returns: bias score, paragraphs, reasons, summary, keywords, drama index

- `POST /fetch-audio` - Upload and analyze audio file
  - Input: multipart form with audio file
  - Returns: transcribed text, bias analysis, drama index

- `POST /fetch-video` - Download YouTube video audio and analyze
  - Input: `{ "url": "youtube_url" }`
  - Returns: transcribed text, bias analysis, drama index

- `POST /fetch-outlet-bias` - Get media outlet bias rating
  - Input: `{ "url": "article_url" }`
  - Returns: outlet name, bias rating, logo URL

### Transcription & Conversion

- `POST /convert-audio` - Transcribe uploaded audio file without bias analysis
  - Input: `{ "filename": "audio_filename" }`
  - Returns: `{ "status": "ok", "text": "transcribed_text" }`

- `POST /convert-yt` - Transcribe YouTube video without bias analysis
  - Input: `{ "url": "youtube_url" }`
  - Returns: `{ "status": "ok", "text": "transcribed_text" }`

### Search & Metrics

- `POST /search-similar` - Find related articles
  - Input: `{ "query": "search_query", "url": "optional_article_url" }`
  - Returns: list of related articles from News API

- `POST /get-drama-index` - Calculate drama index for text
  - Input: `{ "text": "text_content" }`
  - Returns: `{ "status": "success", "drama_index": [score, emotions] }`

---

## How It Works

### Bias Detection Pipeline

1. **Content Extraction** → Scrape or transcribe content
2. **Text Segmentation** → Break into paragraphs
3. **Bias Analysis** → Query Gemini with detection prompt
4. **Scoring** → Evaluate emotional language intensity
5. **Alternatives** → Generate neutral rephrasing
6. **Drama Index** → Calculate manipulation metrics
7. **Cleanup** → Automatically remove temporary files

### Audio Processing

For audio files longer than 50 seconds:
- Split into ~50s chunks to avoid API limits
- Process each chunk separately via Google Speech Recognition
- Concatenate results with proper spacing
- Apply Gemini punctuation correction
- Clean up temporary files

### Drama Index Calculation

The drama index (1-100) combines:
- **Emotion Detection** - RoBERTa model analyzes emotional tone (anger, disgust, fear, sadness, joy, neutral, surprise)
- **Power Words** - Counts inflammatory vocabulary (crisis, destroy, chaos, etc.)
- **Absolutist Language** - Detects extreme statements (always, never, everyone, etc.)
- **Narrative Intensity** - Measures sensational phrasing

---

## Frontend Features

- **Multi-input UI** - URL, audio, or YouTube video analysis
- **Real-time Results** - Streaming paragraph-by-paragraph feedback
- **Visual Bias Scoring** - Color-coded bias indicators (0-100 scale)
- **Drama Index Display** - Emotional intensity metrics with breakdown
- **Paragraph Navigation** - Browse and review analyzed content
- **Unbiased Alternatives** - See suggestions for neutral rephrasing
- **Animated Background** - Smooth, modern interface
- **Responsive Design** - Works on desktop and tablets

---

## Security & Privacy

- API keys stored in `.env` (never committed)
- CORS enabled for local development
- Audio/video files stored temporarily in `user_downloads` and automatically deleted after processing
- No data persistence on server
- Supports chunked processing for long audio without exposing full files to APIs

---

## Team

Created by **Danny Wang, Jonas Huang, Aaron He, and Siddhant Arora**

---

## Acknowledgments

- Gemini API for LLM capabilities
- Hugging Face for emotion detection models
- Google Speech Recognition for transcription
- The Calgary Hacks community for inspiration