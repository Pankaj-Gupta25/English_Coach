import edge_tts
import asyncio
import tempfile
import re


def clean_text_for_tts(text):

    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"\*(.*?)\*", r"\1", text)
    text = re.sub(r"\d+\.", "", text)

    return text


async def generate_audio(text, file_path):

    communicate = edge_tts.Communicate(
        text,
        voice="en-US-JennyNeural",   # very natural female voice
        rate="+10%"
    )

    await communicate.save(file_path)


def speak_text(text):

    cleaned_text = clean_text_for_tts(text)

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")

    asyncio.run(generate_audio(cleaned_text, tmp.name))

    return tmp.name