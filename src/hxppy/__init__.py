import re
import argparse
from pathlib import Path
import pathspec
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.panel import Panel

console = Console()

HEADER_PATTERN = re.compile(r"^===== (.+) =====$")
DEFAULT_ARCHIVE_NAME = "hxppy_backup.txt"

ASCII_LOGO = r"""
  _    _                      _ 
 | |  | |                    | |
 | |__| |_  _ __  _ __  _   _| |
 |  __  | \/ | '_ \| '_ \| | | |
 | |  | |>  <| |_) | |_) | |_| |
 |_|  |_/_/\_\ .__/| .__/ \__, |
             | |   | |     __/ |
             |_|   |_|    |___/ 
      [ Archivator v0.1.0 ]
"""


def load_gitignore_spec(root: Path):
    gitignore_path = root / ".gitignore"
    if not gitignore_path.exists():
        return None
    try:
        lines = gitignore_path.read_text(encoding="utf-8").splitlines()
        return pathspec.PathSpec.from_lines("gitwildmatch", lines)
    except Exception as e:
        console.print(f"[yellow][WARN][/yellow] Не удалось прочитать .gitignore: {e}")
        return None


def is_ignored(path: Path, root: Path, spec, output_path: Path):
    if path.name == ".git" or path.resolve() == output_path.resolve():
        return True
    if spec is None:
        return False
    try:
        rel = path.relative_to(root).as_posix()
        return spec.match_file(rel)
    except ValueError:
        return False


def pack_files(output_path: Path):
    root = Path.cwd()
    spec = load_gitignore_spec(root)
    files_to_pack: list[Path] = []

    for p in root.rglob("*"):
        if p.is_file() and not is_ignored(p, root, spec, output_path):
            files_to_pack.append(p)

    console.print(
        Panel(
            f"[bold green]📦 Начинаем упаковку[/bold green]\nВыходной файл: [cyan]{output_path}[/cyan]"
        )
    )

    if not files_to_pack:
        console.print("[yellow]⚠️ Нет файлов для упаковки![/yellow]")
        return

    count = 0
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console,
    ) as progress:
        task = progress.add_task(
            description="Упаковка файлов...", total=len(files_to_pack)
        )

        with output_path.open("w", encoding="utf-8") as out:
            for p in files_to_pack:
                rel_path = p.relative_to(root).as_posix()
                out.write(f"===== {rel_path} =====\n")
                try:
                    text = p.read_text(encoding="utf-8", errors="replace")
                    out.write(text + "\n\n")
                    count += 1
                except Exception as e:
                    out.write(f"[Ошибка чтения файлов: {e}]\n\n")

                progress.update(
                    task, advance=1, description=f"Добавлен: {rel_path[:30]}..."
                )

    console.print(
        f"\n[bold green]✅ Готово![/bold green] Упаковано файлов: [bold]{count}[/bold]"
    )


def unpack_files(input_path: Path):
    if not input_path.exists():
        console.print(f"[bold red]❌ Ошибка:[/bold red] Файл '{input_path}' не найден.")
        return

    root = Path.cwd()
    console.print(
        Panel(
            f"[bold blue]📂 Распаковка[/bold blue]\nИз файла: [cyan]{input_path}[/cyan]"
        )
    )

    current_file_path = None
    content_buffer: list[str] = []
    count = 0

    with input_path.open("r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        match = HEADER_PATTERN.match(line.strip())
        if match:
            if current_file_path:
                _save_file(current_file_path, content_buffer)
                count += 1

            new_path_str = match.group(1)
            current_file_path = root / new_path_str
            content_buffer = []
        else:
            if current_file_path:
                content_buffer.append(line)

    if current_file_path:
        _save_file(current_file_path, content_buffer)
        count += 1

    console.print(
        f"[bold green]✅ Распаковка завершена![/bold green] Создано файлов: [bold]{count}[/bold]"
    )


def _save_file(path: Path, buffer: list[str]):
    path.parent.mkdir(parents=True, exist_ok=True)
    content = "".join(buffer).rstrip()
    path.write_text(content, encoding="utf-8")


def main():
    console.print(f"[bold magenta]{ASCII_LOGO}[/bold magenta]")
    
    parser = argparse.ArgumentParser(
        description="hxppy-archivator: упаковка проекта в один TXT"
    )
    parser.add_argument(
        "mode", choices=["pack", "p", "unpack", "u"], help="Режим: pack или unpack"
    )
    parser.add_argument(
        "-f", "--file", type=Path, default=Path(DEFAULT_ARCHIVE_NAME), help="Имя архива"
    )

    args = parser.parse_args()
    if args.mode == "pack" or args.mode == "p":
        pack_files(args.file)
    else:
        unpack_files(args.file)


if __name__ == "__main__":
    main()
