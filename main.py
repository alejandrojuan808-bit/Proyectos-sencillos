import os
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


def download_youtube(url: str, fmt: str) -> None:
    if fmt not in {"mp3", "mp4"}:
        raise ValueError("Formato inválido. Usa 'mp3' o 'mp4'.")

    if fmt == "mp3":
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
    fmt = input("Formato (mp3/mp4): ").strip().lower()

    try:
        download_youtube(url, fmt)
        print(f"Archivos guardados en: {OUTPUT_DIR.resolve()}")
    except Exception as exc:
        print(f"Error: {exc}")
        sys.exit(1)
