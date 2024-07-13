import typer
import pathlib2
import sys

from timeline.tlobjects import TlPoint, TlInterval, TlThread, TlHeader, TlSection, TlChart, TlSpacer
from timeline.graphics import viewport
from timeline.tlutils import parse_date, first_of_month, first_of_next_month, tl_colors, convert_str_to_dict
from timeline.svg_primitives import svg_symbol
from datetime import date

from timeline.tllexer import lex
from timeline.tlparser import parse_tl

from timeline.graphics import svg_max_x


### GLOBAL VARIABLES
__version__ = "0.1.2"
__date__ = "19-June-2024"
debug = False

### MAIN
app = typer.Typer(add_completion=False)

def version_callback(value: bool):
    if value:
        typer.echo(f'version {__version__} ({__date__})')
        raise typer.Exit()

# @app.command()
# def test():
# #     tl_text = '''
# # section s1
# # thread t1
# # point 1: 1-Jan-26 (color: red)
# # point 2: 1-Feb (fill: blue)
# # point 3: 1-Mar-24
# # point 4: 1-3
# # interval 1: 1-4 - 1-5 (color: red)
# # '''

#     tl_text = '''
# # BEGIN
# source test.tl

# section s2
# thread t2
# point 4: 1-5-25

# SECTION s1 (color: red)
# #color red
# IMPORT study 1 FROM Clinical
# IMPORT * FROM Regulatory

# # THREAD t1
# # point 1: 1-Jan-26 (color: blue)
# # point 2: 1-Feb (fill: blue)
# # thread t2
# # point 3: 1-Mar
# #interval 1: 1-4 - 1-5 (color: green)
# # END
# '''

#     # lex(tl_text, debug = True)
#     # ast, symbols = parse_tl(tl_text, debug = True)
#     # print(ast)
#     # print(symbols)

#     temp = TlChart()
#     temp.parse(tl_text, debug = True)
#     print("------- chart ---------")
#     print(temp)




@app.command()
def main(
	file: str = typer.Argument(...),
    outfile: str = typer.Option("", "--output", "-o", help="Output file name"),
	version: bool = typer.Option(False, "--version", help="Show version and exit", callback=version_callback),
    # font: str = typer.Option("Arial", "--font", "-f", help="Font type"),
    fontsize: float = typer.Option(14, "--fontsize", "-s", help="Font size"),
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

    mindate = parse_date(mindate)
    maxdate = parse_date(maxdate)
    if mindate > maxdate:
        print('----- VALUE ERROR -----')
        print(f'max date must be after min date!')
        sys.exit(1)

    v = viewport(5, 5, 1200, 0, min_date = mindate, max_date = maxdate, spacing = (0, 5), padding = (5, 5), font_size = fontsize)

    svg_out = cht.render(v, min_date = mindate, max_date = maxdate, include_date = show_date, today = today, debug = debug)

    with open(outfile, "w") as f:
        f.write(svg_out)



if __name__ == "__main__":
	app()