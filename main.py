import os
import shutil
import subprocess
import sys
from pathlib import Path

try:
    import yt_dlp
except ImportError:
    print("yt-dlp no está instalado. Instálalo con: pip install -r requirements.txt")
    sys.exit(1)


OUTPUT_DIR = Path("downloads")
OUTPUT_DIR.mkdir(exist_ok=True)


def normalize_format(fmt: str) -> str:
    normalized = fmt.strip().lower()
    aliases = {
        "mp3": "mp3",
        "audio": "mp3",
        "sonido": "mp3",
        "mp4": "mp4",
        "video": "mp4",
        "vídeo": "mp4",
    }
    if normalized in aliases:
        return aliases[normalized]
    raise ValueError("Formato inválido. Usa 'mp3' o 'mp4' (también puedes escribir 'audio' o 'video').")


def ensure_ffmpeg_available() -> None:
    if shutil.which("ffmpeg") is None or shutil.which("ffprobe") is None:
        raise RuntimeError("Falta FFmpeg/FFprobe. Instálalos para descargar en formato mp4 o mp3.")


def download_youtube(url: str, fmt: str) -> None:
    fmt = normalize_format(fmt)

    if fmt == "mp3":
        ensure_ffmpeg_available()
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": str(OUTPUT_DIR / "%(title)s.%(ext)s"),
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "0",
                }
            ],
            "quiet": True,
            "noplaylist": True,
        }
    else:
        ensure_ffmpeg_available()
        ydl_opts = {
            "format": "bestvideo+bestaudio/best",
            "outtmpl": str(OUTPUT_DIR / "%(title)s.%(ext)s"),
            "quiet": True,
            "noplaylist": True,
        }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        title = info.get("title", "video")
        print(f"Descarga completada: {title}")


if __name__ == "__main__":
    print("=== Descargador de YouTube ===")
    print("Introduce el enlace de YouTube")
    url = input("URL: ").strip()
    fmt = input("Formato (mp3/mp4/audio/video): ").strip()

    try:
        download_youtube(url, fmt)
        print(f"Archivos guardados en: {OUTPUT_DIR.resolve()}")
    except Exception as exc:
        print(f"Error: {exc}")
        sys.exit(1)
