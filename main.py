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


def extract_text(video_id):
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


def record_voice_from_microphone(file_id):
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

    while True:
        try:
            frames.append(stream.read(frame_per_buffer))
        except KeyboardInterrupt:
            break

    stream.stop_stream()
    stream.close()
    p.terminate()

    with wave.open("data/user-voice/%s.wav" % file_id, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))
        wf.close()


def extract_text(file_id):
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

# video_id = "5z9TcACGTXE"
# download_youtube_audio(video_id)
# for segment in extract_text(video_id):
#     print(segment)


voice_file_id = "test"
record_voice_from_microphone(voice_file_id)
user_voice_text = extract_text(voice_file_id)
print(user_voice_text)
ai_response_text = fetch_chatgpt_completions(user_voice_text)
print(ai_response_text)
