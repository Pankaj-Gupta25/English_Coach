import streamlit as st

st.set_page_config(
    page_title="AI English Speaking Coach",
    page_icon="🎤",
    layout="wide"
)

st.title("🎤 AI English Speaking Coach")
st.write("Improve your English speaking with AI-powered feedback.")

st.divider()

# -------------------------
# INPUT SECTION
# -------------------------

col1, col2 = st.columns([1,2])

with col1:
    st.subheader("Select Topic")

    topics = [
        "Importance of Discipline",
        "My Dream Job",
        "Role of Technology in Education",
        "Tell me about yourself",
        "Importance of Time Management"
    ]

    topic = st.selectbox("Choose a topic", topics)

with col2:
    st.subheader("Your Speech (Testing Mode)")
    speech_text = st.text_area(
        "Paste your speech transcript",
        height=220,
        placeholder="Example: Today I want to talk about discipline..."
    )

st.write("")

analyze_button = st.button("🚀 Analyze My Speech")

st.divider()

# -------------------------
# OUTPUT SECTION
# -------------------------

if analyze_button:

    # Dummy values (replace later with LLM output)
    fluency_score = 7
    filler_words = ["um", "like"]
    tense_errors = ["I go to school yesterday"]
    article_errors = ["She is teacher"]
    subject_verb_errors = ["He go to market"]

    improved_version = """
Discipline plays a crucial role in achieving success in life.
It allows individuals to stay focused and maintain consistency
in their efforts. By practicing discipline, people can develop
strong habits that contribute to long-term personal and
professional growth.
"""

    st.header("📊 Speech Analysis")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Fluency Score", f"{fluency_score}/10")

    with col2:
        st.metric("Filler Words", len(filler_words))

    with col3:
        st.metric("Total Errors", len(tense_errors) + len(article_errors) + len(subject_verb_errors))

    st.divider()

    # -------------------------
    # TABS FOR OUTPUT
    # -------------------------

    tab1, tab2, tab3 = st.tabs(["Grammar Errors", "Confidence Indicators", "Improved Speech"])

    with tab1:

        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("Tense Errors")
            if tense_errors:
                st.write(tense_errors)
            else:
                st.success("No tense errors")

        with col2:
            st.subheader("Article Errors")
            if article_errors:
                st.write(article_errors)
            else:
                st.success("No article errors")

        with col3:
            st.subheader("Subject Verb Errors")
            if subject_verb_errors:
                st.write(subject_verb_errors)
            else:
                st.success("No subject-verb errors")

    with tab2:

        st.subheader("Filler Words Detected")

        if filler_words:
            st.write(filler_words)
        else:
            st.success("No filler words detected")

    with tab3:

        st.subheader("Improved Version of Your Speech")

        st.write(improved_version)