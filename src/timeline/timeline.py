import typer
from importlib.metadata import version
import pathlib2
import sys

from timeline.tlobjects import TlChart
from timeline.graphics import viewport
from timeline.tlutils import parse_date


# GLOBAL VARIABLES
debug = False


# __version__ = version("ly1")
app = typer.Typer(add_completion=False, no_args_is_help=True)


def version_callback(value: bool):
    if value:
        typer.echo(f'version {version("timeline")}')
        raise typer.Exit()


@app.command()
def main(
    file: str = typer.Argument(...),
    outfile: str = typer.Option("", "--output", "-o", help="Output file name"),
    version: bool = typer.Option(
        False, "--version", "-v", help="Show version and exit",
        callback=version_callback),
    # font: str = typer.Option("Arial", "--font", "-f", help="Font type"),
    fontsize: float = typer.Option(14, "--fontsize", "-s", help="Font size"),
    debug: bool = typer.Option(
        False, "--debug", "-d", help="Show debug output"),
    mindate: str = typer.Option(
        None, "--min-date", "-i", help="Minimum cutoff date"),
    maxdate: str = typer.Option(
        None, "--max-date", "-x", help="Maximum cutoff date"),
    show_date: bool = typer.Option(
        True, "--show-date", "-w", help="Show date in label"),
        today: bool = typer.Option(False, "--today", "-t", help="Show today")):
    if outfile == "":
        outfile = pathlib2.Path(file).resolve()
        outfile = outfile.parent.joinpath(outfile.stem + ".svg")

    cht = TlChart()
    cht.read_source(file, debug=debug)

    if not mindate:
        mindate = cht.min_date()
    if not maxdate:
        maxdate = cht.max_date()

    mindate = parse_date(mindate)
    maxdate = parse_date(maxdate)
    if mindate > maxdate:
        sys.exit('ERROR: Max date must be after min date!')

    v = viewport(
        5, 5, 1200, 0, min_date=mindate, max_date=maxdate, spacing=(0, 5),
        padding=(5, 5), font_size=fontsize)

    svg_out = cht.render(
        v, min_date=mindate, max_date=maxdate, include_date=show_date,
        today=today, debug=debug)

    with open(outfile, "w") as f:
        f.write(svg_out)


if __name__ == "__main__":
    app()
