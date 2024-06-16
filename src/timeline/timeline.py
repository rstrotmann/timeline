import typer
import pathlib

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

### FUNCTIONS




### MAIN
app = typer.Typer(add_completion=False)

def version_callback(value: bool):
    if value:
        typer.echo(f'version {__version__} ({__date__})')
        raise typer.Exit()

@app.command()
def main(
	# file: str = typer.Argument(...),
    outfile: str = typer.Option("", "--output", "-o", help="Output file name"),
	version: bool = typer.Option(False, "--version", help="Show version and exit", callback=version_callback)
	):
    outfile = "test.svg"

    tl_input1 = """
        1-3-24: MS1
        1-3-24 -> 15-3-24: action 1
        15-3-2024: TEST
        1-Apr-24: MS2
        3-4-24 -> 14-4-24: draft 1
        14-4-24 -> 20-Apr-24: draft 2
        1-5-24 -> 30-6-2024: action2
        15-5-24: coll 1
        1-6-24: coll 2
        15-7-24: MS3
        15-Aug-24 -> 15-Sep-24: long2
    """

    tl_input2 = """
        1-3-24 -> 15.3.24: action 1
        3-4-24 -> 14-4-24: draft 1
        1-5-24 -> 30-6-2024: action2
        7-Jul-2024: label 1
        9-7-24: label 2
        #10-7-24: label 3
        1-7-24 -> 15-9-24: long action
    """

    tl_input3 = """
        1-3-24 -> 15-3-24: action 1
        1-7-24 -> 15-9-24: long action
    """

    # vf = viewframe("1-2-2024", "31-8-2024", sidebar_width=0, padding=(10, 5))
    # vf.sidebar_width = max(vf.text_width(thd1.caption) + vf.padding[0]*2, vf.text_width(thd2.caption) + vf.padding[0]*2)
    # vh = vf.add_viewport(height = 20)
    # v1 = vf.add_viewport(color = tl_colors["red"])
    # v2 = vf.add_viewport(color = tl_colors["yellow"])
    
    # out = vf.render()
    # out += TlHeader().render(vh)
    # out += thd1.render(v1)
    # out += thd2.render(v2)

###################

    v = viewport(5, 5, 1200, 0, "15-12-2023", "15-6-2026", spacing = (0, 5), padding = (5, 5))

    # tlc = TlChart(min_date="1-2-2024", max_date="31-8-2024
    # thead = TlHeader(height = v.line_height())
    thd1 = TlThread(text_input = tl_input1, caption = "upper", color = tl_colors["red"])
    # print(thd1)
    thd2 = TlThread(text_input = tl_input3, caption = "super long thread name", color = tl_colors["red"])
    sct = TlSection(caption = "Section 1", color = tl_colors["red"])
    sct.add_thread(thd1)
    sct.add_thread(thd2)

    cht = TlChart()
    # cht.add_section(TlSpacer(height = 0))
    # cht.add_section(sct)

    # svg_out = cht.render(v, include_date = False, debug = False)

    # with open(outfile, "w") as f:
    #     f.write(svg_out)
    

###################

    test = '''
        section Clinical
        color red

        thread FiH
        Cohort 1: 1-Mar-24 - 1-Apr-24
        SMC 1: 15-Apr-24
        Cohort 2: 21-Apr-24 - 21-May-24
        SMC 2: 31-May-24
        Cohort 3a: 5-Jun-24 - 5-Jul-24
        SMC 3: 18-Jul-24

        thread study 2
        FSI: 1-Aug-2024
        FSFD: 15-Aug-24
        Interim analysis: 15-2-25
        conduct: 15-Aug-2024 - 30-Sep-25
        IDMC1: 30-Sep-24
        IDMC2: 1-Dec-24



        section Regulatory
        color blue
        # comment

        thread FDA interaction

        Briefing Book draft 1: 15-Jun-2024
        BB review 1: 16-Jun-24 - 30-6-24
        BB draft 2:   1-Jul-24
        BB submission: 15.7.24 

        thread Submission
        Dossier final: 31-Aug-2024



        '''


    # lex(test, debug = True)
    # ast, symbols = parse_tl(test, debug = False)
    # print(ast)

    cht.parse(test, debug = True)
    # print(cht)
    
    svg_out = cht.render(v, min_date = "1-Apr-24", max_date = "15-6-26", include_date = False, today = True, debug = False)

    with open(outfile, "w") as f:
        f.write(svg_out)

if __name__ == "__main__":
	app()