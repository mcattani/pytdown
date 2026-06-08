# get_video_info.py
# Este script se encarga de obtener la información de un video de YouTube utilizando la biblioteca yt_dlp.

from utils import format_size, sanitize_str, simplify_codec
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

@dataclass
class FormatInfo:
    """
    Clase de datos para representar la información técnica de un formato específico.
    """
    format_id: str  # ID interno del formato en YouTube
    calidad: str    # Resolución (ej: 720p)
    ext: str        # Extensión del archivo (ej: MP4)
    f_size: str     # Tamaño formateado "Desconocido"
    v_codec: str    # Codec de video simplificado
    a_codec: str    # Codec de audio simplificado

@dataclass
class VideoInfo:
    """
    Clase de datos que agrupa el título del video y sus formatos disponibles.
    """
    title: str
    formats: list[FormatInfo]

def get_video_info(url: str) -> VideoInfo | None:
    """
    Obtiene la información de un video y la lista de formatos disponibles 
    que contienen tanto audio como video.
    
    Args:
        url: La dirección web del video de YouTube.
        
    Returns:
        Un objeto VideoInfo o None si ocurre un error o no hay formatos válidos.
    """
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

    # Extraemos y sanitizamos el título general del video
    title: str = sanitize_str(info.get("title", "Sin título"))

    # Lista para almacenar los objetos FormatInfo filtrados
    formatos_validos: list[FormatInfo] = []

    # 'formats' contiene una lista de diccionarios con cada calidad/tipo disponible
    formatos: list[dict[str, Any]] = info.get("formats", [])
    
    for formato in formatos:
        # Filtramos: solo nos interesan formatos que tengan pista de video Y audio juntas
        if formato.get("vcodec") != "none" and formato.get("acodec") != "none":
            # Obtenemos la altura del video para la calidad (ej: 1080)
            height = formato.get("height")
            # El tamaño puede venir en 'filesize' o 'filesize_approx'
            filesize = formato.get("filesize") or formato.get("filesize_approx")
            # Formateamos el tamaño si lo tenemos, de lo contrario dejamos "Desconocido"
            f_size_str = format_size(filesize) if filesize else "Desconocido"
            
            # Creamos una instancia de FormatInfo con los datos procesados
            format_item = FormatInfo(
                format_id=str(formato.get("format_id", "")),
                calidad=f"{height}p" if height else "N/A",
                ext=str(formato.get("ext", "N/A")).upper(),
                f_size=f_size_str,
                v_codec=simplify_codec(formato.get("vcodec")),
                a_codec=simplify_codec(formato.get("acodec"))
            )
            # Agregamos el objeto a nuestra lista de resultados
            formatos_validos.append(format_item)
    
    # Si no se encontraron formatos válidos, retornamos None
    if not formatos_validos:
        return None
        
    # Retornamos el objeto consolidado VideoInfo
    return VideoInfo(title=title, formats=formatos_validos)

if __name__ == "__main__":
    # Bloque de ejecución principal para pruebas manuales    
    URL_PRUEBA: str = "https://www.youtube.com/watch?v=sPQhTXeoiw0"

    info = get_video_info(URL_PRUEBA)
    if info:
        print(f"Título: {info.title}\n")
        print(f"{'ID':<10} {'Calidad':<10} {'Ext':<6} {'V-Codec':<10} {'A-Codec':<10} {'Tamaño'}")
        print("-" * 75)
        for item in info.formats:
            print(f"{item.format_id:<10} {item.calidad:<10} {item.ext:<6} {item.v_codec:<10} {item.a_codec:<10} {item.f_size}")
    else:
        print("No se encontraron formatos válidos o hubo un error.")
