import pyttsx3
import os
import requests
import wave
import pyaudio
import whisper
from yt_dlp import YoutubeDL


def download_youtube_audio(video_id):
    ydl_opts = {
        'outtmpl': 'data/youtube-audio/%(id)s.%(ext)s',
        'format': 'mp3/bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }]
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(["https://www.youtube.com/watch?v=%s" % video_id])


def extract_text_from_youtube_audio(video_id):
    print("[Start] Load whisper model")
    model = whisper.load_model("base")
    print("[End] Load whisper model")

    audio_path = "data/youtube-audio/%s.mp3" % video_id

    print("[Start] Transcribe %s" % audio_path)
    result = model.transcribe(audio_path)
    print("[End] Transcribe")

    return map(
        lambda segment:
        {
            "start": segment["start"],
            "end": segment["end"],
            "text": segment["text"]
        },
        result["segments"],
    )


def record_user_voice_from_microphone(file_id):
    format = pyaudio.paInt16
    channels = 1
    rate = 44100
    frame_per_buffer = 1024

    p = pyaudio.PyAudio()

    stream = p.open(
        format=format,
        channels=channels,
        rate=rate,
        input=True,
        frames_per_buffer=frame_per_buffer,
    )

    frames = []

    print("[Start] recording")

    while True:
        try:
            frames.append(stream.read(frame_per_buffer))
        except KeyboardInterrupt:
            break

    print("[End] recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    with wave.open("data/user-voice/%s.wav" % file_id, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))
        wf.close()


def extract_text_from_user_voice(file_id):
    print("[Start] Load whisper model")
    model = whisper.load_model("base")
    print("[End] Load whisper model")

    audio_path = "data/user-voice/%s.wav" % file_id

    print("[Start] Transcribe %s" % audio_path)
    result = model.transcribe(audio_path)
    print("[End] Transcribe")

    return result["text"]


def fetch_chatgpt_completions(prompt):
    response = requests.post(
        'https://api.openai.com/v1/completions',
        headers={
            'Authorization': 'Bearer %s' % os.environ['OPENAI_API_KEY'],
        },
        json={
            "model": "text-davinci-003",
            "prompt": prompt,
            "max_tokens": 4000
        },
    )
    return response.json()['choices'][0]['text']


def play_japanese_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


# video_id = "MhQmPRRUhjo"
# download_youtube_audio(video_id)
# for segment in extract_text_from_youtube_audio(video_id):
#     print(segment)


# voice_file_id = "test"
# record_user_voice_from_microphone(voice_file_id)
# user_voice_text = extract_text_from_user_voice(voice_file_id)
# print(user_voice_text)
# ai_response_text = fetch_chatgpt_completions(user_voice_text)
# print(ai_response_text)
# play_japanese_text(ai_response_text)
