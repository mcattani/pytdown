from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

from pytdown.get_video_info import get_video_info, VideoInfo
from pytdown.download_video import download_video

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
        # El error específico ya se imprime dentro de get_video_info
        return

    console.print(f"\n[bold blue]Título:[/bold blue] {video.title}")
    
    # Crear una tabla con los formatos disponibles
    table = Table(title="Formatos disponibles (Video + Audio)")
    table.add_column("ID", style="cyan")
    table.add_column("Calidad", style="magenta")
    table.add_column("Ext", style="green")
    table.add_column("V-Codec")
    table.add_column("A-Codec")
    table.add_column("Tamaño", justify="right")
    
    # Guardamos los IDs válidos para validar la entrada después
    valid_ids: list[str] = []
    for item in video.formats:
        table.add_row(item.format_id, item.calidad, item.ext, item.v_codec, item.a_codec, item.f_size)
        valid_ids.append(item.format_id)
        
    console.print(table)
    
    # Usamos choices para que rich valide que el ID sea uno de la lista
    format_id: str = Prompt.ask(
        "[bold green]Seleccione el ID del formato[/bold green]",
        choices=valid_ids,
        show_choices=False
    )
    
    # Descargar el video y dar feedback final
    if download_video(url, format_id):
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
    
