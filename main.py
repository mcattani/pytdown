from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

from get_video_info import get_video_info, VideoInfo
from download_video import download_video

console = Console()

def main():
    url = Prompt.ask("[bold green]Introduce la URL del video[/bold green]")
    video: VideoInfo = get_video_info(url)
    
    # Si no se pudo obtener la información del video, no continuamos
    if not video: 
        console.print("[red]No se pudo obtener la información del video.[/red]")
        return

    console.print(f"[bold]{video.title}[/bold]")
    
    # Crear una tabla con los formatos disponibles
    table = Table(title="Formatos disponibles")
    table.add_column("ID")
    table.add_column("Calidad")
    table.add_column("Ext")
    table.add_column("V-Codec")
    table.add_column("A-Codec")
    table.add_column("Tamaño")
    for item in video.formats:
        table.add_row(item.format_id, item.calidad, item.ext, item.v_codec, item.a_codec, item.f_size)
        
    console.print(table)
    
    format_id: str = Prompt.ask("[bold green]Seleccione el formato[/bold green]")
    
    # Si no se seleccionó un formato, no continuamos
    if not format_id:
        console.print("[red]No se seleccionó un formato.[/red]")
        return
    
    # Descargar el video
    download_video(url, format_id)    

if __name__ == "__main__":
    main()
