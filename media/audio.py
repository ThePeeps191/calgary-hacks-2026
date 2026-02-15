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
        
        is_already_wav = audio_path.lower().endswith('.wav')
        wav_path = audio_path
        
        if not is_already_wav:
            audio = AudioSegment.from_file(audio_path)
            wav_path = audio_path.replace(os.path.splitext(audio_path)[1], ".wav")
            audio.export(wav_path, format="wav")

            del audio
            gc.collect()
            time.sleep(0.5)
        
        import tempfile

        audio_segment = AudioSegment.from_wav(wav_path)
        duration_ms = len(audio_segment)

        CHUNK_MS = 50 * 1000

        texts = []
        if duration_ms <= CHUNK_MS:
            with sr.AudioFile(wav_path) as source:
                audio_data = recognizer.record(source)
                raw_text = recognizer.recognize_google(audio_data)
                texts.append(raw_text)
        else:
            for start in range(0, duration_ms, CHUNK_MS):
                end = min(start + CHUNK_MS, duration_ms)
                chunk = audio_segment[start:end]
                tf = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
                temp_path = tf.name
                tf.close()
                chunk.export(temp_path, format="wav")
                del chunk
                gc.collect()
                time.sleep(0.05)

                try:
                    with sr.AudioFile(temp_path) as source:
                        audio_data = recognizer.record(source)
                        raw_text = recognizer.recognize_google(audio_data)
                        texts.append(raw_text)
                except sr.UnknownValueError:
                    pass
                except sr.RequestError as e:
                    try:
                        os.remove(temp_path)
                    except Exception:
                        pass
                    return f"Error: {e}"
                finally:
                    try:
                        os.remove(temp_path)
                    except Exception:
                        pass

        raw_text = " ".join(t for t in texts if t)

        gc.collect()

        # Gemini punctuation
        chat = Prompt()
        punctuated_text = chat.prompt(f"Add proper punctuation to this text without changing the words. The text was extracted from an audio so there is a slight possbility that some words were heard wrong. In that case, do change any wrong words. WHEN RETURNING THE TEXT, DO NOT PUT QUOTATIONS AROUND THE TEXT. ONLY PUT QUOTATIONS IF THERE IS, FOR EXAMPLE, AN ACTUAL QUOTE WITHIN THE TEXT I PROVIDE YOU: {raw_text}")

        if not is_already_wav and os.path.exists(wav_path):
            try:
                time.sleep(0.2)
                os.remove(wav_path)
            except Exception:
                pass

        return punctuated_text
        # return raw_text
    
    except sr.UnknownValueError:
        return "Error: Could not understand audio"
    except sr.RequestError as e:
        return f"Error: {e}"
    except Exception as e:
        return f"Error: {str(e)}"
