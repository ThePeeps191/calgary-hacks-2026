# SpinFilter

A comprehensive bias detection and content analysis platform built in 24 hours for the **2026 Calgary Hacks hackathon**.

SpinFilter analyzes articles, audio, and text content to identify political bias, emotional manipulation, and inflammatory language. It provides detailed bias scores, unbiased alternatives, and a "drama index" to help users consume media more critically.

---

## Features

- **URL Content Scraping**: Extract and analyze news articles from any URL
- **Audio Transcription**: Convert audio files (MP3, M4A, WAV) to text with automatic punctuation correction
- **Bias Detection**: AI-powered analysis using Gemini to identify biased language
- **Paragraph Segmentation**: Break down content into analyzable chunks
- **Drama Index**: Emotional intensity and manipulative language scoring (1-100 scale)
- **Unbiased Alternatives**: LLM-generated suggestions for neutral rephrasing
- **Real-time Processing**: Streaming results from backend to React frontend

---

## Technology Stack

### Backend
- **Flask** - REST API framework
- **Python 3.x** - Core language
- **Gemini API** - LLM for bias detection and correction
- **Google Speech Recognition** - Audio transcription
- **Newspaper4k** - Web scraping
- **Transformers (Hugging Face)** - Emotion detection models
- **PyDub** - Audio processing

### Frontend
- **React** - UI framework
- **Framer Motion** - Animations
- **TailwindCSS** - Styling

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
│   └── requirements.txt
│
├── bias/                   # Bias detection & correction
│   ├── __init__.py
│   ├── bias_detection.py  # Detect biased language
│   ├── bias_correction.py # Generate unbiased alternatives
│   ├── text_replacement.py # Paragraph segmentation and analysis
│   ├── bias_detection_prompt.txt   # System prompt for detection
│   └── bias_correction_prompt.txt  # System prompt for correction
│
├── media/                  # Audio processing
│   ├── __init__.py
│   └── audio.py           # Audio to text transcription
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

## How It Works

### Bias Detection Pipeline

1. **Content Extraction** → Scrape or transcribe content
2. **Text Segmentation** → Break into paragraphs
3. **Bias Analysis** → Query Gemini with detection prompt
4. **Scoring** → Evaluate emotional language intensity
5. **Alternatives** → Generate neutral rephrasing
6. **Drama Index** → Calculate manipulation metrics

### Drama Index Calculation

The drama index (1-100) combines:
- **Emotion Detection** - RoBERTa model analyzes emotional tone
- **Power Words** - Counts inflammatory vocabulary
- **Absolutist Language** - Detects extreme statements
- **Narrative Intensity** - Measures sensational phrasing

---

## Frontend Features

- **Multi-input UI** - URL, audio, or text analysis
- **Real-time Results** - Streaming paragraph-by-paragraph feedback
- **Visual Bias Scoring** - Color-coded bias indicators
- **Animated Background** - Smooth, modern interface
- **Responsive Design** - Works on desktop and mobile

---

## Security & Privacy

- API keys stored in `.env` (never committed)
- CORS enabled for local development
- Audio files stored temporarily and cleaned up
- No data persistence on server

---

## Team

Created by **Danny Wang, Jonas Huang, Aaron He, and Siddhant Arora**

---

## Acknowledgments

- Gemini API for LLM capabilities
- Hugging Face for emotion detection models
- Google Speech Recognition for transcription
- The Calgary Hacks community for inspiration