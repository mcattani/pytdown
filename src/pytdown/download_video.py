# download_video.py
# Este módulo se se encarga de descargar el video, utiliza tkinter para crear una ventana de diálogo para elegir carpeta de descarga.

import deno
from typing import Any
from pathlib import Path
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError
from rich.progress import (
    Progress,
    BarColumn,
    DownloadColumn,
    TextColumn,
)
from rich.console import Console

console = Console()

def select_download_folder() -> str | None:
    """
    Intenta usar Tkinter para seleccionar carpeta de descarga.
    Si no está instalado, recurre a una entrada de texto por consola.
    
    Devuelve:
        str -> ruta seleccionada
        None -> si el usuario cancela
    """
    try: 
        from tkinter import Tk
        from tkinter.filedialog import askdirectory

        root = Tk() # Creamos la ventana principal de tkinter
        root.withdraw() # La ocultamos 
        folder = askdirectory(title="Seleccione carpeta de descarga") # Mostramos el selector de carpeta
        root.destroy() # Cerramos tkinter
        
        if folder: return folder
        # Si el usuario cancela (ctrl+c)
        return None
    except (ImportError, ModuleNotFoundError):
        # Si no se encuentra tkinter o no está instalado, recurre a una entrada de texto por consola.
        console.print("[yellow]Aviso: No se pudo cargar la interfaz gráfica (Tkinter).[/yellow]")
        from rich.prompt import Prompt
        folder_str = Prompt.ask("Introduce la ruta de la carpeta de descarga (deja vacío para la carpeta actual)")
        
        # Si no se introduce ninguna ruta usamos la carpeta actual
        if not folder_str: 
            return str(Path.cwd())
        
        # Validamos la ruta introducida
        path_obj = Path(folder_str)
        if path_obj.is_dir(): 
            return str(path_obj.absolute())
        else:
            console.print("[red]La ruta introducida no es una carpeta válida.[/red]")
            return None

def download_video(url: str, format_id: str, original_lang: str | None = None) -> bool:
    """
    Descarga un video usando yt-dlp.

    Parámetros:
        url: URL del video
        format_id: ID del formato elegido
        original_lang: Código del idioma original del video (opcional)

    Devuelve:
        True  -> descarga exitosa
        False -> error o cancelación
    """
    # Solicitamos la carpeta destino y validamos
    download_dir = select_download_folder()
    if not download_dir: 
        return False
    
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

    # Prioriza el audio que coincida con el idioma original
    # Si tenemos el código de idioma, forzamos a yt-dlp a buscar esa pista primero.
    if original_lang:
        format_spec = f"{format_id}+bestaudio[language={original_lang}]/bestaudio/best"
    else:
        format_spec = f"{format_id}+bestaudio/best"

    # Configuramos yt-dlp
    ydl_opts: dict[str, Any]= {
        "format": format_spec,
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
    # Si el usuario cancela (ctrl+c)
    except KeyboardInterrupt:
        console.print("\n[yellow]Descarga cancelada por el usuario.[/yellow]")
        return False
    # Captura error en descarga
    except DownloadError as e:
        console.print(f"[red]Error al descargar el video:[/red] {e}")
        return False
    # Captura otros errores
    except Exception as e:
        console.print(f"[red]Error inesperado:[/red] {e}")
        return False

if __name__ == "__main__":
    # Bloque de ejecución principal para pruebas manuales    
    #print(select_download_folder())
    
    URL_PRUEBA: str = "https://www.youtube.com/watch?v=sPQhTXeoiw0"
    download_video(URL_PRUEBA, "137", "es")
