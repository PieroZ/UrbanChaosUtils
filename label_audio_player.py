import os
import time
import threading
import json
from pathlib import Path
from tkinter import *
from tkinter.simpledialog import askstring
from pydub import AudioSegment
from pydub.playback import _play_with_simpleaudio
from collections import defaultdict

AUDIO_DIR = Path("C:/vTemp/Urban Chaos/talk2/converted")
TRANSCRIPT_DIR = Path("C:/vTemp/Urban Chaos/talk2/transcripts")
LABELS_FILE = AUDIO_DIR / "klasyfikacja_mowcow.txt"
LABEL_NAMES_FILE = AUDIO_DIR / "label_names.json"


def load_labels():
    label_map = defaultdict(list)
    with open(LABELS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if "->" in line:
                fname, label = map(str.strip, line.split("->"))
                label_map[label].append(fname)
    return label_map


def load_label_names():
    if LABEL_NAMES_FILE.exists():
        with open(LABEL_NAMES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_label_names(label_names):
    with open(LABEL_NAMES_FILE, "w", encoding="utf-8") as f:
        json.dump(label_names, f, indent=2, ensure_ascii=False)


class AudioPlayerGUI:
    def __init__(self, master):
        self.master = master
        master.title("🎧 Audio Label Browser with Transcript Viewer")
        self.label_map = load_labels()
        self.label_names = load_label_names()

        self.current_play_obj = None
        self.current_thread = None
        self.stop_flag = threading.Event()

        # Label list
        self.label_listbox = Listbox(master, selectmode=SINGLE)
        self.label_listbox.pack(side="left", fill="y")
        self.refresh_label_listbox()

        # Rename button
        self.rename_button = Button(master, text="✏ Rename Label", command=self.rename_selected_label)
        self.rename_button.pack(fill="x")

        # File list
        self.file_listbox = Listbox(master, selectmode=SINGLE, width=50)
        self.file_listbox.pack(side="left", fill="both", expand=True)

        # Scrollbar
        scrollbar = Scrollbar(master)
        scrollbar.pack(side="right", fill="y")
        self.file_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.file_listbox.yview)

        self.label_listbox.bind("<<ListboxSelect>>", self.update_files)
        self.file_listbox.bind("<Double-1>", self.play_selected)

        # Status
        self.status = Label(master, text="Select a label → then a file", anchor="w")
        self.status.pack(fill="x")

        # Stop button
        self.stop_button = Button(master, text="⏹ Stop Playback", command=self.stop_audio)
        self.stop_button.pack(fill="x")

        # Progress bar
        self.progress = Scale(master, from_=0, to=100, orient=HORIZONTAL, state=DISABLED)
        self.progress.pack(fill="x")

        # Transcript display
        self.transcript_box = Text(master, height=10, wrap=WORD, state=DISABLED)
        self.transcript_box.pack(fill="both", expand=True)

    def refresh_label_listbox(self):
        self.label_listbox.delete(0, END)
        for label in sorted(self.label_map.keys()):
            display_name = self.label_names.get(label, label)
            self.label_listbox.insert(END, display_name)

    def get_selected_raw_label(self):
        index = self.label_listbox.curselection()
        if not index:
            return None
        display_name = self.label_listbox.get(index[0])
        for raw_label, name in self.label_names.items():
            if name == display_name:
                return raw_label
        return display_name  # fallback to raw

    def update_files(self, event=None):
        raw_label = self.get_selected_raw_label()
        if not raw_label:
            return
        self.file_listbox.delete(0, END)
        for fname in sorted(self.label_map[raw_label]):
            self.file_listbox.insert(END, fname)

    def stop_audio(self):
        if self.current_play_obj:
            self.current_play_obj.stop()
            self.stop_flag.set()
            self.status.config(text="⏹ Playback stopped")
        self.progress.set(0)
        self.progress.config(state=DISABLED)

    def play_selected(self, event=None):
        selection = self.file_listbox.curselection()
        if not selection:
            return
        fname = self.file_listbox.get(selection[0])
        audio_path = AUDIO_DIR / fname
        transcript_path = TRANSCRIPT_DIR / (Path(fname).stem + ".txt")

        self.stop_audio()
        self.stop_flag.clear()

        self.status.config(text=f"▶ Playing: {fname}")
        self.show_transcript(transcript_path)

        def _play():
            audio = AudioSegment.from_wav(audio_path)
            self.progress.config(to=int(audio.duration_seconds), state=NORMAL)
            self.progress.set(0)

            play_obj = _play_with_simpleaudio(audio)
            self.current_play_obj = play_obj

            start = time.time()
            while play_obj.is_playing() and not self.stop_flag.is_set():
                elapsed = int(time.time() - start)
                self.progress.set(elapsed)
                time.sleep(0.5)

            self.progress.set(0)
            self.progress.config(state=DISABLED)

        self.current_thread = threading.Thread(target=_play, daemon=True)
        self.current_thread.start()

    def show_transcript(self, path):
        self.transcript_box.config(state=NORMAL)
        self.transcript_box.delete("1.0", END)
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                self.transcript_box.insert("1.0", f.read())
        else:
            self.transcript_box.insert("1.0", "[Transcript not available]")
        self.transcript_box.config(state=DISABLED)

    def rename_selected_label(self):
        raw_label = self.get_selected_raw_label()
        if not raw_label:
            return
        new_name = askstring("Rename Label", f"Enter a new name for label '{raw_label}':")
        if new_name:
            self.label_names[raw_label] = new_name
            save_label_names(self.label_names)
            self.refresh_label_listbox()


if __name__ == "__main__":
    root = Tk()
    gui = AudioPlayerGUI(root)
    root.mainloop()
