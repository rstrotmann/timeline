import typer
import pathlib2

from timeline.tlobjects import TlPoint, TlInterval, TlThread, TlHeader, TlSection, TlChart, TlSpacer
from timeline.graphics import viewport
from timeline.tlutils import parse_date, first_of_month, first_of_next_month, tl_colors
from timeline.svg_primitives import svg_symbol
from datetime import date

from timeline.tllexer import lex
from timeline.tlparser import parse_tl

### GLOBAL VARIABLES
__version__ = "0.1.0"
__date__ = "16-June-2024"
debug = False

### MAIN
app = typer.Typer(add_completion=False)

def version_callback(value: bool):
    if value:
        typer.echo(f'version {__version__} ({__date__})')
        raise typer.Exit()

@app.command()
def main(
	file: str = typer.Argument(...),
    outfile: str = typer.Option("", "--output", "-o", help="Output file name"),
	version: bool = typer.Option(False, "--version", help="Show version and exit", callback=version_callback),
    # font: str = typer.Option("Arial", "--font", "-f", help="Font type"),
    # fontsize: float = typer.Option(16, "--fontsize", "-s", help="Font size"),
    debug: bool = typer.Option(False, "--debug", "-d", help="Show debug output"),
	mindate: str = typer.Option(None, "--min-date", "-i", help="Minimum cutoff date"),
    maxdate: str = typer.Option(None, "--max-date", "-x", help="Maximum cutoff date"),
    show_date: bool = typer.Option(True, "--show-date", "-w", help="Show date in label"),
    today: bool = typer.Option(False, "--today", "-t", help="Show today"),
	):
    if outfile == "":
        outfile = pathlib2.Path(file).resolve()
        outfile = outfile.parent.joinpath(outfile.stem + ".svg")
    
    cht = TlChart()
    cht.read_source(file, debug = debug)

    if not mindate:
        mindate = cht.min_date()
    if not maxdate:
        maxdate = cht.max_date()
    # print(mindate, maxdate)
    v = viewport(5, 5, 1200, 0, min_date = mindate, max_date = maxdate, spacing = (0, 5), padding = (5, 5))

    svg_out = cht.render(v, min_date = mindate, max_date = maxdate, include_date = show_date, today = today, debug = False)

    with open(outfile, "w") as f:
        f.write(svg_out)

if __name__ == "__main__":
	app()