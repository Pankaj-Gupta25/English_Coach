import streamlit as st
import tempfile
import subprocess
import os

from streamlit_mic_recorder import mic_recorder
from main import analyze_audio
from tts import speak_text

st.set_page_config(page_title="AI English Coach", page_icon="🎤")

st.title("🎤 AI English Speaking Coach")
st.write("Record your speech and receive AI feedback.")

# -------------------------
# RECORD AUDIO
# -------------------------

audio = mic_recorder(
    start_prompt="Start Recording",
    stop_prompt="Stop Recording",
    just_once=True
)

# Save audio in session state
if audio:
    st.session_state.audio_bytes = audio["bytes"]

# -------------------------
# DISPLAY AUDIO
# -------------------------

if "audio_bytes" in st.session_state:

    st.success("Recording completed")

    st.audio(st.session_state.audio_bytes)

    if st.button("Analyze Speech"):

        with st.spinner("Processing your speech..."):

            try:

                audio_bytes = st.session_state.audio_bytes

                # Save webm
                with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
                    tmp.write(audio_bytes)
                    webm_path = tmp.name

                # Convert to wav
                wav_path = webm_path.replace(".webm", ".wav")

                subprocess.run(
                    ["ffmpeg", "-i", webm_path, wav_path],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )

                # Run AI pipeline
                transcript, result,coach_message = analyze_audio(wav_path)

                # Cleanup
                os.remove(webm_path)
                os.remove(wav_path)

                # -------------------------
                # RESULTS
                # -------------------------

                st.subheader("Transcript")
                st.write(transcript)

                st.subheader("Fluency Score")
                st.metric("Score", result.fluency_score)

                st.subheader("Improved Speech")
                st.write(result.improved_version)

                # convert to voice
                audio_file = speak_text(coach_message)
                st.subheader("🔊 Listen to your AI Coach")
                st.audio(audio_file)

                st.subheader("🧠 AI Speaking Coach")
                st.write(coach_message)
                # convert to voice
                # audio_file = speak_text(coach_message)

                # st.subheader("🔊 Listen to your AI Coach")
                # st.audio(audio_file)

                
                st.subheader("Grammar Errors")

                st.write("Tense Errors:", result.tense_errors)
                st.write("Article Errors:", result.article_errors)
                st.write("Subject Verb Errors:", result.subject_verb_errors)

                st.subheader("Filler Words")
                st.write(result.filler_words)

            except Exception as e:
                st.error(f"Error: {e}")