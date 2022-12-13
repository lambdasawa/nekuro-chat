from yt_dlp import YoutubeDL


def download_youtube_audio(url):
    ydl_opts = {
        'outtmpl': 'data/youtube-audio/%(id)s.%(ext)s',
        'format': 'mp3/bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }]
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


download_youtube_audio('https://www.youtube.com/watch?v=BaW_jenozKc')
