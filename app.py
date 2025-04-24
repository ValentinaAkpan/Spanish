import streamlit as st
from deep_translator import GoogleTranslator
import time

st.title("🎬 English to Spanish Subtitle Translator")

# Allow .txt, .srt, .vtt files (subtitle formats)
uploaded_file = st.file_uploader(
    "Upload subtitle file (.txt, .srt, .vtt)", 
    type=["txt", "srt", "vtt"]
)

# Initialize session state to store translation
if "translated_result" not in st.session_state:
    st.session_state.translated_result = None

# Translation logic
if uploaded_file and st.session_state.translated_result is None:
    file_type = uploaded_file.name.split('.')[-1].lower()

    # Read file content based on extension
    content = uploaded_file.read().decode("utf-8", errors="ignore")
    lines = content.strip().splitlines()

    translator = GoogleTranslator(source='en', target='es')
    translated_lines = []

    st.write("🔄 Translating...")
    progress_bar = st.progress(0)
    status_text = st.empty()

    total_lines = len(lines)
    for i, line in enumerate(lines):
        try:
            if line.strip() == "" or "-->" in line or line.strip().isdigit() or line.strip().upper() == "WEBVTT":
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

        time.sleep(0.05)  # Optional slowdown

    st.session_state.translated_result = "\n".join(translated_lines)
    st.success("✅ Translation complete!")

# Display and download
if st.session_state.translated_result:
    st.download_button(
        label="📥 Download Translated Subtitles",
        data=st.session_state.translated_result,
        file_name="translated_subtitles_es.txt",
        mime="text/plain"
    )

    st.subheader("📄 Preview (First 20 Lines):")
    st.text("\n".join(st.session_state.translated_result.splitlines()[:20]))
