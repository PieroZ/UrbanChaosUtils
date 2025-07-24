# UrbanChaosUtils
Repo containing various scripts for Urban Chaos game.

# 🔊 Speaker Classification and Transcript Viewer

This project provides a lightweight toolset for:
- Transcribing audio files with Whisper
- Classifying speakers using unsupervised clustering
- Browsing and renaming speaker labels in a GUI
- Viewing associated transcripts

## 🗂 Overview

### `transcript_generator.py`
Uses OpenAI's Whisper model to automatically generate transcripts for all audio files in a folder.

- **Input:** `.wav`, `.mp3`, `.m4a`, etc.
- **Output:** `.txt` transcript for each file
- **Model:** Whisper (default = `base`, changeable)

---

### `classify_wavs.py`
Clusters speaker embeddings using SpeechBrain and KMeans.

- **Input:** Directory of `.wav` files
- **Output:** A file (`speaker_labels.txt`) mapping each audio file to a predicted speaker label (`label_0`, `label_1`, ...)
- **Requires:** `speechbrain`, `torchaudio`, `sklearn`

---

### `label_audio_player.py`

<img width="1425" height="644" alt="image" src="https://github.com/user-attachments/assets/38f76d24-60a6-43e6-80dd-a4832855575a" />


Interactive GUI to:
- Browse audio by speaker label
- Listen to individual clips
- View transcripts
- Rename labels (saved persistently in `label_names.json`)

- **Dependencies:** `tkinter`, `pydub`, `simpleaudio`
- **Supports:** Playback + transcript sync
- **Extra:** Remembers your custom label names across sessions

# 3D Model Viewer
Tool used to convert nprim data to .obj & .mtl format as shown in:
[https://youtu.be/sdvsI-QBcZ0 https://youtu.be/sdvsI-QBcZ0](https://youtu.be/sdvsI-QBcZ0)

# Requirements
You will need to have a full version of **Urban Chaos** game to be able to use nprim_visualizer script. 


Textures can be exported by using tools from [https://github.com/Fire-Head/UCTxcTools/tree/master](https://github.com/Fire-Head/UCTxcTools/tree/master)

nprim_visualizer script has hardcoded path to textures at line 175:

            map_Kd = f"map_Kd C:/Games/Urban Chaos/server/textures/shared/prims/tex{key:03d}hi.tga\n"

You will need to change this path accordingly, as this is the path to textures used to do UV mapping. 
Additionally I copied all nprims (so I don't accidentally modify original) to res/nprims in the directory where python script is located. 

# Animations
These section contains all the tools that are related to characters animation in Urban Chaos. 
Keyframe extractor (shown in the video https://www.youtube.com/watch?v=TWrvUnAD1H8) is the baseline for this tools as it extracts each keyframe from the .all files. 
These can be extracted into separate .obj files or alternatively each keyframe can be calculated and rendered in real time in blender. 

https://github.com/PieroZ/UrbanChaosUtils/assets/3080931/98f7e9ad-f4c2-4de1-bc2c-efa5ffb2dc62

# Acknowledgements

   + **Urban Chaos Discord**:  [Urban Chaos Discord](https://discord.gg/uHny8apA2n) Thanks for being an amazing community! I would have not continuted this work if it weren't for you guys! 
   + **SirSwish**: Special thanks to SirSwish who has been a very active member of the UC community. He developed tools for the UC modders such as [UC-MapPainter](https://github.com/SirSwish/UC-MapPainter) or [UC-ModelViewer](https://github.com/SirSwish/UC-ModelViewer). 
   + **Mike Diskett**: Mike Diskett made [MuckyFoot-UrbanChaos](https://github.com/dizzy2003/MuckyFoot-UrbanChaos) repo public which sparked my interest to reverse engineer some of it's aspects. This project would have not been possible if it weren't for him.
   + **Youtube community**: I was very hesitant to start my youtube journey but I was pleasantly surprised how positive the experience was! Thanks to all the viewers, subscribers and commenters I really do appreciate you all!
   + **Teslafane**: Tesla was there for me when I was speedrunning the game on Twitch. He enodrsed me with his positive energy which was a huge driver for me to do youtube UC content.
