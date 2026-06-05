# utils.py
# Conjunto de funciones útiles.

import re
import time
from functools import wraps 
from typing import Callable, Any

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

if __name__ == "__main__":
    # Bloque de ejecución principal para pruebas manuales
    
    print(f"Prueba Bytes: {format_size(500)}")
    print(f"Prueba KB: {format_size(1024)}")
    print(f"Prueba MB: {format_size(1024 * 1024)}")
    print(f"Prueba GB: {format_size(1024 * 1024 * 1024)}")
    
    print(f"Prueba Sanitizar 1: '{sanitize_str('Video: *Nombre|Inválido?')}'")
    print(f"Prueba Sanitizar 2: '{sanitize_str('   Espacios múltiples    ')}'")
    print(f"Prueba Sanitizar 3: '{sanitize_str('Nombre-Válido_123')}'")
    
    @func_timer
    def prueba_funcion():
        total: int = 0
        for i in range(1000000):
            total += i
    
    prueba_funcion()
    
    
    
    
    
