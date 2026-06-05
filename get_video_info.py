# get_video_info.py
# Este script se encarga de obtener la información de un video de YouTube utilizando la biblioteca yt_dlp.

from typing import Any
from dataclasses import dataclass
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError
"""
Importamos Deno (entorno de ejecución (runtime) para JavaScript).
Es necesario para que yt_dlp pueda ejecutar el código JavaScript que algunas páginas 
(como YouTube) usan para generar los enlaces de descarga reales.
"""
import deno

# URL de prueba para verificar el funcionamiento del script
URL_PRUEBA: str = "https://www.youtube.com/watch?v=szqFrpNf8yA&t=5153s"

@dataclass
class VideoInfo:
    """
    Clase de datos (dataclass) para representar de forma estructurada 
    la información relevante de cada formato de video.
    """
    format_id: str  # ID interno del formato en YouTube
    title: str      # Título del video
    calidad: str    # Resolución (ej: 720p)
    ext: str        # Extensión del archivo (ej: MP4)
    f_size: str     # Tamaño formateado "Desconocido"

def get_video_info(url: str) -> list[VideoInfo] | None:
    """
    Obtiene la lista de formatos disponibles que contienen tanto audio como video.
    Toma como argumento la URL del video de YouTube y devuelve una lista de objetos 
    VideoInfo con los datos relevantes."""
    
    # Configuración de yt_dlp para obtener metadatos sin descargar el video
    ydl_opts: dict[str, Any] = {
        "quiet": True,         # No mostrar mensajes de log en la consola
        "no_warnings": True,   # Ocultar advertencias no críticas
        # Configuramos Deno como el motor para procesar scripts de YouTube
        "js_runtimes": {"deno": {"path": deno.find_deno_bin()}}
    }
    
    # Intentamos extraer la información (metadatos) del video
    try:
        with YoutubeDL(ydl_opts) as ydl:
            # extract_info obtiene el diccionario con todos los datos del video
            # download=False asegura que no se empiece a descargar el archivo
            info = ydl.extract_info(url, download=False)
    except DownloadError as e:
        print(f"No se pudo obtener la información del video: {e.msg}")
        return None
  
    # Si por alguna razón info viene vacío, retornamos None
    if not info:
        return None

    # Extraemos el título general del video (común a todos los formatos)
    title: str = info.get("title", "Sin título")

    # Lista para almacenar los objetos VideoInfo filtrados
    formatos_validos: list[VideoInfo] = []

    # 'formats' contiene una lista de diccionarios con cada calidad/tipo disponible
    formatos: list[dict[str, Any]] = info.get("formats", [])
    
    for formato in formatos:
        # Filtramos: solo nos interesan formatos que tengan pista de video Y audio juntas
        if formato.get("vcodec") != "none" and formato.get("acodec") != "none":
            # Obtenemos la altura del video para la calidad (ej: 1080)
            height = formato.get("height")
            # El tamaño puede venir en 'filesize' o 'filesize_approx'
            filesize = formato.get("filesize") or formato.get("filesize_approx")
            
            # Creamos una instancia de nuestra clase VideoInfo con los datos procesados
            video_info = VideoInfo(
                format_id=str(formato.get("format_id", "")),
                title=title,
                calidad=f"{height}p" if height else "N/A",
                ext=str(formato.get("ext", "N/A")).upper(),
                f_size= filesize if filesize else "Desconocido"
            )
            # Agregamos el objeto a nuestra lista de resultados
            formatos_validos.append(video_info)
    
    # Retornamos la lista si contiene elementos, de lo contrario None
    return formatos_validos if formatos_validos else None

if __name__ == "__main__":
    # Bloque de ejecución principal para pruebas manuales
    info = get_video_info(URL_PRUEBA)
    if info:
        for item in info:
            print(item.format_id, item.title, item.calidad, item.ext, item.f_size)
    else:
        print("No se encontraron formatos válidos.")