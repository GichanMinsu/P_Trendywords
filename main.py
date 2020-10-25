# -*- coding:utf-8 -*-
import urllib3
import json
import base64
import pyaudio
import wave


def api():
    openApiURL = "http://aiopen.etri.re.kr:8000/WiseASR/Pronunciation"
    accessKey = "eb3339f4-461c-4c3f-acb5-269b3a43b0fa"
    audioFilePath = "output.pcm"
    languageCode = "english"
    # script = "pineapple"

    file = open(audioFilePath, "rb")
    audioContents = base64.b64encode(file.read()).decode("utf8")
    file.close()

    requestJson = {
        "access_key": accessKey,
        "argument": {
            "language_code": languageCode,
            # "script": script,
            "audio": audioContents
        }
    }

    http = urllib3.PoolManager()
    response = http.request(
        "POST",
        openApiURL,
        headers={"Content-Type": "application/json; charset=UTF-8"},
        body=json.dumps(requestJson)
    )

    print("[responseCode] " + str(response.status))
    print("[responBody]")
    print(str(response.data, "utf-8"))


if __name__ == "__main__":
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    RECORD_SECONDS = 4
    WAVE_OUTPUT_FILENAME = "output.pcm"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    api()
