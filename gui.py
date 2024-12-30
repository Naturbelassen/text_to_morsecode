import tkinter as tk
from pydub.generators import Sine
import threading
from pydub.playback import play

def play_tone():
    global playing, current_audio
    frequency = int(slider_frequency.get())
    current_audio = Sine(frequency).to_audio_segment(duration=200)
    threading.Thread(target=play_audio).start()

def play_audio():
    global current_audio
    play(current_audio)
    #current_audio.play()

# Create the main window
root = tk.Tk()
root.title("Morse Code Generator")

# Create and place the widgets
tk.Label(root, text="Enter text to decode:").grid(row=0, column=0, padx=10, pady=10)
entry_text = tk.Entry(root, width=50)
entry_text.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Path to save file:").grid(row=1, column=0, padx=10, pady=10)
entry_path = tk.Entry(root, width=50)
entry_path.grid(row=1, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command="").grid(row=1, column=2, padx=10, pady=10)

# Create a frame to hold the width and height spinboxes
frame_dimensions = tk.Frame(root)
frame_dimensions.grid(row=2, column=1, columnspan=2, padx=10, pady=10, sticky="w")

tk.Label(root, text="Resolution (Width x Height):").grid(row=2, column=0, padx=10, pady=10)
spinbox_width = tk.Spinbox(frame_dimensions, from_=50, to=3840, increment=10, width=10)
spinbox_width.pack(side="left", padx=5)

tk.Label(frame_dimensions, text="x").pack(side="left", padx=5)

spinbox_height = tk.Spinbox(frame_dimensions, from_=50, to=2400, increment=10, width=10)
spinbox_height.pack(side="left", padx=5)

# Create a frame to hold the frequency slider and play button
freq_chooser = tk.Frame(root)
freq_chooser.grid(row=3, column=1, columnspan=2, padx=10, pady=10, sticky="w")

tk.Label(root, text="Frequency (Hz):").grid(row=3, column=0, padx=10, pady=10)
slider_frequency = tk.Scale(freq_chooser, from_=50, to=1000, orient="horizontal", length=300, width=14)
slider_frequency.pack(side="left", padx=5)

freq_play_button = tk.Button(freq_chooser, text="Play", command=play_tone).pack(side="left", padx=5)

# Run the application
root.mainloop()