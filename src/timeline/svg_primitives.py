

def svg_line(x1, y1, x2, y2, lwd=1.8, outline_color="black", fill_color = "none", dashed=False):
	dash = f'stroke-dasharray: {lwd*3} {lwd*3}' if dashed else ""
	return(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" style="stroke:{outline_color}; stroke-width:{lwd}; {dash}" />\n')

def svg_rect(x, y, w, h, lwd=1, fill_color="none", line_color="black", fill_opacity=0):
    return(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" style="stroke:{line_color};  stroke-width:{lwd}; fill:{fill_color}; fill-opacity:{1 - fill_opacity}" />\n')

def svg_circle(x, y, r, lwd=1.2, fill_color="none", line_color="black"):
	return(f'<circle cx="{x}" cy="{y}" r="{r}" style="stroke:{line_color};  stroke-width:{lwd}; fill:{fill_color};"/>\n')

def svg_text(x, y, text, css_class="", font_weight="normal"):
	if css_class:
		return(f'<text x="{x}" y="{y}" font-weight="{font_weight}" class="{css_class}">{text}</text>\n')
	else:
		return(f'<text x="{x}" y="{y}" font-weight="{font_weight}">{text}</text>\n')

def svg_path(x, y, points, lwd=1.8, size=1, fill=False, dashed=False, fill_color="none", outline_color="black", title=""):
	# print(f'svg_path outline color : {outline_color}')
	dash = "stroke-dasharray: 2.5 2.5" if dashed else ""
	(x1, y1) = points[-1]
	out = f'<path d="M{x1*size+x}, {y1*size+y} '
	for (x2, y2) in points:
		out += f'L{x2*size+x}, {y2*size+y} '
	out += f'Z" style="stroke: {outline_color}; fill: {fill_color}; stroke-width:{lwd}; {dash}"'
	if title != "":
		out += f'><title>{title}</title></path>\n'
	else:
		out += ' />\n'
	return(out)

def svg_open_path(x, y, points, lwd=1.8, size=1, fill=False, dashed=False, fill_color="none", outline_color="black", title=""):
	dash = "stroke-dasharray: 2.5 2.5" if dashed else ""
	(x1, y1) = points[0]
	out = f'<path d="M{x1*size+x}, {y1*size+y} '
	for (x2, y2) in points[1:]:
		out += f'L{x2*size+x}, {y2*size+y} '
	out += f'" style="stroke: {outline_color}; fill: {fill_color}; stroke-width:{lwd}; {dash}"'
	if title != "":
		out += f'><title>{title}</title></path>\n'
	else:
		out += ' />\n'
	return(out)

def svg_symbol(x, y, width, symbol, size=1, fill=False, outline_color = "black", fill_color = "none", **kwargs):
    if symbol == "diamond":
        return svg_path(x, y, [(0, -0.5), (0.25, 0), (0, 0.5), (-0.25, 0)], size=size*1.4, fill=fill, fill_color=fill_color, outline_color = outline_color, **kwargs)
    elif symbol == "block":
        w = width/size/1.5*.7
        return svg_path(x, y, [(w/-2, -.25), (w/2, -.25), (w/2, .25), (-w/2, .25)], size=size*1.5, fill=fill, fill_color=fill_color, outline_color = outline_color, **kwargs)
    elif symbol == "arrow":
        return svg_path(x, y, [(-0.03, -0.5), (0.03, -0.5), (0.03, 0), (0.1875, 0), (0.0, 0.5), (-0.1875, 0), (-0.03, 0)], size=size*1.2, fill=True, outline_color = outline_color, fill_color = fill_color, **kwargs)
    elif symbol == "circle":
        return svg_circle(x, y, width/2*size, fill_color = fill_color, outline_color = outline_color, **kwargs)
    return ""

def svg_large_arrow(x1, x2, y, height, fill_color = "none", outline_color = "black", **kwargs):
    points = [(x1, y-height/2), (x2-height, y-height/2), (x2-height, y-height), (x2, y), (x2-height, y+height), (x2-height, y+height/2), (x1, y+height/2)]
    return(svg_path(0, 0, points, fill_color=fill_color, outline_color = outline_color, **kwargs))

def svg_large_arrow_start(x1, x2, y, height, **kwargs):
	return(svg_line(x1, y-height/2, x2, y-height/2, **kwargs) + \
		svg_line(x1, y+height/2, x2, y+height/2, **kwargs) + \
		svg_line(x1, y-height/2, x1, y+height/2, **kwargs))

def svg_large_arrow_middle(x1, x2, y, height, **kwargs):
	return(svg_line(x1, y-height/2, x2, y-height/2, **kwargs) + \
		svg_line(x1, y+height/2, x2, y+height/2, **kwargs))

def svg_large_arrow_end(x1, x2, y, height, outline_color = "black", fill_color = "none", **kwargs):
	points = [(x1, y-height/2), (x2-height, y-height/2), (x2-height, y-height), (x2, y), (x2-height, y+height), (x2-height, y+height/2), (x1, y+height/2)]
	return(svg_open_path(0, 0, points, fill_color=fill_color, outline_color = outline_color, **kwargs))

def svg_large_arrow_abbreviated(x1, x2, y, height, **kwargs):
	points = [(x1, y-height/2), (x2-height, y-height/2), (x2, y), (x2-height, y+height/2), (x1, y+height/2)]
	return(svg_path(0, 0, points, **kwargs))

def svg_large_arrow_end_abbreviated(x1, x2, y, height, **kwargs):
	points = [(x1, y-height/2), (x2-height, y-height/2), (x2, y), (x2-height, y+height/2), (x1, y+height/2)]
	return(svg_open_path(0, 0, points, **kwargs))

def svg_large_arrow_ongoing(x1, x2, y, height, lwd=1.8, size=1, **kwargs):
	# height is actually half of the full height of the arrow
	points = [
		(x1, y - height/2),
		(x2 - 2 * height, y - height/2),
		(x2 - height, y - height),
		(x2, y),
		(x2 - height, y + height),
		(x2 - 2 * height, y + height/2),
		(x1, y + height/2),
		(x1, y - height/2)
	]
	points = [
		f"M"
	]
	# return(svg_open_path(0, 0, points, **kwargs))
	out = f'<path d="M{x1} {y - height/2} '
	out += f'H{x2 - 2*height} '
	out += f'M{x2 - height * 5/4} {y - height/2} '
	out += f'h{height * 1/2} '
	out += f'v{-height/2} '
	out += f'l{height} {height} '
	out += f'l{-height} {height} '
	out += f'v{-height/2} '
	out += f'H{x1} '
	out += f'" style="stroke: black; fill: none; stroke-width:{lwd};" '
	out += f'/>\n'
	return(out)

def svg_fine_arrow(x1, x2, y, height, **kwargs):
    head_length = 9
    head_width = 2.7
    points = [(x1, y+height/2), (x2-height*head_length, y+height/2), (x2-height*head_length, y+height*head_width), (x2, y), (x2-height*head_length, y-height*head_width), (x2-height*head_length, y-height/2), (x1, y-height/2)]
    return(svg_path(0, 0, points, **kwargs))


# # arrow end starts 'height' before x2
# def svg_end_arrow(x1, x2, y, height, style = ""):
# 	out = f'<path d="M{x2 - height} {y - height/2} v{height/2} l0 {-height/2} l'
	
# 	out += f'style="{style}"/>\n'

# def svg_end_open(x1, x2, y, height, style = ""):
# 	return(f'<path d="M{x2 - height} {y - height/2} h{height} style="{style}"/>\n')

# def svg_start_open(x1, x2, y, height, **kwargs):
# 	pass

# def svg_start_closed(x1, x2, y, height, **kwargs):
# 	pass