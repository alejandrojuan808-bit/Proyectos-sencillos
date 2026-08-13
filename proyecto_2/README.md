# Proyecto 2 - Autenticador de usuario

Este proyecto muestra un ejemplo sencillo de autenticación de usuarios en Python usando un archivo local como almacenamiento.

## Estructura

```text
proyecto_2/
├── app/
│   ├── __init__.py
│   ├── auth.py
│   └── storage.py
├── data/
│   └── users.json
├── tests/
│   └── test_auth.py
├── main.py
├── requirements.txt
└── README.md
```

## Objetivo

Aprender:
- registro de usuarios
- validación de credenciales
- manejo de contraseñas con hash
- almacenamiento local simple
- pruebas unitarias

## Ejecutar

```bash
python main.py
```

## Probar

```bash
python -m unittest discover -s tests -v
```
