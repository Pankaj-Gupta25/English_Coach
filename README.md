# AI English Coach

A lightweight Streamlit app that records your spoken English, transcribes it, analyzes grammar and fluency with an AI pipeline, and returns a polished improved version plus spoken coaching feedback.

## Features
- Record speech from the browser (via `streamlit_mic_recorder`).
- Transcription using a local Whisper model (`whisper` package, model: `base`).
- Analysis using an LLM (`openai-oss-120B` hosted via Groq / `langchain_groq`).
- Structured output validated with the `Speech_Analysis` Pydantic model.
- Spoken AI coach output generated with `edge_tts` (saved as MP3 and played back in Streamlit).

## Prerequisites
- Python 3.8 or newer
- `ffmpeg` installed and available on `PATH` (used to convert browser `.webm` to `.wav`)
- A working microphone in the browser

Note: this project folder contains a local virtual environment at `venv310` (see `Project/English_coach/venv310`). You can use that venv, or create/activate your own.

Activate the included virtual environment (Windows, from repo root):

```powershell
cd Project\English_coach
venv310\Scripts\activate.bat    # cmd.exe
# or for PowerShell:
venv310\Scripts\Activate.ps1
```

If you prefer to create a fresh venv instead:

```powershell
python -m venv venv310
venv310\Scripts\activate.bat
```

Install Python packages (while `venv310` is active). The venv already contains many packages, but these are the main runtime dependencies:

```powershell
pip install streamlit whisper langchain langchain-core langchain-groq groq edge_tts pydantic python-dotenv
```

To capture the exact installed state for others, run:

```powershell
pip freeze > requirements.txt
```

## Run the app (from this folder)

Start the Streamlit UI (with `venv310` activated):

```powershell
cd Project\English_coach
venv310\Scripts\activate.bat
streamlit run UX.py
```

Notes:
- `UX.py` records audio in the browser (webm). `ffmpeg` converts `.webm` → `.wav` for Whisper.
- `main.py` appends `C:\ffmpeg\bin` to PATH; ensure your ffmpeg binary is in that folder or install ffmpeg and add it to PATH.

Open the browser URL shown by Streamlit, allow microphone access, then record and click `Analyze Speech`.


## Key files & modules used
- `UX.py` — Streamlit frontend and audio handling (records, saves webm, converts via `ffmpeg`, calls `analyze_audio()`)
- `main.py` — AI pipeline: local Whisper transcription, LLM analysis via Groq/ChatGroq, and coach-message creation
- `model.py` — Pydantic model `Speech_Analysis` (fields: tense_errors, article_errors, subject_verb_errors, filler_words, fluency_score, improved_version)
- `tts.py` — Text-to-speech helper using `edge_tts` (generates MP3 with voice `en-US-JennyNeural`)

Modules observed in `main.py` and available in `venv310` (representative):
- `whisper` (local OpenAI Whisper model) — `whisper.load_model("base")` used for transcription
- `langchain_groq.ChatGroq` — Groq client wrapper to call the `openai/gpt-oss-120b` model
- `langchain_core.prompts.ChatPromptTemplate` and `langchain_core.output_parsers.PydanticOutputParser`
- `python-dotenv` to load environment variables from `.env`
- `edge_tts` for TTS (async generation saved as MP3)

Environment variables used:
- `GROQ_API_KEY` — set this (for Groq) in your environment or a local `.env` file so `main.py` can initialize `ChatGroq`.

## How it works (high level)
1. The browser records audio via the `streamlit_mic_recorder` component in `UX.py`.
2. `UX.py` writes the `.webm` bytes, converts to `.wav` using `ffmpeg` and calls `analyze_audio()` in `main.py`.
3. `main.py` transcribes audio using a local Whisper model (`whisper.load_model("base").transcribe(audio_path)`).
4. The transcript is passed to a prompt chain (`ChatPromptTemplate`) and sent to the LLM via `ChatGroq` pointing at `openai/gpt-oss-120b`.
5. The response is parsed into the `Speech_Analysis` Pydantic model with `PydanticOutputParser`.
6. A short, friendly coach message is generated via a second prompt chain and the same LLM. The coach text is converted to speech by `edge_tts` and returned as an MP3 for playback in the Streamlit UI.

Key implementation details (mirrors `main.py`):

- Whisper transcription (local):

```python
import whisper
model = whisper.load_model("base")
result = model.transcribe(audio_path)
transcript = result["text"]
```

- LLM via Groq / ChatGroq (example from `main.py`):

```python
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

llm = ChatGroq(groq_api_key=os.getenv("GROQ_API_KEY"), model="openai/gpt-oss-120b", temperature=0.3)
parser = PydanticOutputParser(pydantic_object=Speech_Analysis)

prompt = ChatPromptTemplate.from_template("""...{format_instruction}...""")
chain = prompt | llm
resp = chain.invoke({"speech": transcript, "format_instruction": parser.get_format_instructions()})
parsed = parser.parse(resp.content)
```

- Coach message generation: a second prompt (`coach_prompt`) is chained into the same LLM to produce short supportive feedback (see `coach_chain` in `main.py`).

- TTS (audio output): `tts.py` uses `edge_tts` (not gTTS). It generates an MP3 using the `en-US-JennyNeural` voice and returns a temp file path that `UX.py` plays in Streamlit.


- If audio conversion fails, verify `ffmpeg` is installed and in your `PATH` (or place ffmpeg in `C:\ffmpeg\bin`).
- If the microphone component doesn't record, check browser permissions and try a different browser.
- If you see errors from the Groq client or missing `GROQ_API_KEY`, create a `.env` file in the project folder with `GROQ_API_KEY=your_key` or set the env var in your shell.
- If TTS generation fails, verify `edge_tts` is installed and your environment allows asyncio subprocesses.

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
