import streamlit as st
from deep_translator import GoogleTranslator
import time
import csv
import io

st.title("📜 Subtitle Translator (English ➡ Spanish)")

uploaded_file = st.file_uploader("Upload a subtitle file", type=["txt", "srt", "vtt", "csv"])
if uploaded_file is not None:
    file_type = uploaded_file.name.split(".")[-1].lower()
    content = uploaded_file.read().decode("utf-8", errors="ignore")
    translator = GoogleTranslator(source='en', target='es')
    translated_lines = []

    # ---- File parsing logic ----
    if file_type in ["srt", "txt", "vtt"]:
        lines = content.strip().split("\n")
    elif file_type == "csv":
        csv_reader = csv.reader(io.StringIO(content))
        lines = [row[0] for row in csv_reader if row]
    else:
        st.error("Unsupported file type.")
        st.stop()

    # ---- Progress tracking ----
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
            status_text.text(f"🔁 Translating line {i + 1}/{total_lines}: {line}")

        except Exception as e:
            translated_lines.append(f"[Translation Error] {line}")
            status_text.text(f"❌ Error at line {i + 1}: {str(e)}")

        time.sleep(0.05)  # Optional: slow down for dramatic effect

    st.success("✅ Translation complete!")
    st.download_button("⬇ Download Translated File", "\n".join(translated_lines), file_name="translated_subs.txt")

    st.subheader("📄 Preview of Translated Subtitles:")
    st.text("\n".join(translated_lines[:20]))
