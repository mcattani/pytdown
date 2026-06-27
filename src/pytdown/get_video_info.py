# get_video_info.py
# Este script se encarga de obtener la información de un video de YouTube utilizando la biblioteca yt_dlp.

from pytdown.utils import format_size, simplify_codec
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
    format_id: str        # ID interno del formato en YouTube
    calidad: str          # Resolución 
    fps: int | None       # Cuadros por segundo
    ext: str              # Extensión del archivo
    f_size: str           # Tamaño formateado "Desconocido"
    v_codec: str          # Codec de video simplificado
    a_codec: str          # Codec de audio simplificado
    has_audio: bool       # Indica si el formato tiene audio
    requires_ffmpeg: bool # Indica si el formato requiere ffmpeg

@dataclass
class VideoInfo:
    """
    Clase de datos que agrupa el título del video, sus formatos disponibles 
    y el idioma original detectado.
    """
    title: str
    formats: list[FormatInfo]
    original_lang: str | None

def get_video_info(url: str) -> VideoInfo | None:
    """
    Obtiene la información de un video y los formatos de video disponibles.
    Los formatos pueden contener audio integrado o requerir una pista de audio
    adicional durante la descarga.
    
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
   
    # Si no hay título, devolvemos "Sin título"
    title: str | None = info.get("title", "Sin título")
    
    # Idioma original del video para filtrar traducciones
    original_lang = info.get("language")

    # 'formats' contiene una lista de diccionarios con cada calidad/tipo disponible
    formatos: list[dict[str, Any]] | None= info.get("formats", [])
    
    formatos_validos: list[FormatInfo] = []
    vistos: set[tuple[Any, ...]] = set()
   
    for formato in formatos:
        # Filtramos: solo nos interesan formatos que contengan video.
        # Los formatos de audio solamente (vcodec="none") se descartan.
        vcodec = formato.get("vcodec", "none")
        acodec = formato.get("acodec", "none")
        
        # Ignorar formatos sin video
        if vcodec == "none":
            continue
       
        # Filtramos los videos traducidos (solo formato original)
        lang = formato.get("language")
        is_dubbed = "dubbed" in (formato.get("format_note") or "").lower()
        if (lang and original_lang and lang != original_lang) or is_dubbed:
            continue

        # Obtenemos la resolución y el código del codec
        height = formato.get("height")
        ext = formato.get("ext")
        fps = formato.get("fps")
        v_codec_simple = simplify_codec(vcodec)
        a_codec_simple = simplify_codec(acodec)
        
        # Indica si el formato ya incluye audio
        has_audio: bool = acodec != "none"
        
        # Los formatos sin audio requieren ffmpeg (se combina video + audio separado)
        requires_ffmpeg: bool = not has_audio

        # Identificador técnico único para evitar mostrar formatos repetidos.
        id_tecnico = (height, ext, v_codec_simple, a_codec_simple, fps)

        if id_tecnico in vistos:
            continue
        
        vistos.add(id_tecnico)

        # El tamaño puede venir en 'filesize' o 'filesize_approx'
        filesize = formato.get("filesize") or formato.get("filesize_approx")
        # Formateamos el tamaño si lo tenemos, de lo contrario dejamos "?"
        f_size_str = format_size(filesize) if filesize else "?"
       
        # Creamos una instancia de FormatInfo con los datos procesados
        format_item = FormatInfo(
            format_id=str(formato.get("format_id", "")),
            calidad=f"{height}p" if height else "N/A",
            fps=int(fps) if fps else None,
            ext=str(ext if ext else "N/A").upper(),
            f_size=f_size_str,
            v_codec=v_codec_simple,
            a_codec=a_codec_simple,
            has_audio=has_audio,
            requires_ffmpeg=requires_ffmpeg
        )
        # Agregamos el objeto a nuestra lista de resultados
        formatos_validos.append(format_item)
    
    # Si no se encontraron formatos válidos, retornamos None
    if not formatos_validos: return None
        
    # Retornamos el objeto VideoInfo incluyendo el idioma original
    return VideoInfo(title=title, formats=formatos_validos, original_lang=original_lang)

if __name__ == "__main__":
    # Bloque de ejecución principal para pruebas manuales    
    URL_PRUEBA: str = "https://www.youtube.com/watch?v=sPQhTXeoiw0"

    info = get_video_info(URL_PRUEBA)
    if info:
        console.print(f"[bold blue]Título:[/bold blue] {info.title}")
        console.print(f"[bold yellow]Idioma detectado:[/bold yellow] {info.original_lang}\n")
        console.print(f"{'ID':<10} {'Resol.':<10} {'FPS':<6} {'Ext':<6} {'V-Codec':<10} {'A-Codec':<10} {'Tamaño'}")
        console.print("-" * 85)
        for item in info.formats:
            fps_str = str(item.fps) if (item.fps and item.fps > 0) else "N/A"
            console.print(f"{item.format_id:<10} {item.calidad:<10} {fps_str:<6} {item.ext:<6} {item.v_codec:<10} {item.a_codec:<10} {item.f_size}")
    else:
        console.print("[red]No se encontraron formatos válidos o hubo un error.[/red]")
