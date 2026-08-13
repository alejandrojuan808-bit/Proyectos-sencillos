import argparse
from pathlib import Path

from .core import OUTPUT_DIR, download_youtube


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Descargador de YouTube")
    parser.add_argument("--url", help="Enlace de YouTube")
    parser.add_argument("--format", choices=["mp3", "mp4", "audio", "video"], help="Formato de salida")
    parser.add_argument("--output-dir", default=str(OUTPUT_DIR), help="Directorio donde guardar las descargas")
    parser.add_argument("--cookies", help="Ruta al archivo de cookies de navegador")
    parser.add_argument(
        "--cookies-from-browser",
        choices=["chrome", "firefox", "edge", "safari"],
        help="Importar cookies directamente de un navegador compatible",
    )
    parser.add_argument(
        "--js-runtime",
        choices=["deno", "node", "nodejs"],
        help="Runtime JavaScript para yt-dlp (si está instalado)",
    )
    return parser.parse_args()


def main() -> int:
    print("=== Descargador de YouTube ===")
    args = parse_args()
    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(exist_ok=True, parents=True)

    url = args.url or input("URL: ").strip()
    fmt = args.format or input("Formato (mp3/mp4/audio/video): ").strip()

    try:
        download_youtube(url, fmt, output_dir=output_dir)
        print(f"Archivos guardados en: {output_dir}")
        return 0
    except Exception as exc:
        print(f"Error: {exc}")
        return 1
