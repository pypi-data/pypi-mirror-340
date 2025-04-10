# EasyVoice

EasyVoice is a simple Python library for basic NLP, text-to-speech (TTS), and automatic speech recognition (ASR).

## Install

```bash
pip install easyvoice
```

## Usage

```python
from easyvoice import text_summary, text_to_speech, speech_to_text

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
```
