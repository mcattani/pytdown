# get_video_info.py
# Este script se encarga de obtener la información de un video de YouTube utilizando la biblioteca yt_dlp.

from pytdown.utils import format_size, sanitize_str, simplify_codec
from typing import Any
from dataclasses import dataclass
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError
from rich.console import Console
"""
Importamos Deno (entorno de ejecución (runtime) para JavaScript).
Es necesario para que yt_dlp pueda ejecutar el código JavaScript que algunas páginas 
(como YouTube) usan para generar los enlaces de descarga reales.
"""
import deno

console = Console()

@dataclass
class FormatInfo:
    """
    Clase de datos para representar la información técnica de un formato específico.
    """
    format_id: str  # ID interno del formato en YouTube
    calidad: str    # Resolución (ej: 720p)
    fps: int        # Cuadros por segundo
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
        console.print(f"[red]No se pudo obtener la información del video:[/red] {e.msg}")
        return None
  
    # Si por alguna razón info viene vacío, retornamos None
    if not info:
        return None

    # Extraemos y sanitizamos el título general del video
    title: str = sanitize_str(info.get("title", "Sin título"))

    # Lista para almacenar los objetos FormatInfo filtrados
    formatos_validos: list[FormatInfo] = []
    # Conjunto para llevar control de lo que ya hemos añadido y evitar duplicados
    vistos: set[tuple[Any, Any, Any, Any, Any]] = set()

    # 'formats' contiene una lista de diccionarios con cada calidad/tipo disponible
    formatos: list[dict[str, Any]] = info.get("formats", [])
    
    for formato in formatos:
        # Filtramos: solo nos interesan formatos que tengan pista de video Y audio juntas
        vcodec = formato.get("vcodec")
        acodec = formato.get("acodec")

        if vcodec != "none" and acodec != "none":
            height = formato.get("height")
            ext = formato.get("ext")
            fps = formato.get("fps")
            v_codec_simple = simplify_codec(vcodec)
            a_codec_simple = simplify_codec(acodec)

            # Creamos una tupla con los datos de la lista de formatos para evitar la duplicación
            lista_formatos = (height, ext, v_codec_simple, a_codec_simple, fps)

            if lista_formatos in vistos:
                continue
            
            vistos.add(lista_formatos)

            # El tamaño puede venir en 'filesize' o 'filesize_approx'
            filesize = formato.get("filesize") or formato.get("filesize_approx")
            # Formateamos el tamaño si lo tenemos, de lo contrario dejamos "Desconocido"
            f_size_str = format_size(filesize) if filesize else "Desconocido"
            
            # Creamos una instancia de FormatInfo con los datos procesados
            format_item = FormatInfo(
                format_id=str(formato.get("format_id", "")),
                calidad=f"{height}p" if height else "N/A",
                fps=int(fps) if fps else 0,
                ext=str(ext if ext else "N/A").upper(),
                f_size=f_size_str,
                v_codec=v_codec_simple,
                a_codec=a_codec_simple
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
        console.print(f"[bold blue]Título:[/bold blue] {info.title}\n")
        console.print(f"{'ID':<10} {'Calidad':<10} {'FPS':<6} {'Ext':<6} {'V-Codec':<10} {'A-Codec':<10} {'Tamaño'}")
        console.print("-" * 85)
        for item in info.formats:
            fps_str = str(item.fps) if item.fps > 0 else "N/A"
            console.print(f"{item.format_id:<10} {item.calidad:<10} {fps_str:<6} {item.ext:<6} {item.v_codec:<10} {item.a_codec:<10} {item.f_size}")
    else:
        console.print("[red]No se encontraron formatos válidos o hubo un error.[/red]")
