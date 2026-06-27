from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

from pytdown.get_video_info import get_video_info, VideoInfo, FormatInfo
from pytdown.download_video import download_video

from pytdown.utils import check_ffmpeg

console = Console()

def create_format_table(formats: list[FormatInfo]) -> dict[str, str]:
    """
    Crea un diccionario que relaciona el número de formato con su ID de yt-dlp
    """
    format_map = {}
    for index, item in enumerate(formats, start=1):
        format_map[str(index)] = item.format_id
    return format_map
    

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
    
    # Creamos un diccionario para mapear el número de formato con su ID de yt-dlp
    format_map = create_format_table(video.formats)

    console.print(f"\n[bold blue]Título:[/bold blue] {video.title}")
    
    # Crear una tabla con los formatos disponibles
    table = Table(title="Formatos disponibles")
    table.add_column("#", style="cyan", justify="center")
    table.add_column("Resol.", style="magenta", justify="center")
    table.add_column("FPS", justify="center")
    table.add_column("Ext", style="green")
    table.add_column("Codec")
    table.add_column("Tamaño")
    
    # Detectamos FFmpeg UNA sola vez
    ffmpeg_available = check_ffmpeg()

    for index, item in enumerate(video.formats, start=1):
        
        # Si el formato incluye audio, mostramos el código de audio
        if item.has_audio:
            codec = f"{item.v_codec}/{item.a_codec}"
        else:
            codec = item.v_codec
        
        display_id: str = str(index)
        row_style = ""

        # Solo marcamos si requiere ffmpeg Y NO está instalado
        if item.requires_ffmpeg and not ffmpeg_available:
            display_id = f"[bold red]* {display_id}[/bold red]"
            row_style = "dim"
        
        # Armamos la fila de la tabla
        table.add_row(
            display_id,
            item.calidad, 
            str(item.fps) if item.fps is not None else "-",
            item.ext,
            codec,
            item.f_size,
            style=row_style
        )
        
    console.print(table)

    # Leyenda solo si fmpeg no está instalado
    if not ffmpeg_available:
        console.print("[dim]* Requiere ffmpeg para ser descargado[/dim]\n")
    
    # Mostramos la opción de descargar el video
    option: str = Prompt.ask(
        "[bold green]Seleccione una opción[/bold green]",
        choices=list(format_map.keys()),
        show_choices=False
    )
    
    # Obtenemos el formato seleccionado
    format_id = format_map[option]
    
    selected_format: FormatInfo | None = None
    
    # Buscamos el formato seleccionado
    for item in video.formats:
        if item.format_id == format_id:
            selected_format = item
            break
    
    # Comprobamos si es necesario ffmpeg para descargar el formato
    if selected_format and selected_format.requires_ffmpeg:
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