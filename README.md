# AI English Coach

A lightweight Streamlit app that records your spoken English, transcribes it, analyzes grammar and fluency with a simple AI pipeline, and returns a polished improved version plus spoken coaching feedback.

## Features
- Record speech from the browser and upload audio.
- Transcription and analysis (tense, articles, subject-verb agreement, filler words).
- Fluency scoring and an improved speech suggestion.
- AI coach text returned and spoken via gTTS.

## Prerequisites
- Python 3.8 or newer
- ffmpeg installed and available on `PATH` (used to convert browser webm to wav)
- A working microphone in the browser

Note: There isn't a root `requirements.txt` visible for the repo. This project folder contains a local virtual environment `venv310` — use that to run the app or create your own virtual environment.

Activate the included virtual environment (Windows):

```
cd Project\English_coach
venv310\Scripts\activate.bat    # if you're using cmd.exe
# or for PowerShell:
venv310\Scripts\Activate.ps1
```

If you don't have the venv or want to create a fresh one:

```
python -m venv venv310
venv310\Scripts\activate.bat
```

Install required Python packages (recommended while `venv310` is active):

```
pip install streamlit gTTS pydantic streamlit-mic-recorder
```

After installing, you can generate a `requirements.txt` for reproducibility:

```
pip freeze > requirements.txt
```

## Run the app (from this folder)

Start the Streamlit UI (with `venv310` activated):

```
streamlit run UX.py
```

Open the browser URL shown by Streamlit, allow microphone access, then record and click `Analyze Speech`.

## Key files
- `UX.py` — Streamlit frontend and audio handling
- `main.py` — AI analysis pipeline entrypoint (used by `UX.py`)
- `model.py` — Pydantic model `Speech_Analysis` for structured output
- `tts.py` — Text-to-speech helper using `gTTS`

## How it works (high level)
1. The browser records audio via the `streamlit_mic_recorder` component.
2. `UX.py` saves the webm bytes, converts to WAV with `ffmpeg`, and calls `analyze_audio()` in `main.py`.
3. The pipeline returns a transcript and a `Speech_Analysis` result with errors, a fluency score, and an improved version.
4. `tts.py` converts the coach message to an mp3 for playback.

## Troubleshooting
- If audio conversion fails, verify `ffmpeg` is installed and in your `PATH`.
- If the microphone component doesn't record, check browser permissions and try a different browser.
- On Windows, install ffmpeg and add its `bin` folder to the system PATH.
- If you see missing Python packages, activate `venv310` then run `pip install` as shown above.

## Next steps / Improvements
- Replace gTTS with an offline TTS or higher-quality TTS provider (optional).
- Add persistent history of recordings and improvements.
- Add configurable analysis thresholds or multi-language support.

If you'd like, I can run a quick smoke test or commit this README for you.

## Models & Transcription

- LLM used: `openai-oss-120B` (open-source 120B model) for the analysis and improved-speech generation. You may run this model via a hosted endpoint (if available) or locally (Hugging Face / inference server) depending on your setup.
- Speech-to-text: OpenAI Whisper (`whisper-1`) is used to transcribe the recorded WAV before feeding the transcript to the LLM.

Basic integration notes and examples:

- Transcribe with Whisper (OpenAI API example):

```python
import openai

with open("audio.wav","rb") as f:
	resp = openai.Audio.transcribe("whisper-1", f)
	transcript = resp["text"]
```

- Call the LLM (conceptual example). Adjust to your client/hosting method for `openai-oss-120B`:

```python
messages = [
	{"role": "system", "content": "You are an English coach. Return valid JSON matching the Speech_Analysis schema."},
	{"role": "user", "content": f"Transcript: {transcript}\nReturn JSON only."}
]

# If using OpenAI-hosted API (example)
resp = openai.ChatCompletion.create(model="openai-oss-120b", messages=messages)
json_text = resp["choices"][0]["message"]["content"]

# Parse with Pydantic
from model import Speech_Analysis
result = Speech_Analysis.parse_raw(json_text)
```

Notes:
- Ensure the audio is converted to a Whisper-friendly format (wav, 16-bit PCM). `ffmpeg` is used in `UX.py` for this conversion.
- To improve reliability of structured output, instruct the model clearly to return only JSON and validate with `Speech_Analysis.parse_raw()`; provide example JSON in the system prompt if necessary.
