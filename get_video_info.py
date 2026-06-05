from typing import Any
from dataclasses import dataclass
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError
"""Importamos Deno (entorno de ejecución (runtime) para JavaScript) necesario para ejecutar el código 
JavaScript que algunas páginas usan para generar los enlaces de descarga."""
import deno

# URL de prueba
URL: str = "https://www.youtube.com/watch?v=szqFrpNf8yA&t=5153s"

def get_video_info(URL: str) -> dict[str,Any]:
    pass

if __name__ == __main__:
    pass