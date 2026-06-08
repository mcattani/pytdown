# download_video.py
# Este módulo se se encarga de descargar el video, utiliza tkinter para crear una ventana de diálogo para elegir carpeta de descarga.

from pathlib import Path
from tkinter import Tk
from tkinter.filedialog import askdirectory
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError
from rich.progress import (
    Progress,
    BarColumn,
    DownloadColumn,
    TransferSpeedColumn,
    TimeRemainingColumn,
    TextColumn,
)

def select_download_folder() -> str | None:
    """
    Muestra una ventana de diálogo para seleccionar carpeta de descarga.
    Devuelve:
        str -> ruta seleccionada
        None -> si el usuario cancela
    """
    # Creamos la ventana principal de tkinter
    root = Tk()
    
    # La ocultamos 
    root.withdraw()
    
    # Mostramos el selector de carpeta
    folder = askdirectory(title="Seleccione carpeta de descarga")
    
    # Cerramos tkinter
    root.destroy()
    
    # Devuelve la carpeta elegida o none si el usuario cancela
    return folder or None

if __name__ == "__main__":
    # Bloque de ejecución principal para pruebas manuales    
    # print(select_download_folder())
    
    