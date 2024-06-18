from timeline.tlutils import parse_date, date_string, first_of_month, first_of_next_month, tl_colors, month_names, first_of_year
from timeline.graphics import viewport
from timeline.svg_primitives import svg_symbol, svg_large_arrow, svg_large_arrow_start, svg_large_arrow_middle, svg_large_arrow_end, svg_rect, svg_text, svg_large_arrow_ongoing, svg_large_arrow_abbreviated, svg_large_arrow_end_abbreviated, svg_line
from datetime import datetime
import re
import itertools
from timeline.tllexer import lex
from timeline.tlparser import parse_tl
import pprint
import sys

global_min_date = datetime.strptime("1-Jan-9999", '%d-%b-%Y')
global_max_date = datetime.strptime("1-Jan-2024", '%d-%b-%Y')

class TlObject(object):
    def __init__(self) -> None:
        self.start_date = None
        self.end_date = None

    def __str__(self) -> str:
        pass

    def __repr__(self) -> str:
        pass

    def render(self, viewport: viewport, y = None):
        pass

    def start_x(self, viewport: viewport) -> float:
        return(viewport.date_x(self.start_date))

    def end_x(self, viewport: viewport) -> float:
        return(viewport.date_x(self.end_date))  


class TlPoint(TlObject):
    def __init__(self, date, caption = "", date_format = "%d-%b"):
        self.start_date = parse_date(date)
        self.end_date = self.start_date
        self.caption = caption
        self.keepout_left = -7
        self.keepout_right = 9
        self.date_format = date_format

    def date_label(self):
        return(datetime.strftime(self.start_date, self.date_format))

    def __str__(self):
        return(f'Point ({date_string(self.start_date)}): {self.caption}')
    
    def __repr__(self) -> str:
        return str(self)
    
    def index_date(self):
        return(self.start_date)
    
    def render(self, viewport: viewport, y = None, width = 50):
        if not y:
            y = viewport._height/2
        x = self.start_x(viewport)
        y = y + viewport.y
        return(svg_symbol(x, y, width, "diamond", size = 10))


# class TlRange(TlInterval):
#     def __init__(self, date, caption = ""):
#         pass


class TlInterval(TlObject):
    def __init__(self, start_date, end_date, caption, date_format = "%d-%b", abbreviated = False):
        # print(f'make interval')
        self.start_date = parse_date(start_date)
        self.end_date = parse_date(end_date)
        self.caption = caption
        self.keepout_left = 0
        self.keepout_right = 0
        self.type = "full"
        self.date_format = date_format
        self.abbreviated = abbreviated
        if self.start_date > self.end_date:
            print("----- VALUE ERROR! -----")
            print(f'interval "{self.caption}": start date ({start_date} must be before end data ({end_date})!')
            sys.exit(1)
        
    
    def date_label(self):
        out = datetime.strftime(self.start_date, self.date_format) + " - " + datetime.strftime(self.end_date, self.date_format)
        return(out)

    def __str__(self):
        return(f'Interval ({self.date_label()}): {self.caption}')
    
    def __repr__(self) -> str:
        return str(self)
    
    def index_date(self):
        return(self.start_date)
    
    def render(self, viewport: viewport, x_start = None, x_end = None, y = None, offset_start = 0, offset_end = 0):
        if not y:
            y = viewport._height/2
        if not x_start:
            x_start = self.start_x(viewport) + offset_start
        if not x_end:
            x_end = self.end_x(viewport) + offset_end
        y = y + viewport.y
        if x_start < x_end:
            match self.type:
                case "full":
                    if self.abbreviated:
                        return(svg_large_arrow_abbreviated(x_start, x_end, y, 10)) 
                    else:
                        return(svg_large_arrow(x_start, x_end, y, 10)) 
                case "left":
                    return(svg_large_arrow_start(x_start, x_end, y, 10))
                case "mid":
                    # if x_start < x_end:
                    return(svg_large_arrow_middle(x_start, x_end, y, 10)) 
                    # else:
                    #     return("")
                case "right":
                    if self.abbreviated:
                        return(svg_large_arrow_end_abbreviated(x_start, x_end, y, 10)) 
                    else:
                        return(svg_large_arrow_end(x_start, x_end, y, 10)) 
                case _:
                    return ""
        else:
            return("")
        

def break_interval(ivl, pts):
    # make sure that pts are only points and lie between start and end dates:
    pts = [i for i in pts if (i.start_date < ivl.end_date) & (i.start_date > ivl.start_date) & isinstance(i, TlPoint)]
    pts.append(TlPoint(ivl.end_date))

    # break into list of intervals
    ivls = []
    start = ivl.start_date
    abbr = ivl.abbreviated
    for i, p in enumerate(pts):
        end = p.start_date
        temp = TlInterval(start, end, ivl.caption, abbreviated = abbr)
        if len(pts) == 1: 
            temp.type = "full"
        elif i == 0:
            temp.type = "left"
        elif i == len(pts) - 1:
            temp.type = "right"
        else:
            temp.type = "mid"
        ivls.append(temp)
        start = p.end_date
    # print(f"broken interval: {ivls}")
    return(ivls)


class TlHeader(TlObject):
    def __init__(self, height = 20):
        self._height = height
        self.color = "white"
        self.caption = ""

    def height(self, v: viewport, include_date = True):
        return(v.line_height() * 1.5)

    def x_offset(self, v):
        return(0)
    
    def render(self, v: viewport, x, include_date = True, debug = True) -> str:
        v1 = v.add_viewport(x_offset = x, height = self.height(v))
        grid = [v1.min_date]
        while first_of_next_month(grid[-1]) <= v1.max_date:
            grid.append(first_of_next_month(grid[-1]))
        grid.append(v1.max_date)
        grid = list(set(grid))
        grid.sort()
        out = v1.render_background(debug = debug)
        for i, j in zip(grid, grid[1:]):
            current_color = "#e0e0e0" if (i.month - 1) % 6 < 3 else "transparent"
            out += svg_rect(v1.date_x(i), v1.y, v1.date_x(j) - v1.date_x(i), v1.height, fill_color = current_color, lwd = 1.5)

            label_x = v1.date_x(i) + (v1.date_x(j) - v1.date_x(i))/2 - v1.text_width(month_names[i.month])/2
            label_y = v1.y + v1.height/2 - v1.padding[1] + v1.line_height()/2 + v1.padding[1]*0.5
            out += svg_text(label_x, label_y, month_names[i.month])
        return(out)


class TlThread(object):
    def __init__(self, text_input = None, caption = "", height = 100, color = "transparent"):
        self.objects = []
        self.caption = caption
        self.color = color
        self._height = height
        if text_input:
            self.parse(text_input)

    def __str__(self):
        out = f"THREAD {self.caption}\n"
        for o in self.objects:
            out += str(o) + "\n"
        return(out)

    def min_date(self):
        if not self.objects:
            return(global_min_date)
        return(min([i.start_date for i in self.objects]))
    
    def max_date(self):
        if not self.objects:
            return(global_max_date)
        return(max([i.end_date for i in self.objects]))

    def _vertical_layout(self, v: viewport, include_date = True):
        """
        Return a list of 7 values:
        
        1. top of top label area
        2. bottom of top label area
        3. top of symbol area
        4. bottom of symbol area
        5. top of bottom label area
        6. bottom of bottom label area
        7. bottom of thread drawing area
        """
        ypadding = v.padding[1]
        (top_lbls, bottom_lbls) = self._layout_labels(v, include_date)
        has_top = len(top_lbls) != 0
        has_bottom = len(bottom_lbls) != 0

        top_height = has_top * v.line_height() * (include_date + 1)
        bottom_height = has_bottom * v.line_height() * (include_date + 1)
        mid_height = 20

        y_layout = [ypadding, top_height, ypadding, mid_height, ypadding, bottom_height, ypadding * has_bottom]
        return(list(itertools.accumulate(y_layout)))

    def height(self, v: viewport, include_date = True):
        # temp = self._vertical_layout(v, include_date)
        return(self._vertical_layout(v, include_date)[-1])
    
    def add_object(self, tl_object):
        self.objects.append(tl_object)

    def parse(self, tl: str) -> list:
        out = []
        for l in tl.splitlines():
            m = re.match(r"^\s*([0-9]+-[0-9A-Za-z]+-[0-9]+)(\s->\s([0-9]+-[0-9A-Za-z]+-[0-9]+))?:\s(.*)", l)
            if m:
                if m.groups()[2]:
                    out.append(TlInterval(start_date = parse_date(m.groups()[0]), end_date = parse_date(m.groups()[2]), caption = m.groups()[3]))
                else:
                    out.append(TlPoint(date = parse_date(m.groups()[0]), caption = m.groups()[3]))
        self.objects = out

    def parse_ast(self, ast):
        for i in ast:
            if i[0] == 'point':
                temp = TlPoint(date = i[2], caption = i[1])
            if i[0] == 'interval':
                temp = TlInterval(caption = i[1], start_date = i[2], end_date = i[3])
            self.objects.append(temp)

    def objects_in_viewport(self, viewport: viewport):
        out  = []
        for i in self.objects:
            if i.start_date <= viewport.max_date and i.start_date >= viewport.min_date:
                if i.end_date > viewport.max_date:
                    i.end_date = viewport.max_date
                    i.abbreviated = True
                out.append(i)
        return out
    
    def render_background(self, viewport: viewport) -> str:
        return(svg_rect(viewport.x, viewport.y, viewport.width, viewport._height, fill_color = self.color, line_color = "transparent"))

    def render_caption(self, viewport: viewport, y = None) -> str:
        if not y:
            y = viewport._height/2
        out = svg_text(viewport.x + viewport.padding[0], viewport.y + y, self.caption)
        return(out)

    def render_today(self, v: viewport) -> str:
        today_x = v.date_x(datetime.today())
        return(svg_line(today_x, v.y, today_x, v.y + v.height , color = "red"))

    def render(self, v: viewport, y = None, include_date = True, today = False, debug = False):
        y_layout = self._vertical_layout(v, include_date = include_date)
        y_upper = y_layout[0] + v.line_height() * 0.8
        y_mid = y_layout[2] + 20/2
        y_bottom = y_layout[4] + v.line_height() * 0.8

        out = self.render_background(v)
        if today:
            out += self.render_today(v)

        # render monthgrid
        grid = v.monthgrid()
        for i, j in zip(grid, grid[1:]):
            if (i.month - 1) % 2 < 1:
                out += svg_rect(v.date_x(i), v.y, v.date_x(j) - v.date_x(i), v.height, fill_color = "white", fill_opacity = 0.5, lwd = 0)

        obj = sorted(self.objects_in_viewport(v), key = lambda x: x.start_date)
        pts = [i for i in obj if isinstance(i, TlPoint)]
        pts_dates = [i.start_date for i in pts]

        for i in obj:
            if isinstance(i, TlInterval):
                for j in break_interval(i, pts):
                    offset_start = 8 if j.start_date in pts_dates else 0
                    offset_end = -8 if j.end_date in pts_dates else 0
                    out += j.render(v, y = y_mid, offset_start = offset_start, offset_end = offset_end)
            if isinstance(i, TlPoint):
                out += i.render(v, y = y_mid)
        out += self.render_labels(v, include_date, upper_label_y = y_upper, lower_label_y = y_bottom)

        if debug:
            out += self.render_layout(v, include_date)
        return(out)

    def _layout_labels(self, v: viewport, include_date = True):
        lbls = list()
        for i in self.objects_in_viewport(v):
            caption = (i.date_label(), i.caption)
            if include_date:
                w = max([v.text_width(i) for i in caption])
            else:
                w = v.text_width(i.caption)
            x_offset = v.text_width("0") if isinstance(i, TlPoint) else 0
            lbls.append((
                caption,
                w,
                i.start_x(v) - x_offset,
                i.end_x(v) - x_offset))
        lbls.sort(key = lambda x: x[2])

        out_top = [("dummy", 0, 0, 0, "")]
        out_bottom = [("dummy", 0, 0, 0, "")]
        for l in lbls:
            (l_caption, l_width, l_start, l_end) = l
            last_top_x = max([i[2] + i[1] for i in out_top])
            last_bottom_x = max([i[2] + i[1] for i in out_bottom])
            if last_top_x < l_start:
                out_top.append((l_caption, l_width, l_start, l_end, "left"))
            elif last_bottom_x < l_start:
                out_bottom.append((l_caption, l_width, l_start, l_end, "left"))
        return((out_top[1:], out_bottom[1:]))

    def render_labels(self, v: viewport, include_date = True, upper_label_y = None, lower_label_y = None) -> str:
        if not upper_label_y:
            upper_label_y = v.line_height() + v.padding[1]
        if not lower_label_y:
            lower_label_y = v._height - v.padding[1] - v.line_height()
        
        upper_label_y += v.y
        lower_label_y += v.y

        (out_top, out_bottom) = self._layout_labels(v, include_date)

        # render labels
        svg_out = ""
        for label_y, label_list in [(upper_label_y, out_top), (lower_label_y, out_bottom)]:
            for (i_caption, _i_width, i_start, _i_end, _i_alignment) in label_list: 
                y = label_y
                if include_date:
                    svg_out += svg_text(i_start, y, i_caption[0]) 
                    y += v.line_height()
                svg_out += svg_text(i_start, y, i_caption[1])
        return(svg_out)

    def render_layout(self, v: viewport, include_date = True):
        y_layout = self._vertical_layout(v, include_date = include_date)
        out = ""
        for i in y_layout:
            out += svg_line(v.x, v.y + i, v.x + v.width, v.y + i, lwd = 0.5)
        return(out)


class TlMonthscale(TlThread):
    def __init__(self):
        TlThread.__init__(self)

    def height(self, v: viewport, include_date = True):
        return(v.line_height() * 1.3)

    def render(self, v: viewport, include_date = True, today = False, debug = False):
        grid = v.monthgrid()

        out = svg_rect(v.x, v.y, v.width, self.height(v), fill_color = "white", lwd = 0)
        for i, j in zip(grid, grid[1:]):
            current_color = "#e0e0e0" if (i.month - 1) % 6 < 3 else "white"
            out += svg_rect(v.date_x(i), v.y, v.date_x(j) - v.date_x(i), self.height(v), fill_color = current_color, lwd = 1.5)
            
            label_x = v.date_x(i) + (v.date_x(j) - v.date_x(i))/2 - v.text_width(month_names[i.month])/2
            label_y = v.y + v.height/2 - v.padding[1] + v.line_height()/2 + v.padding[1]* 0.5
            out += svg_text(label_x, label_y, month_names[i.month])
        return(out)


class TlYearscale(TlMonthscale):
    def __init__(self):
        TlThread.__init__(self)
        self.color = "white"

    def render(self, v: viewport, include_date = True, today = False, debug = False):
        grid =  list(set([first_of_year(i) for i in v.monthgrid()] + [v.min_date]))
        # print(grid)
        out = self.render_background(v)
        for i in grid:
            label_y = v.y + v.height/2 - v.padding[1] + v.line_height()/2 + v.padding[1] * 0.5
            if i >= v.min_date and i < v.max_date:
                out += svg_text(v.date_x(i) + v.padding[0], label_y, i.year)
                if i.month == 1 and i.day == 1:
                    out += svg_line(v.date_x(i), v.y, v.date_x(i), v.y + v.height)
        return(out)


class TlSection(object):
    def __init__(self, caption = "", height = 0, color = "transparent"):
        self.threads = []
        self.caption = caption
        self.color = color
        self._height = height

    def __str__(self):
        out = f"SECTION {self.caption}\n"
        for t in self.threads:
            out += str(t) + "\n"
        return(out)
    
    def min_date(self):
        if not self.threads:
            return(global_min_date)
        return(min([i.min_date() for i in self.threads]))
    
    def max_date(self):
        if not self.threads:
            return(global_max_date)
        return(max(i.max_date() for i in self.threads))

    def height(self, v: viewport, include_date = True):
        return(sum([i.height(v, include_date = include_date) for i in self.threads]))
    
    def add_thread(self, thread):
        self.threads.append(thread)
        pass

    def x_offset(self, v: viewport):
        return(max([v.text_width(i.caption + "xx") for i in self.threads] + [v.text_width(self.caption)]) + v.padding[0] * 2)

    def render(self, v: viewport, x, y = None, include_date = True, today = False, debug = False):
        out = ""
        out += svg_text(x = v.x + v.padding[0], y = v.y + v.line_height() * 1.5, text = self.caption, font_weight="bold")

        for i in self.threads:
            temp = v.add_viewport(x_offset = x, height = i.height(v, include_date = include_date), padding = v.padding, spacing = v.spacing)
            out += temp.render_background(debug = debug)
            out += i.render(temp, include_date = include_date, today = today, debug = debug)
            vlayout = i._vertical_layout(temp, include_date = include_date)
            out += svg_text(v.x + v.padding[0] + v.text_width("xx"), temp.y + (vlayout[2] + vlayout[3])/2 + temp.line_middle(), i.caption)

        svg_out = svg_rect(v.x, v.y, v.width, v.height, fill_color = self.color, lwd = 0)
        
        # # render monthgrid
        # grid = v.monthgrid()
        # for i, j in zip(grid, grid[1:]):
        #     if (i.month - 1) % 2 < 1:
        #         svg_out += svg_rect(v.date_x(i), v.y, v.date_x(j) - v.date_x(i), v.height, fill_color = "white", fill_opacity = 0.5, lwd = 0)

        svg_out +=  out
        return(svg_out)


class TlSpacer(TlSection):
    def __init__(self, height = 0):
        TlSection.__init__(self, caption = "", height = height)


    def height(self, v: viewport, include_date = False):
        return(self._height)

    def x_offset(self, v):
        return(0)
    
    def render(self, v: viewport, x, y = None, include_date = False, today = False, debug = False):
        temp = v.add_viewport(0, self.height(v))
        out = ""
        if debug:
            out = temp.render_background(debug = debug)
        return(out)


class TlChart(object):
    def __init__(self, text_input = None, x = 5, y = 5, width = 1200, height = 600, min_date = None, max_date = None):
        self.sections = []
        temp = TlSection()
        temp.add_thread(TlYearscale())
        temp.add_thread(TlMonthscale())
        self.add_section(temp)
        self.add_section(TlSpacer(height = 5))

    def __str__(self):
        out = "CHART\n"
        for s in self.sections:
            out += str(s) + "\n"
        return(out)

    def add_section(self, section = None, text_input = None):
        if section:
            self.sections.append(section)

    def x_offset(self, v: viewport):
        return(max([i.x_offset(v) for i in self.sections]))

    def min_date(self):
        return(min([i.min_date() for i in self.sections]).strftime("%d-%m-%Y"))

    def max_date(self):
        return(max([i.max_date() for i in self.sections]).strftime("%d-%m-%Y"))

    def render(self, v: viewport, include_date = True, min_date = None, max_date = None, today = False, debug = True):
        if not min_date:
            min_date = min([i.min_date() for i in self.sections])
        else:
            min_date = parse_date(min_date)
        if not max_date:
            max_date = max([i.max_date() for i in self.sections])  
        else:
            max_date = parse_date(max_date)
        v.min_date = first_of_month(min_date)
        v.max_date = first_of_next_month(max_date)        
        out = ""
        for i in self.sections:
            temp = v.add_viewport(x_offset = 0, padding = v.padding, spacing = (0, 0))
            out += i.render(temp, self.x_offset(v) + v.padding[1] * 2, include_date = include_date, today = today, debug = debug)

        svg_out = v.render_svg_header()
        if debug:
            svg_out += v.render_background(debug = debug)
        svg_out += out + v.render_svg_footer()
        return(svg_out)
    
    def parse(self, tl_code: str, debug = False):
        temp = "BEGIN" + tl_code + "END"
        lex(temp, debug = debug)
        ast, symbols = parse_tl(temp, debug = debug)

        if debug:
            pprint.pprint(ast)

        for section in ast[1]:
            temp_section = TlSection(caption = section[1], color = tl_colors[section[2]])
            for thread in section[3]:
                temp_thread = TlThread(caption = thread[1], color=temp_section.color)
                for item in thread[2]:
                    if(item[0] == 'point'):
                        temp_thread.add_object(TlPoint(date = item[2], caption = item[1]))
                    if(item[0] == 'interval'):
                        temp_thread.add_object(TlInterval(caption = item[1], start_date = item[2], end_date = item[3]))
                temp_section.add_thread(temp_thread)
            self.add_section(temp_section)

    def read_source(self, infile, outfile = None, debug = False):
        try: 
            with open(infile) as f:
                # temp = yaml.safe_load(f)
                temp = f.read()
                if debug:
                    print(temp)
        except FileNotFoundError as err:
            raise(FileNotFoundError(f'Source file {infile} does not exist'))
        # except Exception as err:
        #     raise KeyError(f'Could not parse {infile}')
        self.parse(temp, debug = debug)