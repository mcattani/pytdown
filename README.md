# YouTube Video Downloader (CLI)

[![Python Version](https://img.shields.io/badge/python-3.13%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![yt-dlp](https://img.shields.io/badge/powered%20by-yt--dlp-red)](https://github.com/yt-dlp/yt-dlp)
[![Rich](https://img.shields.io/badge/UI-Rich-green)](https://github.com/Textualize/rich)
[![Licencia](https://img.shields.io/badge/licencia-GPL--3.0-blue)](LICENSE)

Una herramienta de línea de comandos (CLI) para la descarga de videos de YouTube con selección de formatos de alta calidad. Desarrollada con Python 3.13, `yt-dlp` y `rich`.

## Características Principales

- **Arquitectura Modular:** Lógica separada en módulos específicos para la extracción de metadatos, gestión de descargas y funciones de utilidad.
- **Interfaz Enriquecida:** Tablas interactivas y barras de progreso dinámicas mediante la librería `Rich`.
- **Validación de Entradas:** Validación de URLs y selección de formatos restringida a opciones válidas para evitar errores de ejecución.
- **Integración con Deno:** Utiliza el runtime de `Deno` para la interpretación avanzada de JavaScript requerida por las plataformas de streaming modernas.
- **Utilidades Portátiles:** Módulo `utils.py` independiente para la sanitización de cadenas y formateo, con cero dependencias externas.

## Estructura del Proyecto

```text
.
├── main.py              # Punto de entrada y gestión de la interacción con el usuario
├── get_video_info.py    # Extracción de metadatos y filtrado de formatos
├── download_video.py    # Lógica de descarga e implementación de hooks de progreso
├── utils.py             # Funciones auxiliares reutilizables (Sin dependencias)
└── pyproject.toml       # Metadatos del proyecto y dependencias
```

## Requisitos Previos

- **Python 3.13 o superior**
- **Deno:** Requerido como runtime de JavaScript para `yt-dlp`.

## Instalación

1. **Clonar el repositorio:**
   ```bash
   git clone [URL DEL REPOSITORIO AQUÍ]
   cd youtube-downloader
   ```

2. **Instalar dependencias:**
   Se recomienda el uso de un entorno virtual:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # En Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```
   *Nota: Asegúrese de tener instalados `yt-dlp`, `rich` y el wrapper de `deno` para Python.*

## Uso

Ejecute el script principal para iniciar la interfaz interactiva:

```bash
python main.py
```

1. **Introducir URL:** Proporcione una URL válida de un video de YouTube.
2. **Selección de Formato:** Elija un ID de formato de la tabla generada (restringido a opciones válidas).
3. **Selección de Directorio:** Se abrirá un selector de carpetas nativo para elegir el destino.
4. **Monitorizar Progreso:** Siga el estado de la descarga a través de la barra de progreso en la CLI.

## Notas Técnicas

- **Filtrado de Metadatos:** El script filtra automáticamente los formatos que contienen pistas de video y audio combinadas para mayor simplicidad.
- **Sanitización:** Los nombres de archivo se sanitizan automáticamente para garantizar la compatibilidad con sistemas de archivos Windows, macOS y Linux.
- **Manejo de Errores:** Bloques `try-except` exhaustivos para gestionar problemas de red, errores específicos de `yt-dlp` y cancelaciones del usuario (Ctrl+C).

---

### Soporte y Feedback

Desarrollado por [The Nerdy Apprentice](https://thenerdyapprentice.blogspot.com/).

[![Invitame un café en cafecito.app](https://img.shields.io/badge/Cafecito-Soporte-orange?style=flat-square&logo=coffeescript&logoColor=white)](https://cafecito.app/thenerdyapprentice)
