import argparse
import shutil
import sys
from pathlib import Path
from urllib.parse import urlparse

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


def validate_youtube_url(url: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("La URL debe comenzar con http:// o https://")
    if "youtube.com" not in parsed.netloc and "youtu.be" not in parsed.netloc:
        raise ValueError("La URL debe ser un enlace de YouTube.")


def ensure_ffmpeg_available() -> None:
    if shutil.which("ffmpeg") is None or shutil.which("ffprobe") is None:
        raise RuntimeError("Falta FFmpeg/FFprobe. Instálalos para descargar en formato mp4 o mp3.")


def build_download_options(fmt: str, output_dir: Path) -> dict:
    if fmt == "mp3":
        return {
            "format": "bestaudio/best",
            "outtmpl": str(output_dir / "%(title)s.%(ext)s"),
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

    return {
        "format": "bestvideo+bestaudio/best",
        "outtmpl": str(output_dir / "%(title)s.%(ext)s"),
        "quiet": True,
        "noplaylist": True,
        "merge_output_format": "mp4",
    }


def download_youtube(url: str, fmt: str, output_dir: Path | None = None) -> str:
    output_dir = output_dir or OUTPUT_DIR
    output_dir.mkdir(exist_ok=True)
    fmt = normalize_format(fmt)
    validate_youtube_url(url)
    ensure_ffmpeg_available()

    ydl_opts = build_download_options(fmt, output_dir)
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        if not info:
            raise RuntimeError("No se pudo obtener información del video.")
        title = info.get("title", "video")
        print(f"Descarga completada: {title}")
        return title


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Descargador de YouTube")
    parser.add_argument("--url", help="Enlace de YouTube")
    parser.add_argument("--format", choices=["mp3", "mp4", "audio", "video"], help="Formato de salida")
    parser.add_argument("--output-dir", default=str(OUTPUT_DIR), help="Directorio donde guardar las descargas")
    return parser.parse_args()


def main() -> int:
    print("=== Descargador de YouTube ===")
    args = parse_args()
    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(exist_ok=True)

    url = args.url or input("URL: ").strip()
    fmt = args.format or input("Formato (mp3/mp4/audio/video): ").strip()

    try:
        download_youtube(url, fmt, output_dir=output_dir)
        print(f"Archivos guardados en: {output_dir}")
        return 0
    except Exception as exc:
        print(f"Error: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
