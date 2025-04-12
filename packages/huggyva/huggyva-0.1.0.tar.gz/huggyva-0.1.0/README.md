# HuggyVA

HuggyVA is Huggingface Seq2SeqML models based voice assistant/chat!

## Installation

To install **HuggyVA** on your device, you can use **Pip**:

```bash
pip install huggyva
```

Or you may want to build it from its source:

```bash
git clone https://github.com/ashkanfeyzollahi/huggyva.git
cd huggyva
python -m build
```

After you install **HuggyVA**, you will need to install **PyAudio** by doing one of options below based on your platform:

* On Windows, install with PyAudio using Pip: execute `pip install SpeechRecognition[audio]` in a terminal.

* On Debian-derived Linux distributions (like Ubuntu and Mint), install PyAudio using APT: execute `sudo apt-get install python-pyaudio python3-pyaudio` in a terminal.
If the version in the repositories is too old, install the latest release using Pip: execute `sudo apt-get install portaudio19-dev python-all-dev python3-all-dev && sudo pip install SpeechRecognition[audio]` (replace pip with pip3 if using Python 3).

* On OS X, install PortAudio using Homebrew: brew install portaudio. Then, install with PyAudio using Pip: `pip install SpeechRecognition[audio]`.

* On other POSIX-based systems, install the portaudio19-dev and python-all-dev (or python3-all-dev if using Python 3) packages (or their closest equivalents) using a package manager of your choice, and then install with PyAudio using Pip: `pip install SpeechRecognition[audio]` (replace pip with pip3 if using Python 3).

## Usage

When you run the command `huggyva -h`, it shows:

```plain
usage: HuggyVA [-h] [--microphone-device-index MICROPHONE_DEVICE_INDEX]
               [--microphone-sample-rate MICROPHONE_SAMPLE_RATE]
               [--microphone-chunk-size MICROPHONE_CHUNK_SIZE] [--model-name MODEL_NAME]
               [--speech-recognition-engine SPEECH_RECOGNITION_ENGINE]
               [--speech-recognition-engine-kwargs SPEECH_RECOGNITION_ENGINE_KWARGS]
               [--tts-driver-name TTS_DRIVER_NAME] [--tts-rate TTS_RATE]
               [--tts-volume TTS_VOLUME] [--tts-voice TTS_VOICE]

Huggingface Seq2SeqML models based voice assistant/chat!

options:
  -h, --help            show this help message and exit
  --microphone-device-index MICROPHONE_DEVICE_INDEX
  --microphone-sample-rate MICROPHONE_SAMPLE_RATE
  --microphone-chunk-size MICROPHONE_CHUNK_SIZE
  --model-name MODEL_NAME
  --speech-recognition-engine SPEECH_RECOGNITION_ENGINE
  --speech-recognition-engine-kwargs SPEECH_RECOGNITION_ENGINE_KWARGS
  --tts-driver-name TTS_DRIVER_NAME
  --tts-rate TTS_RATE
  --tts-volume TTS_VOLUME
  --tts-voice TTS_VOICE
```

And when you run the `huggyva` itself (or with other flags), it will show something similiar to this:

```plain
Parsing arguments!
Reading configuration file! (if available)
Setting up a pretrained Seq2SeqLM model! ('lucadiliello/bart-small')
config.json: 100%|███████████████████████████████████████████████| 1.71k/1.71k [00:00<?, ?B/s]
model.safetensors: 100%|████████████████████████████████████| 282M/282M [10:14<00:00, 442kB/s][11:43<5:03:27, 14.9kB/s]
Setting up an AutoTokenizer!
tokenizer_config.json: 100%|█████████████████████████████████████| 1.35k/1.35k [00:00<?, ?B/s]
vocab.json: 100%|███████████████████████████████████████████| 999k/999k [00:07<00:00, 127kB/s]
merges.txt: 100%|███████████████████████████████████████████| 456k/456k [00:01<00:00, 234kB/s]
special_tokens_map.json: 100%|███████████████████████████████████████| 957/957 [00:00<?, ?B/s]
Setting up TTS engine!
Setting up Recognizer!
Setting up Microphone!
...
Listening to your beautiful voice!
```

If you want to use another model instead of default one, you can just choose *Seq2SeqML* model of your choice from **HuggingFace** and when you run `huggyva --model-name <model-name>`, or you can just make a file named `.huggyva` in your current working directory and put this into that file:

```ini
[config.model]
name=<model-name>
```

## Configuration

You can use flags to configure *huggyva* to use model of your choice, increase or decrease tts volume/rate and etc. In configuration file you can do same.

1. Start by making a new file named `.huggyva`
2. Copy and paste this default configuration to the `.huggyva` file:

    ```ini
    [config.model]
    name=lucadiliello/bart-small

    [config.microphone]
    device-index=
    sample-rate=
    chunk-size=1024

    [config.speech-recognition]
    engine-name=google

    [config.text-to-speech]
    driver-name=
    rate=100
    volume=1.0
    voice=0
    ```
