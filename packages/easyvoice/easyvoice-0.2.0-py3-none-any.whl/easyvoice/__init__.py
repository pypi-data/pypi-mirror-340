# -*- coding: utf-8 -*-
"""Updated easyvoice (my first library for Python Community)"""

import os
import nltk
from gtts import gTTS
import speech_recognition as sr
from nltk.tokenize import sent_tokenize
from pydub import AudioSegment


# Ensure NLTK data is available (including punkt_tab if needed)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab')  # Specifically downloading punkt_tab as per your request

def text_summary(text):
    """
    Summarizes the input text to the first sentence.

    Args:
        text (str): The input text.

    Returns:
        str: The first sentence of the text.
    """
    sentences = sent_tokenize(text)
    return sentences[0] if sentences else ""

def text_to_speech(text, filename="output.mp3"):
    """
    Converts the given text to speech and saves it as an audio file.

    Args:
        text (str): The text to convert to speech.
        filename (str): The name of the file to save the audio.

    Returns:
        str: The filename of the saved audio.
    """
    tts = gTTS(text)
    tts.save(filename)
    return filename

def speech_to_text(audio_file):
    """
    Converts speech from an audio file (MP3 or WAV) to text.

    Args:
        audio_file (str): Path to the audio file.

    Returns:
        str: Recognized text.
    """
    recognizer = sr.Recognizer()
    temp_file = None

    # Convert MP3 to WAV if necessary
    if audio_file.lower().endswith(".mp3"):
        sound = AudioSegment.from_mp3(audio_file)
        temp_file = "temp.wav"
        sound.export(temp_file, format="wav")
        audio_file = temp_file  # Use the temporary WAV file

    # Recognize speech
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        print("Could not understand audio")
        text = ""
    except sr.RequestError as e:
        print(f"Error with Google Speech Recognition service; {e}")
        text = ""
    finally:
        if temp_file and os.path.exists(temp_file):
            os.remove(temp_file)  # Clean up temporary file

    return text

if __name__ == "__main__":
    input_text = "Symon finds a small cat in the garden. He gives it milk and a soft blanket. The cat purrs, and Symon smiles."
    print("Original text:", input_text)

    summary = text_summary(input_text)
    print("Summarized text:", summary)

    # Create speech from summarized text
    audio_file = text_to_speech(summary, "summary.mp3")
    print(f"Audio file created: {audio_file}")

    # Recognize text from speech
    recognized_text = speech_to_text(audio_file)
    print(f"Recognized text from {audio_file}: {recognized_text}")
