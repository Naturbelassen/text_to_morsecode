from PIL import Image, ImageDraw
from moviepy import ImageSequenceClip, AudioFileClip
import numpy as np
from pydub import AudioSegment
from pydub.generators import Sine
import subprocess


# Morse-Code Definition
MORSE_CODE = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..',
    '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
    '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----',
    ' ': ' '
}

# Message to Convert
message = "Hello World"

# Convert Message to Morse Code
def text_to_morse(text):
    return ' '.join(MORSE_CODE[char] if char != ' ' else '' for char in text.upper()).replace('  ', ' ')

morse_message = text_to_morse(message)
print(morse_message)
print(f"Length of Morse message: {len(morse_message)}")

# Image Settings
image_size = (200, 200)
background_color = "black"
dot_color = "white"
frames = []

# Timing (in milliseconds) with larger pauses
dot_time = 200  # Duration of a dot
line_time = 400  # Duration of a dash
symbol_pause = 300  # Larger pause between symbols
word_pause = 600  # Larger pause between words

# Create Frames for Morse Code
for symbol in morse_message:
    if symbol == ".":
        # Dot Frame
        img = Image.new("RGB", image_size, background_color)
        draw = ImageDraw.Draw(img)
        draw.ellipse((80, 80, 120, 120), fill=dot_color)
        frames.append((img, dot_time))  # Frame for the dot
        pause_img = Image.new("RGB", image_size, background_color)  # Pause after the dot
        frames.append((pause_img, symbol_pause))
    elif symbol == "-":
        # Dash Frame
        img = Image.new("RGB", image_size, background_color)
        draw = ImageDraw.Draw(img)
        draw.rectangle((60, 90, 140, 110), fill=dot_color)
        frames.append((img, line_time))  # Frame for the dash
        pause_img = Image.new("RGB", image_size, background_color)  # Pause after the dash
        frames.append((pause_img, symbol_pause))
    elif symbol == " ":
        # Space Between Words
        print("Space")
        img = Image.new("RGB", image_size, background_color)
        frames.append((img, word_pause))  # Pause between words

# Add Final Pause After the Last Symbol
final_pause_img = Image.new("RGB", image_size, background_color)
frames.append((final_pause_img, word_pause))  # Final long pause

# Save Frames as GIF
output_file_gif = "hello_world_morse.gif"
frames_list = [frame[0] for frame in frames]
durations = [frame[1] for frame in frames]

frames_list[0].save(
    output_file_gif,
    save_all=True,
    append_images=frames_list[1:],
    duration=durations,
    loop=0
)

print(f"GIF saved as {output_file_gif}")

# Generate Morse Code Audio
audio = AudioSegment.silent(duration=0)
frequency = 550  # Frequency of the Morse code tone

for symbol in morse_message:
    if symbol == ".":
        audio += Sine(frequency).to_audio_segment(duration=dot_time)
        audio += AudioSegment.silent(duration=symbol_pause)
    elif symbol == "-":
        audio += Sine(frequency).to_audio_segment(duration=line_time)
        audio += AudioSegment.silent(duration=symbol_pause)
    elif symbol == " ":
        audio += AudioSegment.silent(duration=word_pause)

# Save the audio file
audio_file = "hello_world_morse.wav"
audio.export(audio_file, format="wav")


# Dateinamen definieren
gif_file = output_file_gif
audio_file = audio_file
output_file = "youtput___.mp4"

# FFmpeg-Befehl erstellen
command = [
    "ffmpeg",
    "-i", gif_file,  # Input GIF
    "-i", audio_file,  # Input WAV
    "-c:v", "libx264",  # Video-Codec
    "-c:a", "aac",  # Audio-Codec
    "-shortest",  # Kürze auf die kürzere Eingabe
    output_file  # Output-Datei
]

# FFmpeg-Befehl ausführen
try:
    subprocess.run(command, check=True)
    print(f"Video erfolgreich erstellt: {output_file}")
except subprocess.CalledProcessError as e:
    print("Fehler beim Ausführen von FFmpeg:")
    print(e)
