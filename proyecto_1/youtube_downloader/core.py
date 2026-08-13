import shutil
from pathlib import Path
from urllib.parse import urlparse

try:
    import yt_dlp
    from yt_dlp.utils import DownloadError
except ImportError:  # pragma: no cover - depende del entorno
    yt_dlp = None
    DownloadError = Exception

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "downloads"
OUTPUT_DIR.mkdir(exist_ok=True)


def normalize_format(fmt: str) -> str:
    """Normaliza aliases de formato a mp3 o mp4."""
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
    """Valida que la URL sea un enlace de YouTube válido."""
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("La URL debe comenzar con http:// o https://")
    if "youtube.com" not in parsed.netloc and "youtu.be" not in parsed.netloc:
        raise ValueError("La URL debe ser un enlace de YouTube.")


def is_ffmpeg_available() -> bool:
    """Indica si FFmpeg y FFprobe están disponibles en PATH."""
    return shutil.which("ffmpeg") is not None and shutil.which("ffprobe") is not None


def ensure_ffmpeg_available() -> None:
    """Garantiza que FFmpeg exista cuando el formato MP3 lo requiera."""
    if not is_ffmpeg_available():
        raise RuntimeError(
            "Falta FFmpeg/FFprobe. Instálalos para descargar en formato mp3, o para obtener mp4 con mezcla automática."
        )


def detect_js_runtime() -> str | None:
    """Busca un runtime JavaScript compatible para yt-dlp."""
    for runtime in ["deno", "node", "nodejs"]:
        if shutil.which(runtime):
            return runtime
    return None


def build_download_options(
    fmt: str,
    output_dir: Path,
    ffmpeg_available: bool,
    js_runtime: str | None = None,
    cookiefile: str | None = None,
    cookies_from_browser: str | None = None,
) -> dict:
    """Construye las opciones de descarga según el formato deseado."""
    opts = {
        "outtmpl": str(output_dir / "%(title)s.%(ext)s"),
        "quiet": True,
        "noplaylist": True,
    }

    if js_runtime:
        opts["js_runtime"] = js_runtime

    if cookiefile:
        opts["cookiefile"] = cookiefile
    elif cookies_from_browser:
        opts["cookies_from_browser"] = cookies_from_browser

    if fmt == "mp3":
        ensure_ffmpeg_available()
        opts.update(
            {
                "format": "bestaudio/best",
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "0",
                    }
                ],
            }
        )
        return opts

    if ffmpeg_available:
        opts.update(
            {
                "format": "bestvideo+bestaudio/best",
                "merge_output_format": "mp4",
            }
        )
    else:
        opts.update({"format": "best[ext=mp4]/best"})
    return opts


def _require_yt_dlp():
    """Devuelve la dependencia yt-dlp o lanza un error claro si falta."""
    if yt_dlp is None:
        raise RuntimeError("yt-dlp no está instalado. Instálalo con: pip install -r requirements.txt")
    return yt_dlp


def download_youtube(
    url: str,
    fmt: str,
    output_dir: Path | None = None,
    cookiefile: str | None = None,
    cookies_from_browser: str | None = None,
    js_runtime: str | None = None,
) -> str:
    """Descarga un video de YouTube en mp3 o mp4."""
    output_dir = output_dir or OUTPUT_DIR
    output_dir.mkdir(exist_ok=True, parents=True)
    fmt = normalize_format(fmt)
    validate_youtube_url(url)
    ffmpeg_available = is_ffmpeg_available()
    ydl_module = _require_yt_dlp()

    ydl_opts = build_download_options(
        fmt,
        output_dir,
        ffmpeg_available,
        js_runtime=js_runtime,
        cookiefile=cookiefile,
        cookies_from_browser=cookies_from_browser,
    )

    try:
        with ydl_module.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            if not info:
                raise RuntimeError("No se pudo obtener información del video.")
            title = info.get("title", "video")
            print(f"Descarga completada: {title}")
            return title
    except DownloadError as exc:
        message = str(exc).lower()
        if "sign in to confirm" in message or "cookies" in message:
            raise RuntimeError(
                "YouTube requiere autenticación. Usa --cookies o --cookies-from-browser para pasar cookies de navegador."
            ) from exc
        raise
