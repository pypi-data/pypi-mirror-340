from anime_light.cli.parser import create_parser
from anime_light.cli.commands import process_single_file, process_batch
from anime_light.cli.utils import check_ffmpeg
import sys
import os
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn

console = Console()

def main():
    if not check_ffmpeg():
        sys.exit(1)

    parser = create_parser()
    args = parser.parse_args()

    # Configurar directorios de salida
    output_base_dir = args.output_dir if args.output_dir else os.path.join(
        os.path.dirname(args.input) if os.path.isfile(args.input) else args.input,
        "output"
    )
    output_dir = os.path.join(output_base_dir, args.resolution)
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    if os.path.isfile(args.input):
        # Modo archivo único
        with Progress(
            TextColumn("[bold blue]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
            TextColumn("•"),
            TextColumn("[bold green]{task.fields[filename]}"),
        ) as progress:
            if process_single_file(args.input, output_dir, args.resolution, args.crf, args.preset, progress):
                console.print(f"[green]✓ Conversión completada! Guardado en: {output_dir}")
    
    elif os.path.isdir(args.input):
        # Modo batch
        process_batch(
            input_dir=args.input,
            output_dir=output_dir,
            resolution=args.resolution,
            crf=args.crf,
            preset=args.preset,
            recursive=args.recursive,
            exclude_patterns=args.exclude
        )
        
    else:
        console.print("[red]❌ La ruta no es un archivo ni una carpeta válida.")