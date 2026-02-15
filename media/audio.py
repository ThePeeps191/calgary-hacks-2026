import speech_recognition as sr
from pydub import AudioSegment
import os
import gc
import time
from llm_api import Prompt

print("media audio.py imports finished")

def audio_to_text(filename):
    # Build the file path
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    audio_path = os.path.join(project_root, "user_downloads", filename)
    
    if not os.path.exists(audio_path):
        return f"Error: File not found at {audio_path}"
    
    try:
        recognizer = sr.Recognizer()
        
        # Check if file is already WAV
        is_already_wav = audio_path.lower().endswith('.wav')
        wav_path = audio_path
        
        if not is_already_wav:
            # Convert audio to WAV
            audio = AudioSegment.from_file(audio_path)
            wav_path = audio_path.replace(os.path.splitext(audio_path)[1], ".wav")
            audio.export(wav_path, format="wav")
            # Force garbage collection to release file handles
            del audio
            gc.collect()
            time.sleep(0.5)
        
        # Read text
        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)
            raw_text = recognizer.recognize_google(audio_data)
        
        # Force garbage collection after reading
        gc.collect()
        
        # Gemini punctuation
        chat = Prompt()
        punctuated_text = chat.prompt(f"Add proper punctuation to this text without changing the words. The text was extracted from an audio so there is a slight possbility that some words were heard wrong. In that case, do change any wrong words. WHEN RETURNING THE TEXT, DO NOT PUT QUOTATIONS AROUND THE TEXT. ONLY PUT QUOTATIONS IF THERE IS, FOR EXAMPLE, AN ACTUAL QUOTE WITHIN THE TEXT I PROVIDE YOU: {raw_text}")
        
        # Only delete if we created a new WAV file (not the original)
        if not is_already_wav and os.path.exists(wav_path):
            try:
                time.sleep(0.2)
                os.remove(wav_path)
            except Exception:
                pass  # Ignore if file is still in use
        
        return punctuated_text
        # return raw_text
    
    except sr.UnknownValueError:
        return "Error: Could not understand audio"
    except sr.RequestError as e:
        return f"Error: {e}"
    except Exception as e:
        return f"Error: {str(e)}"
