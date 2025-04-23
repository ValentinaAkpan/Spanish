import streamlit as st
from deep_translator import GoogleTranslator

st.title("📄 English to Spanish Subtitle Translator")

# Upload subtitle file
uploaded_file = st.file_uploader("Upload a .txt or .srt subtitle file", type=["txt", "srt"])
if uploaded_file is not None:
    content = uploaded_file.read().decode("utf-8")
    lines = content.strip().split("\n")

    # Cache the translator so it doesn't reload each time
    @st.cache_resource
    def get_translator():
        return GoogleTranslator(source='en', target='es')

    translator = get_translator()
    translated_lines = []

    progress_bar = st.progress(0)
    status_text = st.empty()

    # Group lines into batches (skip timecodes and numbering)
    batch = []
    indexed_lines = []
    for idx, line in enumerate(lines):
        if "-->" in line or line.strip().isdigit() or line.strip() == "":
            if batch:
                indexed_lines.append(batch)
                batch = []
            indexed_lines.append([line])  # Keep timecodes or blank lines
        else:
            batch.append(line)
    if batch:
        indexed_lines.append(batch)

    total_batches = len(indexed_lines)
    for i, group in enumerate(indexed_lines):
        if len(group) == 1 and ("-->" in group[0] or group[0].strip().isdigit() or group[0].strip() == ""):
            translated_lines.extend(group)
        else:
            try:
                # Translate all lines in the batch at once
                combined = "\n".join(group)
                translated_text = translator.translate(combined)
                translated_lines.extend(translated_text.split("\n"))
            except Exception as e:
                translated_lines.extend([f"[Translation Error] {line}" for line in group])

        progress = (i + 1) / total_batches
        progress_bar.progress(progress)
        status_text.text(f"Processing batch {i + 1}/{total_batches}")

    st.success("✅ Translation complete!")
    translated_text = "\n".join(translated_lines)

    st.download_button("📥 Download Translated File", translated_text, file_name="translated_subs_es.txt")
    st.subheader("📄 Preview (First 20 lines):")
    st.text("\n".join(translated_lines[:20]))
