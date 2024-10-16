# Typing Sounds

Have you ever wanted to screen record and have the nice typing sounds of your keyboard BUT your girlfriend or cat keeps interrupting you? Well then this app is perfect for you! By listening to your typing, this app can autogenerate typing and clicking sounds for you to overlay your screen recording with.

## Setup

```
# Create a virtual environment
python -m venv venv

# Activate the environment
source venv/bin/activate

# Or on windows
./venv/Scripts/Activate

# Then install all packages
python -m pip install -r requirements.txt
```

## Execution

Run the app using `python main.py`. To stop the recording, simply hit `CTRL + SHIFT + T`.

## Output

The output of the app will be in `output_audio.wav`. Make sure to save it as it will be overwritten the next time you run the app!
