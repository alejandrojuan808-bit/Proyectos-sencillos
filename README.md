# Descargador de YouTube

Este proyecto permite descargar videos de YouTube en formato MP4 o MP3 desde la terminal.

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

Modo interactivo:
```bash
python main.py
```

Modo automático con argumentos:
```bash
python main.py --url "https://www.youtube.com/watch?v=VIDEO_ID" --format mp4
```

También puedes usar:
- `audio` o `mp3` para audio
- `video` o `mp4` para video

Si YouTube pide inicio de sesión o un captcha, pasa cookies:
```bash
python main.py --url "https://www.youtube.com/watch?v=VIDEO_ID" --format mp4 --cookies cookies.txt
```

O importa cookies desde el navegador compatible:
```bash
python main.py --url "https://www.youtube.com/watch?v=VIDEO_ID" --format mp4 --cookies-from-browser chrome
```

### Runtime JavaScript
Si ves avisos de EJS, instala un runtime compatible y usa:
```bash
python main.py --url "https://www.youtube.com/watch?v=VIDEO_ID" --format mp4 --js-runtime deno
```

## Pruebas

```bash
python -m unittest discover -s tests -v
```
