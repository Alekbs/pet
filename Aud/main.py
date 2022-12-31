#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import pyaudio
import pyttsx3
import time
from datetime import datetime
from vosk import Model, KaldiRecognizer
from playsound import playsound
from threading import Thread
from PIL import ImageGrab


def listen():
    """
    Записывает речь и преобразует в текст
    """
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if (rec.AcceptWaveform(data)) and (len(data) > 0):
            answer = json.loads(rec.Result())
            if answer["text"]:
                return answer["text"]


def say(msg):
    """
    Синтез речи
    """
    print(msg)
    engine.say(msg)
    engine.runAndWait()


def timer(time_for_timer):
    """
    Функция таймера
    """
    time_second = time_for_timer[0] * 60 + time_for_timer[1]
    time.sleep(time_second)
    if stop_timer == True:
        return "Поток завершен досрочно"
    playsound(os.getcwd() + "\\alarm.mp3")
    print("Поток завершен")


def time_now():
    """
    Время в данный момент
    """
    time_check = datetime.now()
    say(f"Время: {time_check.hour} часа {time_check.minute} минут")


def text2int(textnum, numwords={}):
    """
    Перевод строковых чисел в int
    """
    if not numwords:
        units = [
            "ноль",
            "один",
            "два",
            "три",
            "четыре",
            "пять",
            "шесть",
            "семь",
            "восемь",
            "девять",
            "десять",
            "одинадцать",
            "двенадцать",
            "тринадцать",
            "четырнадцать",
            "пятнадцать",
            "шестнадцать",
            "семнадцать",
            "восемнадцать",
            "девятнадцать",
        ]

        tens = [
            "",
            "",
            "двадцать",
            "тридцать",
            "сорок",
            "пятьдесят",
            "шестьдесят",
            "семьдесят",
            "восемьдесят",
            "девяносто",
        ]

        scales = ["сто", "тысяча", "million", "billion", "trillion"]

        numwords["and"] = (1, 0)
        for idx, word in enumerate(units):
            numwords[word] = (1, idx)
        for idx, word in enumerate(tens):
            numwords[word] = (1, idx * 10)
        for idx, word in enumerate(scales):
            numwords[word] = (10 ** (idx * 3 or 2), 0)

    current = result = 0
    for word in textnum.split():
        if word not in numwords:
            return None

        scale, increment = numwords[word]
        current = current * scale + increment
        if scale > 100:
            result += current
            current = 0

    return result + current


def read_file():
    """
    Чтение файла
    """
    with open("../read/" + os.listdir("../read")[0], "r", encoding="utf8") as f:
        file = f.readlines()
    for stroke in file:
        engine.say(stroke)
        engine.runAndWait()


def main():
    """
    Главная функция программы
    """
    global stop_timer
    while True:
        say("Я вас слушаю")
        text = listen()
        print(text)
        if text == "привет":
            say("Здравствуйте")

        if "который час" in text:
            time_now()

        elif "скриншот" in text:
            snapshot = ImageGrab.grab()
            path_int = 1
            path = "../img/1.png"
            while os.path.exists(path):
                path_int += 1
                path = "../img/" + str(path_int) + ".png"
            snapshot.save(path)

        elif text.split()[0] == "таймер":

            tft = []
            for times in text.split()[1::]:
                temp = text2int(times)
                if temp == None:
                    say("Скажите правильное время")
                    break
                tft.append(temp)
            if len(tft) != 1:
                if tft[0] % 10 == 0 and tft[1] % 10 != 0:
                    tft[0] = tft[0] + tft[1]
                if len(tft) == 4:
                    tft[1] = tft[2] + tft[3]
                elif len(tft) == 3:
                    tft[1] = tft[2]
            else:
                tft.append(tft[0])
                tft[0] = 0
            time_for_timer = tft[0:2]
            stop_timer = False
            say(f"Включаю таймер {time_for_timer}")
            thread_timer = Thread(target=timer, args=(time_for_timer,))
            thread_timer.start()
        elif text.split()[0] == "останови" and "таймер" in text:
            say("Таймер остановлен!")
            stop_timer = True

        elif "прочитай файл" in text:
            stop_read = False
            say("напишите стоп, чтобы закончить чтение")
            thread_read = Thread(target=read_file(), args=())
            thread_read.start()

        elif "запусти калькулятор" in text:
            os.startfile(
                "C:\Windows\WinSxS\\amd64_microsoft-windows-calc_31bf3856ad364e35_10.0.19041.1_none_5faf0ebeba197e78\calc.exe"
            )
        elif "что ты умеешь" in text:
            say("команда который час - говорит время на данный момент")
            say("команда скриншот - делает скриншот и помещает в папку img")
            say("команда запусти калькулятор - запускает калькулятор")
            say(
                "Команда таймер минуты:секунды - запускает таймер, например таймер 10 30"
            )
            say("Прочитай файл - читает файл из папки read")
            say("Команда что ты умеешь - выводит возможности программы")
            say("Команда выход - выходит из программы")
        elif "выход" in text:
            say("До свидания...")
            exit()


if __name__ == "__main__":

    s_city = "Petersburg,RU"
    city_id = 0
    appid = "4cc4d270bd9025aabc0598cd3f2b000f"
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
