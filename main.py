from pynput.keyboard import Listener as KeyboardListener, Key, KeyCode
from pynput.mouse import Listener as MouseListener
import time
from pydub import AudioSegment
import random
import threading

# List of key presses
key_presses = []
start = time.time_ns()

# List of current keys pressed down
curr = set()

# Load all sounds
sounds = []
for i in range(9):
    sounds.append(AudioSegment.from_file(f"types/c{i+1}.wav", format="wav"))
click = AudioSegment.from_file("click.wav", format="wav")

# Stop recording var
stop = False


def process_recording():
    global stop
    print("Recording done... processing...")
    kps = key_presses[:-3]

    # Get max sound length
    max_len = 0
    for sound in sounds:
        max_len = max(max_len, len(sound))

    # Calculate the total duration of the track in milliseconds (adjust based on your timestamps)
    max_timestamp_ns = max(map(lambda x: x[0], kps))
    total_duration_ms = (max_timestamp_ns / 1e6) + max_len  # Convert nanoseconds to milliseconds and account for sound length

    # Create a silent audio segment of the required length
    output = AudioSegment.silent(duration=total_duration_ms)

    # Loop over each timestamp and overlay the sound at the correct position
    for timestamp in kps:
        sound = None
        if timestamp[1] == 'mouse':
            sound = click
        else:
            sound = random.choice(sounds)
        position_ms = timestamp[0] / 1e6  # Convert nanoseconds to milliseconds
        output = output.overlay(sound, position=position_ms)

    # Export the final audio as a WAV file
    output.export("output_audio.wav", format="wav")
    print("Done!")
    stop = True


def on_press(key):
    curr.add(key)
    key_presses.append((time.time_ns() - start, 'key'))

    if(key == KeyCode.from_char('T') and Key.shift in curr and Key.ctrl in curr):
        process_recording()
        return False


def on_release(key):
    if key in curr:
        curr.remove(key)


def on_click(x, y, button, pressed):
    if stop:
        return False

    if pressed:
        key_presses.append((time.time_ns() - start, 'mouse'))


def run_keyboard_listener():
    with KeyboardListener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


def run_mouse_listener():
    with MouseListener(on_click=on_click) as listener:
        listener.join()


def start_listeners():
    # Create keyboard listener thread
    keyboard_thread = threading.Thread(target=run_keyboard_listener)
    # Create mouse listener thread
    mouse_thread = threading.Thread(target=run_mouse_listener)

    # Start both threads
    keyboard_thread.start()
    mouse_thread.start()

    # Wait for both threads to complete
    keyboard_thread.join()
    mouse_thread.join()


# Start both listeners concurrently
start_listeners()
