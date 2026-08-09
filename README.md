# Descargador de YouTube

Este proyecto permite descargar videos de YouTube en formato MP4 o MP3 usando solo el enlace.

## Requisitos

- Python 3.10+
- ffmpeg instalado y disponible en PATH

### Instalar ffmpeg

Ubuntu/Debian:
```bash
sudo apt update && sudo apt install -y ffmpeg
```

## Instalación

```bash
python -m pip install -r requirements.txt
```

## Uso

```bash
python main.py
```

Luego pega el enlace de YouTube y elige:
- `mp3` para audio
- `mp4` para video
