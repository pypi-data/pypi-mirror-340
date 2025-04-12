"""
Huggingface Seq2SeqML models based voice assistant/chat!
"""

import argparse
import configparser
import json
import os
import traceback
from typing import Optional

import pyttsx3
import rich
import speech_recognition
import transformers


argparser = argparse.ArgumentParser(
    prog="HuggyVA",
    description="Huggingface Seq2SeqML models based voice assistant/chat!",
    epilog="Enjoy making your own open-source voice-assistants",
)

argparser.add_argument("--microphone-device-index", type=Optional[int], default=None)
argparser.add_argument("--microphone-sample-rate", type=Optional[int], default=None)
argparser.add_argument("--microphone-chunk-size", type=int, default=1024)

argparser.add_argument("--model-name", type=str, default="lucadiliello/bart-small")

argparser.add_argument("--speech-recognition-engine", type=str, default="google")
argparser.add_argument(
    "--speech-recognition-engine-kwargs", type=Optional[str], default=None
)

argparser.add_argument("--tts-driver-name", type=Optional[str], default=None)
argparser.add_argument("--tts-rate", type=int, default=100)
argparser.add_argument("--tts-volume", type=int, default=1.0)
argparser.add_argument("--tts-voice", type=int, default=0)


def main() -> None:
    rich.print("Parsing [bold magenta]arguments[/bold magenta]!")
    args = argparser.parse_args()

    rich.print(
        "Reading [bold magenta]configuration file[/bold magenta]! "
        "([underline]if available[/underline])"
    )
    config = configparser.ConfigParser()
    config.read(".huggyva")

    model_name = args.model_name

    if "config.model" in config:
        model_name = config["config.model"].pop("name", model_name)

    rich.print(
        "Setting up a pretrained [bold orange]Seq2SeqLM model[/bold orange]! "
        f"[underline]({model_name!r})[/underline]"
    )
    model = transformers.AutoModelForSeq2SeqLM.from_pretrained(args.model_name)

    rich.print("Setting up an [bold orange]AutoTokenizer[/bold orange]!")
    tokenizer = transformers.AutoTokenizer.from_pretrained(args.model_name)

    rich.print("Setting up [bold green]TTS engine[/bold green]!")
    tts_driver_name = args.tts_driver_name
    tts_rate = args.tts_rate
    tts_volume = args.tts_volume
    tts_voice = args.tts_voice

    if "config.text-to-speech" in config:
        tts_driver_name = config["config.text-to-speech"].pop(
            "driver-name", tts_driver_name
        )
        tts_rate = config["config.text-to-speech"].pop("rate", tts_rate)
        tts_volume = config["config.text-to-speech"].pop("volume", tts_volume)
        tts_voice = config["config.text-to-speech"].pop("voice", tts_voice)

    tts_engine = pyttsx3.init(tts_driver_name)

    tts_engine.setProperty("rate", tts_rate)
    tts_engine.setProperty("volume", tts_volume)

    tts_voices = tts_engine.getProperty("voices")
    tts_engine.setProperty("voice", tts_voices[tts_voice])

    rich.print("Setting up [bold green]Recognizer[/bold green]!")
    recognizer = speech_recognition.Recognizer()

    rich.print("Setting up [bold green]Microphone[/bold green]!")
    microphone_device_index = args.microphone_device_index
    microphone_sample_rate = args.microphone_sample_rate
    microphone_chunk_size = args.microphone_chunk_size

    if "config.microphone" in config:
        microphone_device_index = config["config.microphone"].pop(
            "device-index", microphone_device_index
        )
        microphone_sample_rate = config["config.microphone"].pop(
            "sample-rate", microphone_sample_rate
        )
        microphone_chunk_size = config["config.microphone"].pop(
            "chunk-size", microphone_chunk_size
        )

    microphone = speech_recognition.Microphone(
        microphone_device_index,
        microphone_sample_rate,
        microphone_chunk_size,
    )

    rich.print("Setting up [bold green]speech recognition engine[/bold green]!")
    speech_recognition_engine = args.speech_recognition_engine
    speech_recognition_engine_kwargs = {}

    if "config.speech-recognition" in config:
        speech_recognition_engine = config["config.speech-recognition"].pop(
            "engine-name", speech_recognition_engine
        )

        for item in config["config.speech-recognition"]:
            speech_recognition_engine_kwargs[item] = config[
                "config.speech-recognition"
            ].pop(item)

    try:
        speech_recognizer = getattr(
            recognizer, "recognize_%s" % speech_recognition_engine
        )
    except AttributeError:
        raise AttributeError(
            f"{args.speech_recognition_engine!r} isn't a valid speech recognition engine!"
            " Instead try something like 'sphinx' or 'google'"
        )

    rich.print(
        "Reading [bold magenta]conversation history[/bold magenta]! "
        "([underline]if available[/underline])"
    )
    conversation_history = []

    if os.path.exists(".huggyva.history"):
        with open(".huggyva.history") as conversation_history_file:
            conversation_history = json.load(conversation_history_file)

    history_string = "\n".join(conversation_history)

    rich.print("Voice assistant initialized [bold green]successfully[/bold green]!")

    while True:
        rich.print("Listening to your [bold pink]beautiful voice[/bold pink]!")
        tts_engine.say("Listening to your beautiful voice")
        tts_engine.runAndWait()

        try:
            input_text = speech_recognizer(
                recognizer.listen(microphone, **speech_recognition_engine_kwargs)
            )

        except speech_recognition.UnknownValueError:
            rich.print(
                "[italic]Sorry, may you repeat what did you say[/italic]?"
                f"\n{traceback.format_exc()}"
            )
            tts_engine.say("Sorry, may you repeat what did you say")
            tts_engine.runAndWait()
            continue

        except speech_recognition.RequestError:
            rich.print(
                "[italic]Sorry, we couldn't proccess what you said[/italic]:"
                f"\n{traceback.format_exc()}"
                "\n[bold yellow]Check internet connection and etc.[/bold yellow]"
            )
            tts_engine.say("Sorry, we couldn't proccess what you said")
            tts_engine.runAndWait()
            continue

        except:
            rich.print(
                "[italic]Sorry, we couldn't proccess what you said[/italic]:"
                f"\n{traceback.format_exc()}"
            )
            tts_engine.say("Sorry, we couldn't proccess what you said")
            tts_engine.runAndWait()
            continue

        rich.print("Proccessing [bold blue]inputs[/bold blue]!")
        inputs = tokenizer.encode_plus(history_string, input_text, return_tensors="pt")
        rich.print("Generating [bold blue]response[/bold blue]!")
        outputs = model.generate(**inputs)

        rich.print("Proccessing [bold blue]response[/bold blue]!")
        response = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

        print(response)
        tts_engine.say(response)
        tts_engine.runAndWait()

        rich.print(
            "Adding input and response to [bold blue]converstation history[/bold blue]!"
        )
        conversation_history.append(input_text)
        conversation_history.append(response)

        history_string = "\n".join(conversation_history)


if __name__ == "__main__":
    main()
