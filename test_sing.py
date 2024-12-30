from PIL import Image
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
    ' ': '/'
}

# Message to Convert
message = "Hello World"

def text_to_morse(text):
    # Convert each character to Morse code
    morse_code = ' '.join(MORSE_CODE[char] for char in text.upper() if char in MORSE_CODE)
    return format_morse(morse_code)

def format_morse(morse_code):
    # Entferne Leerzeichen vor und nach `/`
    return morse_code.replace(' / ', '/')

morse_message = text_to_morse(message)
print(morse_message)

# Image Settings
image_size = (1920, 1080)
background_color = "white"
frames = []

# Timing (in milliseconds) with larger pauses
white_dot_time = 100  # Duration of a dot
white_dash_time = 300  # Duration of a dash
symbol_pause = 100  # Pause between symbols
word_pause = 700  # Pause between words

imgWhite = Image.new("RGB", image_size, background_color)
imgBlack = Image.new("RGB", image_size, "black")

# Create Frames for Morse Code
for symbol in morse_message:
    if symbol == ".":
        # Dot Frame
        frames.append((imgWhite, white_dot_time))  # Frame for the dot
        frames.append((imgBlack, symbol_pause))  # Pause after the dot
    elif symbol == "-":
        # Dash Frame
        frames.append((imgWhite, white_dash_time))  # Frame for the dash
        frames.append((imgBlack, symbol_pause))  # Pause after the dash
    elif symbol == " ":
        # Space Between Words
        frames.append((imgBlack, white_dash_time)) # Pause between characters
    elif symbol == "/":
        # Space Between Words
        frames.append((imgBlack, word_pause)) # Pause between words
    

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
        audio += Sine(frequency).to_audio_segment(duration=white_dot_time)
        audio += AudioSegment.silent(duration=symbol_pause)
    elif symbol == "-":
        audio += Sine(frequency).to_audio_segment(duration=white_dash_time)
        audio += AudioSegment.silent(duration=symbol_pause)
    elif symbol == " ":
        audio += AudioSegment.silent(duration=white_dash_time)
    elif symbol == "/":
        audio += AudioSegment.silent(duration=word_pause)

# Save the audio file
audio_file = "hello_world_morse.wav"
audio.export(audio_file, format="wav")
print(f"Audio saved as {audio_file}")

# Dateinamen definieren
gif_file = output_file_gif
audio_file = audio_file
output_file = "newalleTimingsoutput___.mp4"

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