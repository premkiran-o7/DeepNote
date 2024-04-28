import streamlit as st
import yt_dlp
import assemblyai as aai
import google.generativeai as genai

# Function to download audio, transcribe, and save transcript
def download_transcribe_save(URL):
    # Download audio URL (assuming AssemblyAI supports m4a)
    with yt_dlp.YoutubeDL() as ydl:
        info = ydl.extract_info(URL, download=False)
        for format in info["formats"][::-1]:
            if format["resolution"] == "audio only" and format["ext"] == "m4a":
                audio_url = format["url"]
                break

    # Set AssemblyAI API key
    aai.settings.api_key = st.secrets.aai

    # Transcribe audio
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_url)

    # Save transcript to file
    filename = "transcript.txt"  # Customize filename as desired
    with open(filename, 'w') as f:
        f.write(transcript.text)

    st.success(f"Transcript saved to: {filename}")
    return filename

# Function to generate notes and save to Markdown file
def generate_notes(transcript_filename):
    # Generate notes
    genai.configure(api_key=st.secrets.ggai)
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    with open(transcript_filename, "r") as f:
        context = f.read()
    response = model.generate_content(f"Convert the given transcript into a well-formatted markdown notes and explore other sources on the internet to add more context. The transcript is:\n\n{context}")

    # Save notes to file
    notes_filename = "notes.md"
    with open(notes_filename, 'w') as f:
        f.write(response.text)

    st.success(f"Notes saved to: {notes_filename}")
    return notes_filename, response.text

# UI
st.title("YouTube Audio Transcription and Note Generation")

# Stage 1: Input URL
url_input = st.text_input("Enter YouTube video URL:")
if url_input:
    transcript_filename = download_transcribe_save(url_input)
    st.success("Transcription generated! Click the button below to generate notes.")
    generate_notes_button = st.button("Generate Notes")

# Stage 2: Generate notes from transcript
if "transcript_filename" in locals():
    if generate_notes_button:
        notes_filename, notes_text = generate_notes(transcript_filename)
        st.success("Notes generated!")
        st.markdown(notes_text)
        st.markdown("---")
        #st.markdown(f"Download the notes markdown file [here](/{notes_filename})")
        st.download_button(
            label="Download data as md file",
            data=notes_text,
            file_name='notes.md',
            mime='text/md',
        )
