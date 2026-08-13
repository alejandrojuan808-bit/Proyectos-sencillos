# Descargador de YouTube

Este proyecto permite descargar videos de YouTube en formato MP4 o MP3 desde la terminal. La estructura está organizada por módulos para separar la lógica de descargas, la CLI y la configuración del proyecto.

## Estructura del proyecto

```text
Proyectos-sencillos/
├── downloads/                 # Descargas generadas por la app
├── config/                    # Configuración y archivos auxiliares
├── scripts/                   # Scripts de ejecución rápida
├── tests/                     # Pruebas del proyecto
├── youtube_downloader/        # Paquete principal de la aplicación
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py                 # Entrada de la interfaz de consola
│   └── core.py                # Lógica de validación, descarga y opciones
├── main.py                    # Entrada simple compatible con el proyecto original
├── README.md
├── requirements.txt
└── .venv/
```

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

Modo interactivo recomendado:
```bash
python -m youtube_downloader
```

Modo automático con argumentos:
```bash
python -m youtube_downloader --url "https://www.youtube.com/watch?v=VIDEO_ID" --format mp4
```

También puedes usar:
- `audio` o `mp3` para audio
- `video` o `mp4` para video

Si YouTube pide inicio de sesión o un captcha, pasa cookies:
```bash
python -m youtube_downloader --url "https://www.youtube.com/watch?v=VIDEO_ID" --format mp4 --cookies cookies.txt
```

O importa cookies desde el navegador compatible:
```bash
python -m youtube_downloader --url "https://www.youtube.com/watch?v=VIDEO_ID" --format mp4 --cookies-from-browser chrome
```

### Runtime JavaScript
Si ves avisos de EJS, instala un runtime compatible y usa:
```bash
python -m youtube_downloader --url "https://www.youtube.com/watch?v=VIDEO_ID" --format mp4 --js-runtime deno
```

## Pruebas

```bash
python -m unittest discover -s tests -v
```
