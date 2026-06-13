# YouTube Video Downloader (CLI)

[![Python Version](https://img.shields.io/badge/python-3.13%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![yt-dlp](https://img.shields.io/badge/powered%20by-yt--dlp-red)](https://github.com/yt-dlp/yt-dlp)
[![Rich](https://img.shields.io/badge/UI-Rich-green)](https://github.com/Textualize/rich)
[![Licencia](https://img.shields.io/badge/licencia-GPL--3.0-blue)](LICENSE)

Una herramienta de línea de comandos (CLI) moderna y potente para descargar videos de YouTube con selección de formatos de alta calidad. Ahora distribuida como un paquete de Python instalable.

## Características Principales

- **Paquete Instalable:** Se integra en tu sistema como un comando global (`pytdown`).
- **Interfaz Enriquecida:** Tablas interactivas y barras de progreso dinámicas mediante la librería `Rich`.
- **Validación Inteligente:** Selección de formatos restringida a opciones válidas para garantizar descargas exitosas (audio + video.
- **Integración con Deno:** Utiliza el runtime de `Deno` para la interpretación avanzada de JavaScript requerida por YouTube.
- **Arquitectura Robusta:** Estructura de proyecto `src/` siguiendo los estándares modernos de Python.

## Estructura del Proyecto

```text
.
├── src/
│   └── pytdown/         # Código fuente del paquete
│       ├── main.py          # Punto de entrada y CLI logic
│       ├── get_video_info.py# Extracción de metadatos
│       ├── download_video.py# Gestión de descargas
│       └── utils.py         # Funciones auxiliares
├── pyproject.toml       # Definición del paquete y dependencias
└── uv.lock              # Lockfile para reproducibilidad (uv)
```

## Requisitos Previos

- **Python 3.13 o superior**
- **Deno:** Necesario para que `yt-dlp` procese los scripts de YouTube. Puedes instalarlo desde [deno.com](https://deno.com/).

## Instalación

### Opción A: Usando [uv](https://github.com/astral-sh/uv) (Recomendado)

Si eres desarrollador o quieres la mejor experiencia:

```bash
# Clonar e instalar dependencias
git clone [URL DEL REPOSITORIO]
cd youtube_downloader
uv sync

# Ejecutar sin instalar globalmente
uv run pytdown

# O instalar como herramienta global en tu sistema
uv tool install .
```

### Opción B: Usando pip (Tradicional)

```bash
git clone [URL DEL REPOSITORIO]
cd youtube_downloader
pip install .
```

## Uso

Una vez instalado, simplemente ejecuta el comando desde cualquier terminal:

```bash
pytdown
```

1. **Introducir URL:** Pega la URL del video.
2. **Seleccionar Formato:** Elige el ID de la tabla de calidades disponibles.
3. **Destino:** Selecciona la carpeta de descarga (se abrirá un selector nativo).
4. **Progreso:** Visualiza la descarga en tiempo real con la barra de progreso.

## Desarrollo

Para contribuir o modificar el proyecto:
1. Crea un entorno virtual con `uv venv` o `python -m venv .venv`.
2. Las dependencias se gestionan a través de `pyproject.toml`. No se requiere `requirements.txt`.

---

### Soporte y Feedback

Desarrollado por [The Nerdy Apprentice](https://thenerdyapprentice.blogspot.com/).

[![Invitame un café en cafecito.app](https://img.shields.io/badge/Cafecito-Soporte-orange?style=flat-square&logo=coffeescript&logoColor=white)](https://cafecito.app/thenerdyapprentice)
