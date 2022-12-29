
import pyaudio
from vosk import Model, KaldiRecognizer
from flask import Flask, Response, render_template, request
import json
import time

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('alek.html')


@app.route("/process_audio")
def process_audio():
    url = request.args.get("url")
    print("url = ", url)


@app.route("/listen")
def listen():
    def respond_to_client():
        while True:
            stream.start_stream()
            data = stream.read(4000, exception_on_overflow=False)
            if len(data) == 0:
                break
            if (rec.AcceptWaveform(data)) and (len(data) > 0):
                answer = json.loads(rec.Result())
                text = answer['text']
                print(text)
                _data = json.dumps({"text": text})
                yield f"id: 1\ndata: {_data}\nevent: online\n\n"

        time.sleep(0.001)
    return Response(respond_to_client(), mimetype='text/event-stream')


if __name__ == "__main__":
    model = Model("vosk-model-small-ru-0.4")
    rec = KaldiRecognizer(model, 8000)
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=8000,
        input=True,
        frames_per_buffer=8000
    )
    app.run(host='0.0.0.0', port=5000, debug=False)
