import whisper
import os

# Path to directory with audio files
input_dir = r"C:\vTemp\Urban Chaos\talk2"
output_dir = os.path.join(input_dir, "transcripts")
os.makedirs(output_dir, exist_ok=True)

# Load Whisper model (you can change "base" to "small", "medium", etc.)
model = whisper.load_model("base")

# Supported audio file extensions
audio_extensions = {".mp3", ".wav", ".m4a", ".flac", ".ogg"}

# Loop through all files in the directory
for filename in os.listdir(input_dir):
    if not any(filename.lower().endswith(ext) for ext in audio_extensions):
        continue  # Skip non-audio files

    filepath = os.path.join(input_dir, filename)
    print(f"Transcribing: {filename}")

    try:
        result = model.transcribe(filepath)
        transcript = result["text"]

        # Write transcript to a .txt file
        output_file = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}.txt")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(transcript)

        print(f"Saved transcript to: {output_file}")

    except Exception as e:
        print(f"Error processing {filename}: {e}")
