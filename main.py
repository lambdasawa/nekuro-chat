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


video_id = "5z9TcACGTXE"

# download_youtube_audio(video_id)

for segment in extract_text(video_id):
    print(segment)
