import streamlit as st
from deep_translator import GoogleTranslator
import time

st.title("English to Spanish Subtitle Translator")

uploaded_file = st.file_uploader("Upload subtitle .txt or .srt file", type=["txt", "srt"])
if uploaded_file is not None:
    content = uploaded_file.read().decode("utf-8")
    lines = content.strip().split("\n")

    translator = GoogleTranslator(source='en', target='es')
    translated_lines = []

    progress_bar = st.progress(0)
    status_text = st.empty()

    total_lines = len(lines)
    for i, line in enumerate(lines):
        try:
            if "-->" in line or line.strip().isdigit() or line.strip() == "":
                translated_lines.append(line)
            else:
                translated = translator.translate(line)
                translated_lines.append(translated)

            progress = (i + 1) / total_lines
            progress_bar.progress(progress)
            status_text.text(f"Translating line {i + 1}/{total_lines}: {line}")

        except Exception as e:
            translated_lines.append(f"[Translation Error] {line}")
            status_text.text(f"Error at line {i + 1}: {str(e)}")

        time.sleep(0.05)  # Optional slow-down for demo effect

    st.success("✅ Translation complete!")
    st.download_button("Download Translated File", "\n".join(translated_lines), file_name="translated_subs.txt")

    st.subheader("Preview of Translated Subtitles:")
    st.text("\n".join(translated_lines[:20]))
