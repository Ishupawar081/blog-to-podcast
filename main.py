import requests
from bs4 import BeautifulSoup
import streamlit as st
import subprocess
from gtts import gTTS
import uuid
import os


st.title("🎧 Blog → Podcast (Open Source)")

url = st.text_input("Enter Blog URL")

if st.button("Generate Podcast"):

    if url.strip() == "":
        st.warning("Enter a valid URL")

    else:
        with st.spinner("Processing..."):

            # -------- STEP 1: SCRAPE BLOG --------
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")

            paragraphs = soup.find_all("p")
            blog_text = " ".join([p.get_text() for p in paragraphs])

            # -------- STEP 2: LLM (OLLAMA) --------
            prompt = f"""
            Convert this blog into a podcast script.

            Rules:
            - Conversational
            - Engaging
            - Max 2000 characters

            Blog:
            {blog_text}
            """

            result = subprocess.run(
                ["ollama", "run", "mistral"],
                input=prompt,
                text=True,
                capture_output=True
            )

            podcast_script = result.stdout

            # -------- STEP 3: TEXT → AUDIO --------
            tts = gTTS(podcast_script)

            os.makedirs("audio", exist_ok=True)
            filename = f"audio/podcast_{uuid.uuid4()}.mp3"

            tts.save(filename)

            # -------- OUTPUT --------
            st.success("Podcast Generated!")

            audio_bytes = open(filename, "rb").read()
            st.audio(audio_bytes, format="audio/mp3")

            st.download_button(
                "Download Podcast",
                audio_bytes,
                file_name="podcast.mp3"
            )
