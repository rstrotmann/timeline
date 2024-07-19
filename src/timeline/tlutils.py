import re
from datetime import date, datetime, timedelta
import matplotlib.colors as colors

month_names = ["", "J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"]
tl_colors = {"transparent": "#ffffff", "white": "#ffffff", "red": "#fbd8ea", "blue": "#c4e2fa", "yellow": "#fff4d6", "violet": "#dad0ef", "green": "#edf5dc", "aqua": "#d4f3f6", "grey": "#f0f0f0"}

tl_contrast_colors = {"transparent": "#ffffff", "white": "#ffffff", "red": "#F8BBDA", "blue": "#A5D3F7", "yellow": "#FFE5A0", "violet": "#C8B9E7", "green": "#D8E9B3", "aqua": "#B2E9EF", "grey": "#DCDCDC"}

tl_strong_colors = {"transparent": "#ffffff", "white": "#ffffff", "red": "#F59BC9", "blue": "#7CBFF4", "yellow": "#FFD769", "violet": "#B39FDE", "green": "#C4DE8B", "aqua": "#82DCE5", "grey": "#C6C6C6"}

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
    temp = re.findall(r'(\w*)\:\s*([\w\.]*)', input)
    out = {i[0]: i[1] for i in temp}
    return(out)

def validate_parameters(parameter: dict):
    # validate colors
    for i in ["color", "fill"]:
        temp_col = parameter.get(i, "transparent")
        if not temp_col in tl_colors.keys():
            raise ValueError(f"unknown color '{temp_col}'")
        

def intensify_color(hex_string):
    temp = colors.hex2color(hex_string)
    # print(f'hex: {hex_string}, rgb: {temp}')
    if temp[0] > max(temp[1:2]):
        i_hi = 0
        if temp[1] > temp[2]:
            i_lo = 2
        else:
            i_lo = 1
    elif temp[2] > max(temp[0:1]):
        i_hi = 2
        if temp[0] > temp[1]:
            i_lo = 1
        else:
            i_lo = 0
    else:
        i_hi = 1
        if temp[0] > temp[2]:
            i_lo = 2
        else:
            i_lo = 0
    out = list(temp)
    out[i_lo] -= 0.2
    # out[i_lo] *= 0.85
    if out[i_lo] < 0:
        out[i_lo] = 0
    out[i_hi] += 0.2
    # out[i_hi] /= 0.85
    if out[i_hi] > 1:
        out[i_hi] = 1
    return colors.rgb2hex(out)