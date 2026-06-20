from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

from pytdown.get_video_info import get_video_info, VideoInfo, FormatInfo
from pytdown.download_video import download_video

from pytdown.utils import check_ffmpeg

console = Console()

def run_app():
    url = Prompt.ask("[bold green]Introduce la URL del video[/bold green]")
    
    # Validación básica de URL
    if not url.startswith(("http://", "https://")):
        console.print("[red]Error: La URL introducida no parece válida.[/red]")
        return

    video: VideoInfo | None = get_video_info(url)
    
    # Si no se pudo obtener la información del video, no continuamos
    if not video: 
        return

    console.print(f"\n[bold blue]Título:[/bold blue] {video.title}")
    
    # Crear una tabla con los formatos disponibles
    table = Table(title="Formatos disponibles")
    table.add_column("ID", style="cyan")
    table.add_column("Resol.", style="magenta")
    table.add_column("FPS", justify="center")
    table.add_column("Ext", style="green")
    table.add_column("Codec")
    table.add_column("Tamaño", justify="right")
    
    # Guardamos los IDs válidos para validar la entrada
    valid_ids: list[str] = []
    for item in video.formats:
        
        # Si el formato incluye audio, mostramos el código de audio
        if item.has_audio:
            codec = f"{item.v_codec} / {item.a_codec}"
        else:
            codec = item.v_codec
        
        # Armamos la fila de la tabla
        table.add_row(
            item.format_id, 
            item.calidad, 
            str(item.fps) if item.fps is not None else "-",
            item.ext,
            codec,
            item.f_size
        )
        
        valid_ids.append(item.format_id)
        
    console.print(table)
    
    # Mostramos la opción de descargar el video
    format_id: str = Prompt.ask(
        "[bold green]Seleccione el ID del formato[/bold green]",
        choices=valid_ids,
        show_choices=False
    )
    
    selected_format: FormatInfo | None = None
    
    # Buscamos el formato seleccionado
    for item in video.formats:
        if item.format_id == format_id:
            selected_format = item
            break
    
    # Comprobamos si es necesario ffmpeg para descargar el formato
    if selected_format and not selected_format.has_audio:
        if not check_ffmpeg():
            console.print("[red]No se encontró ffmpeg en el sistema. Es necesario para descargar este formato.[/red]")
            return
        
    # Descargar el video pasando el idioma original
    if download_video(url, format_id, video.original_lang):
        console.print("\n[bold green]Descarga completada[/bold green]")
    else:
        console.print("\n[bold red]La descarga no se completó.[/bold red]")

def main():
    try:
        run_app()
    except KeyboardInterrupt:
        console.print("\n[bold red]Programa terminado por el usuario.[/bold red]")

if __name__ == "__main__":
    main()
