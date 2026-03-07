import tempfile
from gtts import gTTS

def speak_text(text):

    tts=gTTS(text=text,lang="en")

    temp=tempfile.NamedTemporaryFile(delete=False,suffix=".mp3")
    tts.save(temp.name)
    return temp.name

    
