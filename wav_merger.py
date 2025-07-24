import subprocess
from pathlib import Path

base_dir = Path("res/wav_merger/")
output_dir = Path("output/wav_merger/")
temp_dir = base_dir / "converted"
output_file = "combined.wav"
output_path = output_dir / output_file

def convert_to_pcm_s16le(input_path: Path, output_path: Path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([
        "ffmpeg", "-y", "-i", str(input_path),
        "-ar", "22050", "-ac", "1",
        "-c:a", "pcm_s16le", str(output_path)
    ], check=True)


def merge_pcm_wavs(input_dir: Path, output_path: Path):
    # Zbierz WAV-y
    converted_wavs = sorted([f for f in input_dir.iterdir() if f.suffix.lower() == ".wav"])

    # Stwórz plik listy
    list_file_path = input_dir / "list.txt"
    with list_file_path.open("w", encoding="utf-8") as f:
        for wav in converted_wavs:
            f.write(f"file '{wav.resolve()}'\n")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Połącz z konwersją
    subprocess.run([
        "ffmpeg", "-f", "concat", "-safe", "0", "-i", str(list_file_path),
        "-c:a", "pcm_s16le", str(output_path)
    ], check=True)

    list_file_path.unlink()


if __name__ == '__main__':
    temp_dir.mkdir(parents=True, exist_ok=True)

    # Konwertuj każdy WAV do PCM S16LE
    for input_wav in sorted(base_dir.glob("*.wav")):
        converted_wav = temp_dir / input_wav.name
        convert_to_pcm_s16le(input_wav, converted_wav)

    # Połącz skonwertowane pliki
    merge_pcm_wavs(temp_dir, output_path)
