import re
from datetime import date, datetime, timedelta

month_names = ["", "J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"]
tl_colors = {"transparent": "#ffffff", "white": "#ffffff", "red": "#fbd8ea", "blue": "#c4e2fa", "yellow": "#fff4d6", "violet": "#dad0ef", "green": "#edf5dc", "aqua": "#d4f3f6", "grey": "#f0f0f0"}
tl_fill_colors = {"transparent": "#ffffff", "white": "#ffffff", "red": "#ff0000", "blue": "#c4e2fa", "yellow": "#FFC833", "violet": "#503291", "green": "#0f7447", "aqua": "#2CBECD", "black":"#000000"}

def parse_date(d) -> date:
    if isinstance(d, date) or isinstance(d, datetime):
        return(d)
    else:
        for fmt in ('%d-%b-%Y', '%d-%b-%y', '%d-%m-%Y', '%d-%m-%y'):
            try:
                return datetime.strptime(d, fmt)
            except ValueError:
                pass
        raise ValueError(f'not a valid date ({d})')

def date_string(d: date) -> str:
    return d.strftime("%d-%b-%Y")

def first_of_month(d: datetime) -> datetime:
    return(datetime.strptime(f'{d.year}-{d.month}-01', "%Y-%m-%d"))

def first_of_next_month(d: datetime) -> datetime:
    return(first_of_month(first_of_month(d) + timedelta(32)))

def first_of_year(d: datetime) -> datetime:
    return(datetime.strptime(f'{d.year}-01-01', '%Y-%m-%d'))

def convert_str_to_dict(input: str) -> dict:
    temp = re.findall(r'(\w*)\:\s*(\w*)', input)
    out = {i[0]: i[1] for i in temp}
    return(out)

def validate_parameters(parameter: dict):
    # validate colors
    for i in ["color", "fill"]:
        temp_col = parameter.get(i, "transparent")
        if not temp_col in tl_colors.keys():
            raise ValueError(f"unknown color '{temp_col}'")