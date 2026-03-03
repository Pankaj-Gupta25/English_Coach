import os
import whisper
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate

load_dotenv()

# from there we will generate the transcript of the audio
os.environ["PATH"] += os.pathsep + r"C:\ffmpeg\bin"

model = whisper.load_model("base")
result = model.transcribe("audio.mp3")

