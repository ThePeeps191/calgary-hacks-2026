import os
import yt_dlp
from .audio import audio_to_text

def download_youtube(url):
    downloads_dir = os.path.join(os.path.dirname(__file__), "..", "user_downloads")
    
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(downloads_dir, "%(id)s.%(ext)s"),
        "quiet": True,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "wav",
            "preferredquality": "192",
        }],
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        video_id = info["id"]
    
    filename = f"{video_id}.wav"
    return filename

if __name__ == "__main__":
    print(audio_to_text(download_youtube("https://www.youtube.com/watch?v=68p8MRjrvmo")))