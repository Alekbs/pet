#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import json
import pyaudio
import pyttsx3
import time
from datetime import datetime, date, time
from vosk import Model, KaldiRecognizer


def listen():
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if (rec.AcceptWaveform(data)) and (len(data) > 0):
            answer = json.loads(rec.Result())
            if answer["text"]:
                yield answer["text"]


def say(msg):
    print(msg)
    engine.say(msg)
    engine.runAndWait()


def time_now():
    time_check = datetime.now()
    say(f"Время: {time_check.hour} часа {time_check.minute} минут")


def main():

    say("Я вас слушаю")
    for text in listen():
        print(text)
        if "который час" in text:
            time_now()
        elif "выход" in text:
            say("До свидания...")
            exit()


if __name__ == "__main__":
    engine = pyttsx3.init()
    ru_voice_id = "HKEY_LOCAL-MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_RU-RU_IRINA_11.0"
    engine.setProperty("voice", ru_voice_id)
    model = Model("vosk-model-small-ru-0.4")
    rec = KaldiRecognizer(model, 16000)
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=8000,
    )
    stream.start_stream()
    main()
