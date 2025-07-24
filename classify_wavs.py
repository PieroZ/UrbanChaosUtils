import os
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
os.environ["HF_HUB_DISABLE_SYMLINKS"] = "1"

from speechbrain.inference.speaker import SpeakerRecognition
from pathlib import Path
import torchaudio
import numpy as np
from sklearn.cluster import KMeans

AUDIO_DIR = Path("C:/vTemp/Urban Chaos/talk2/converted")
OUTPUT_FILE = AUDIO_DIR / "speaker_labels.txt"
MIN_DURATION_SEC = 1.0

if __name__ == '__main__':
    recognizer = SpeakerRecognition.from_hparams(
        source="speechbrain/spkrec-ecapa-voxceleb",
        savedir="pretrained_models/spkrec"
    )

    embeddings = []
    file_paths = []

    for wav_file in AUDIO_DIR.glob("*.wav"):
        try:
            signal, sr = torchaudio.load(wav_file)
            duration = signal.shape[1] / sr
            if duration < MIN_DURATION_SEC:
                print(f"⏭ Pominięto (za krótki): {wav_file.name}")
                continue

            # Przekazujemy załadowany sygnał zamiast ścieżki
            emb = recognizer.encode_batch(signal)
            embeddings.append(emb.squeeze().cpu().numpy())
            file_paths.append(wav_file.name)
            print(f"✅ {wav_file.name}")

        except Exception as e:
            print(f"❌ {wav_file.name}: {e}")

    if len(embeddings) < 2:
        raise RuntimeError("Za mało plików audio do klasteryzacji.")

    X = np.stack(embeddings)
    n_clusters = min(10, len(X))
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(X)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for fname, label in zip(file_paths, labels):
            f.write(f"{fname} -> label_{label}\n")

    print(f"\n📄 Wyniki zapisane do: {OUTPUT_FILE}")