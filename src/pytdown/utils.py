# utils.py
# Conjunto de funciones útiles.

import os
import re
import time
from functools import wraps 
from typing import Callable, Any
from shutil import which

def format_size(bytes_size: int) -> str:
    """
    Convierte un tamaño en bytes a su representación más legible (KB, MB, GB, etc.)
    y devuelve una cadena de texto (string).
    """
    # Lista de unidades disponibles
    units: list[str] = ["Bytes", "KB", "MB", "GB", "TB"]
    i: int = 0
    size: float = float(bytes_size)
    
    # Dividimos por 1024 sucesivamente hasta encontrar la unidad adecuada
    # o hasta agotar las unidades disponibles en la lista.
    while size >= 1024 and i < len(units) - 1:
        size /= 1024
        i += 1
        
    # Devolvemos el tamaño con dos decimales y la unidad correspondiente (índice i)
    return f"{size:.2f} {units[i]}"

def sanitize_str(string: str) -> str:
    """
    Elimina caracteres inválidos para nombres de archivos en Windows, Mac y Linux.
    Reemplaza espacios múltiples por uno solo y quita espacios en los extremos.
    """
    # Elimina carácteres prohibidos: \ / : * ? " < > |
    clean_name: str = re.sub(r'[\\/*?:"<>|]', "", string)
    # Reemplaza múltiples espacios por uno solo y quita espacios al inicio y al final
    clean_name = re.sub(r'\s+', ' ', clean_name).strip()
    return clean_name

def truncate_filename(filename: str, max_length: int = 128) -> str:
    """
    Trunca un nombre de archivo conservando la extensión si es necesario.
    
    Algoritmo:
    - Si el nombre está dentro del límite, se devuelve sin cambios
    - Si excede el límite, se trunca el nombre base agregando "..." antes de la extensión
    - La extensión siempre se preserva intacta
    - Si no hay espacio ni para "...", se trunca todo el nombre
    
    Args:
        filename: nombre del archivo (ej: "Mi_Video_Largo.mp4")
        max_length: longitud máxima en caracteres (por defecto 128, suficiente para NTFS/ext4)
    
    Returns:
        Nombre truncado si es necesario, o el original si está dentro del límite
    
    Ejemplos:
        >>> truncate_filename("Video.mp4", 128)
        'Video.mp4'
        >>> truncate_filename("A" * 200 + ".mp4", 128)
        'AAAA...mp4'  # El nombre base se trunca, la extensión se preserva
    """
    # Separamos el nombre de archivo y la extensión
    name, ext = os.path.splitext(filename)
    
    # Si está dentro del límite, no hacemos nada
    if len(filename) <= max_length:
        return filename
    
    # Calculamos cuánto espacio disponible hay para el nombre base (restando la extensión)
    available_space = max_length - len(ext)
    
    # Si no hay espacio para "...", se trunca todo el nombre
    if available_space <= 3:
        return filename[:max_length]
    
    # Truncamos el nombre base dejando espacio para "..." y la extensión
    return name[:available_space - 3] + "..." + ext
        

def simplify_codec(codec: Any) -> str:
    """
    Simplifica el nombre del codec a un formato más amigable.
    """
    if not codec or codec == "none":
        return "N/A"
    
    codec_str = str(codec).lower()
    prefix = codec_str.split(".")[0]
    
    # Diccionario de mapeo para codecs conocidos
    codecs_map: dict[str, str] = {
        "avc1": "H.264",
        "vp9": "VP9",
        "vp09": "VP9",
        "av01": "AV1",
        "mp4a": "AAC",
        "opus": "Opus",
    }
    
    # Si el prefijo está en el diccionario, devolvemos su nombre amigable.
    # De lo contrario, devolvemos el prefijo en mayúsculas.
    return codecs_map.get(prefix, prefix.upper())

def func_timer(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Decorador para medir el tiempo de ejecución de una función.
    """
    # La función decorada se envuelve con wraps para preservar su metadata original (nombre, docstring, etc.)
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_time: float = time.perf_counter()  # Usamos perf_counter para mayor precisión
        result: Any = func(*args, **kwargs)
        end_time: float = time.perf_counter()
        print(f"La función '{func.__name__}' tardó {end_time - start_time:.4f} segundos en ejecutarse.")
        return result
    return wrapper

def check_ffmpeg() -> bool:
    """
    Comprueba si ffmpeg está instalado en el sistema.
    """
    return which("ffmpeg") is not None
    

if __name__ == "__main__":
    # Bloque de ejecución principal para pruebas manuales
    
    print(f"Prueba Bytes: {format_size(500)}")
    print(f"Prueba KB: {format_size(1024)}")
    print(f"Prueba MB: {format_size(1024 * 1024)}")
    print(f"Prueba GB: {format_size(1024 * 1024 * 1024)}")
    
    print(f"Prueba Sanitizar 1: '{sanitize_str('Video: *Nombre|Inválido?')}'")
    print(f"Prueba Sanitizar 2: '{sanitize_str('   Espacios múltiples    ')}'")
    print(f"Prueba Sanitizar 3: '{sanitize_str('Nombre-Válido_123')}'")
    
    print(f"Prueba Codec 1 (Video): {simplify_codec('avc1.640028')}")
    print(f"Prueba Codec 2 (Audio): {simplify_codec('mp4a.40.2')}")
    print(f"Prueba Codec 3 (Video): {simplify_codec('vp09.00.51.08.01.01.01.01.00')}")
    
    @func_timer
    def prueba_funcion():
        total: int = 0
        for i in range(1000000):
            total += i
    
    prueba_funcion()
    
    print(f"Prueba ffmpeg: {check_ffmpeg()}")