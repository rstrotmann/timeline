from timeline.svg_primitives import svg_line, svg_rect, svg_circle, svg_text, svg_path, svg_symbol, svg_large_arrow
from datetime import date
from datetime import datetime
from timeline.tlutils import parse_date, first_of_next_month
from PIL import ImageFont
from matplotlib import font_manager


class viewport:
    def __init__(self, x, y, width, height, min_date: str, max_date: str, font_family = "Arial", font_size = 14, padding = (5,5), spacing = (5, 5), color = "transparent"):
        self.x = x
        self.y = y
        self.width = width
        self._height = height
        self.padding = padding
        self.spacing = spacing
        self.min_date = parse_date(min_date)
        self.max_date = parse_date(max_date)
        self.font_family = font_family
        self.font_size = font_size
        ttf_font = font_manager.FontProperties(family = font_family, weight = 'normal')
        ttf_file = font_manager.findfont(ttf_font)
        self.ifont = ImageFont.truetype(ttf_file, int(font_size))
        self.color = color
        self.viewports = []
        self.lwd = 1.8

    def __str__(self):
        return(f'viewport: x={round(self.x)}, y={round(self.y)}, height={round(self.height)}, width={round(self.width)}')

    def add_viewport(self, x_offset = 0, height = 0, spacing = (5, 5), padding = (5, 5), color = "transparent"):
        next_y = self.y + self.height
        temp = viewport(self.x + self.spacing[0] + x_offset, next_y, self.width - x_offset - 2 * self.spacing[0], height, self.min_date.strftime("%d-%m-%Y"), self.max_date.strftime("%d-%m-%Y"), self.font_family, self.font_size, padding, spacing, color = color)
        self.viewports.append(temp)
        return(temp)

    def monthgrid(self):
        grid = [self.min_date]
        while first_of_next_month(grid[-1]) <= self.max_date:
            grid.append(first_of_next_month(grid[-1]))
        grid.append(self.max_date)
        grid = list(set(grid))
        grid.sort()
        return(grid)

    @property
    def height(self):
        out = self._height + sum([i.height + self.spacing[1] for i in self.viewports])
        return(out)

    def line_height(self) -> float:
        _ascent, descent = self.ifont.getmetrics()
        text_height = self.ifont.getmask("X").getbbox()[3] + descent
        return(text_height * 1.2)

    def line_middle(self) -> float:
        _ascent, descent = self.ifont.getmetrics()
        (width, baseline), (offset_x, offset_y) = self.ifont.font.getsize("Altyq")
        return((_ascent - offset_y)/2)

    def text_width(self, text: str) -> float:
        return(self.ifont.getlength(text))
    
    def width_days(self):
        return((self.max_date - self.min_date).days)

    def _render_outline(self):
        out = svg_rect(self.x, self.y, self.width, self.height)
        for i in self.viewports:
            out += i._render_outline()
        return(out)
        
    def render_background(self, debug = False):
        out = ""
        if debug:
            out += self._render_outline()
        out += svg_rect(self.x, self.y, self.width, self.height, fill_color = "#f0f0f0", lwd = 0)
        for i in self.viewports:
            out += i.render_background(debug = debug)
        return(out)
    
    def date_x(self, d: date):
        if not d >= self.min_date and d <= self.max_date:
            return(None)
        temp = (d - self.min_date).days / (self.max_date - self.min_date).days
        pos = temp * self.width + self.x
        return(pos)
    
    def render_svg_header(self):
        svg_out = f'<svg width="{self.width + self.x + 2 * self.spacing[0] + 10}" height="{self.height + self.y + self.spacing[1] + 10}" viewbox="0 0 {self.width + self.spacing[0] * 2} {self.height/self.width}" xmlns="http://www.w3.org/2000/svg">\n'
        svg_out += f'<style>text {{font-family: {self.font_family}; font-size: {self.font_size}px ;}}</style>\n'
        return(svg_out)

    def render_svg_footer(self):
        svg_out = "</svg>"
        return(svg_out)
