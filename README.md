# PytDown - Video Downloader (CLI)

[![Python Version](https://img.shields.io/badge/python-3.13%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![yt-dlp](https://img.shields.io/badge/powered%20by-yt--dlp-red)](https://github.com/yt-dlp/yt-dlp)
[![Rich](https://img.shields.io/badge/UI-Rich-green)](https://github.com/Textualize/rich)
[![Licencia](https://img.shields.io/badge/licencia-GPL--3.0-blue)](LICENSE)

# 🚧 **Este proyecto está en construcción** 🚧

Una herramienta de línea de comandos (CLI) para descargar videos de **YouTube, Instagram y Facebook** con selección inteligente de formatos. Distribuida como un paquete de Python instalable.

![imagen de muestra](https://i.ibb.co/zTxh4YJ8/video-propio-cffmpeg.png)

## Características Principales

- **Paquete Instalable:** Se integra en tu sistema como un comando global (`pytdown`).
- **Interfaz Enriquecida:** Tablas interactivas y barras de progreso dinámicas mediante la librería `Rich`.
- **Idioma:** Filtra y selecciona automáticamente el **lenguaje original** del video, ignorando traducciones o doblajes.
- **Multi-plataforma:** Soporta YouTube, Instagram y Facebook con formatos optimizados para cada plataforma.
- **Validación Inteligente:** Selección de formatos restringida a opciones válidas para garantizar descargas exitosas.
- **Integración con Deno:** Utiliza el runtime de `Deno` para la interpretación avanzada de JavaScript requerida por estas plataformas.

## Estructura del Proyecto

```text
.
├── src/
│   └── pytdown/          # Código fuente del paquete
│       ├── main.py           # Punto de entrada y CLI logic
│       ├── get_video_info.py # Extracción de metadatos
│       ├── download_video.py # Gestión de descargas
│       └── utils.py          # Funciones auxiliares
├── pyproject.toml        # Definición del paquete y dependencias
└── uv.lock               # Lockfile para reproducibilidad (uv)
```

## Requisitos Previos

- **Python 3.13 o superior**
- **Deno:** Necesario para que `yt-dlp` procese los scripts de YouTube. Puedes instalarlo desde [deno.com](https://deno.com/).
- **FFmpeg (Recomendado):** Necesario para descargar formatos de alta calidad (1080p, 4K, etc.) donde el video y el audio se transmiten por separado. El script unirá automáticamente ambas pistas si FFmpeg está presente en el sistema.
- **Tkinter (Opcional):** Se utiliza para mostrar un selector de carpetas gráfico. Si no está instalado (común en algunas distros de Linux), el script detectará la ausencia y te permitirá introducir la ruta manualmente por consola.

![imagen de muestra 2](https://i.ibb.co/27NRCkZx/video-propio-sffmpeg.png)

## Instalación

### Opción A: Usando [uv](https://github.com/astral-sh/uv) (Recomendado)

```bash
# Clonar e instalar dependencias
git clone https://github.com/mcattani/pytdown.git
cd youtube_downloader
uv sync

# Ejecutar sin instalar globalmente
uv run pytdown

# O instalar como herramienta global en tu sistema
uv tool install .
```

### Opción B: Usando pip (Tradicional)

```bash
git clone https://github.com/mcattani/pytdown.git
cd youtube_downloader
pip install .
```

## Uso

Una vez instalado, simplemente ejecuta el comando desde cualquier terminal:

```bash
pytdown
```

1. **Introducir URL:** Pega la URL del video (YouTube, Instagram o Facebook).
2. **Seleccionar Formato:** Elige el ID de la tabla de calidades disponibles (solo formatos compatibles).
3. **Validación:** El script comprobará si tienes `FFmpeg` si el formato elegido requiere fusión de audio/video.
4. **Destino:** Selecciona la carpeta de descarga mediante el selector gráfico o mediante la terminal (si Tkinter no está disponible).
5. **Progreso:** Visualiza la descarga con la barra de progreso.

---

Desarrollado por [The Nerdy Apprentice](https://thenerdyapprentice.blogspot.com/).

[![Invitame un café en cafecito.app](https://img.shields.io/badge/Cafecito-Soporte-orange?style=flat-square&logo=coffeescript&logoColor=white)](https://cafecito.app/thenerdyapprentice)
