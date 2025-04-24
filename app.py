import streamlit as st
from deep_translator import GoogleTranslator
from docx import Document
import time

st.title("🎬 English to Spanish Subtitle Translator")

uploaded_file = st.file_uploader("Upload subtitle file (.srt, .vtt, .txt, .docx)", type=["txt", "srt", "vtt", "docx"])

def extract_lines_from_docx(file):
    doc = Document(file)
    return [para.text for para in doc.paragraphs if para.text.strip() != ""]

def is_non_translatable(line):
    return (
        line.strip() == "" or
        "-->" in line or
        line.strip().isdigit() or
        line.strip().upper() == "WEBVTT"
    )

if uploaded_file:
    file_extension = uploaded_file.name.split(".")[-1].lower()

    if file_extension == "docx":
        lines = extract_lines_from_docx(uploaded_file)
    else:
        content = uploaded_file.read().decode("utf-8")
        lines = content.strip().splitlines()

    translator = GoogleTranslator(source='en', target='es')
    translated_lines = []

    st.write("🔄 Translating...")
    progress_bar = st.progress(0)
    status_text = st.empty()

    total_lines = len(lines)
    for i, line in enumerate(lines):
        try:
            if is_non_translatable(line):
                translated_lines.append(line)
            else:
                translated_text = translator.translate(line)
                translated_lines.append(translated_text)

            progress = (i + 1) / total_lines
            progress_bar.progress(progress)
            status_text.text(f"Translating line {i + 1}/{total_lines}")

        except Exception as e:
            translated_lines.append(f"[Error translating] {line}")
            status_text.text(f"❌ Error at line {i + 1}: {e}")

        time.sleep(0.05)  # Optional slowdown for visible progress

    st.success("✅ Translation complete!")

    translated_result = "\n".join(translated_lines)

    st.download_button(
        label="📥 Download Translated Subtitles",
        data=translated_result,
        file_name="translated_subtitles_es.txt",
        mime="text/plain"
    )

    st.subheader("📄 Preview (First 20 Lines):")
    st.text("\n".join(translated_lines[:20]))
