# download_video.py
# Este módulo se se encarga de descargar el video, utiliza tkinter para crear una ventana de diálogo para elegir carpeta de descarga.

import deno
from typing import Any
from pathlib import Path
from tkinter import Tk
from tkinter.filedialog import askdirectory
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError
from rich.progress import (
    Progress,
    BarColumn,
    DownloadColumn,
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


def download_video(url: str, format_id: str) -> bool:
    """
    Descarga un video usando yt-dlp.

    Parámetros:
        url: URL del video
        format_id: ID del formato elegido

    Devuelve:
        True  -> descarga exitosa
        False -> error o cancelación
    """
    # Solicitamos la carpeta destino y validamos
    download_dir = select_download_folder()
    if not download_dir: return False
    
    # Definimos cómo se verá la barra de progreso
    progress = Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        "[progress.percentage]{task.percentage:>3.0f}%",
        DownloadColumn(),
    )
    
    # Rich identifica cada barra mediante un ID. Al principio todavía no existe ninguna barra.
    task_id = None
    
    def progress_hook(data):
        """
        Esta función es llamada automáticamente por yt-dlp
        durante la descarga.
        """
        nonlocal task_id
        
        if data["status"] == "downloading":
            # Intentamos obtener el tamaño total (real o estimado)
            total = data.get("total_bytes") or data.get("total_bytes_estimate")
            downloaded = data.get("downloaded_bytes", 0)

            # Si la barra no existe, la creamos (incluso si total es None)
            if task_id is None:
                task_id = progress.add_task(description="Descargando...", total=total)
            
            # Rich maneja automáticamente si total es None (barra indeterminada)
            # y se ajusta si el total cambia durante la descarga.
            progress.update(task_id, completed=downloaded, total=total)
            
        elif data["status"] == "finished":
            if task_id is not None:
                # Al terminar, nos aseguramos de que la barra llegue al 100% 
                # usando el tamaño total real descargado.
                total = data.get("total_bytes") or data.get("downloaded_bytes")
                progress.update(task_id, description="Completado", completed=total, total=total)

    # Configuramos yt-dlp
    ydl_opts: dict[str, Any]= {
        "format": format_id,
        "outtmpl": str(Path(download_dir) / "%(title)s.%(ext)s"),
        "progress_hooks": [progress_hook],
        "js_runtimes": {"deno": {"path": deno.find_deno_bin()}},
        "quiet": True,
        "no_warnings": True,
        "noprogress": True, # Evita que yt-dlp intente mostrar su propia barra
    }
    
    try:
        with progress:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        return True
    except DownloadError as e:
        print(f"Error al descargar el video: {e}")
        return False

if __name__ == "__main__":
    # Bloque de ejecución principal para pruebas manuales    
    #print(select_download_folder())
    
    URL_PRUEBA: str = "https://www.youtube.com/watch?v=wxaXWSVhRXU"
    download_video(URL_PRUEBA, "18")
    
    