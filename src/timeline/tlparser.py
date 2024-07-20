import ply.yacc as yacc
from timeline.tllexer import *

symbol_table = {}
sources = []


def p_expression_atomic(p):
    '''
    expression : point
               | interval
               | thread
               | section
               | chart
               | source
               | import
               | marker
    '''
    p[0] = p[1]



## SOURCE

def p_source(p):
    '''
    source : SOURCE
    '''
    p[0] = ('source', p[1])

def p_import(p):
    '''
    import : IMPORT
    '''
    p[0] = ('import', p[1][0].strip(), p[1][1].strip(), p[1][2])


## CHART

def p_chart(p):
    '''
    temp_chart : BEGIN section
               | BEGIN source
               | BEGIN marker
    '''
    p[0] = [p[2]]

def p_chart1(p):
    '''
    temp_chart : temp_chart section
    '''
    p[0] = p[1]
    p[0].append(p[2])

def p_chart2(p):
    '''
    temp_chart : temp_chart source
               | temp_chart marker
    '''
    p[0] = p[1]
    p[0].append(p[2])

def p_chart3(p):
    '''
    chart : temp_chart END
    '''
    p[0] = ('chart', p[1])



## MARKER

def p_marker(p):
    '''
    marker : MARKER DATE
    '''
    p[0] = ('marker', p[2], '')

def p_marker1(p):
    '''
    marker : MARKER DATE PARAMETER
    '''
    p[0] = ('marker', p[2], p[3])



# ## SECTION

def p_section(p):
    '''
    temp_section : SECTION SYMBOL_NAME
    '''
    p[0] = (p[2], [], '')

def p_section1(p):
    '''
    temp_section : SECTION SYMBOL_NAME PARAMETER
    '''
    p[0] = (p[2], [], p[3])

def p_section2(p):
    '''
    temp_section : temp_section thread
    '''
    p[0] = p[1]
    p[0][1].append(p[2])

def p_section3(p):
    '''
    temp_section : temp_section import
    '''
    p[0] = p[1]
    p[0][1].append(p[2])

def p_section4(p):
    '''
    section : temp_section
    '''
    p[0] = ('section', p[1][0], p[1][1], p[1][2]) 



# ## THREAD

def p_thread(p):
    '''
    temp_thread : THREAD SYMBOL_NAME
    '''
    p[0] = (p[2], [], '')

def p_thread1(p):
    '''
    temp_thread : THREAD SYMBOL_NAME PARAMETER
    '''
    p[0] = (p[2], [], p[3])

def p_thread2(p):
    '''
    temp_thread : temp_thread point
                | temp_thread interval
    '''
    p[0] = p[1]
    p[0][1].append(p[2])

def p_thread3(p):
    '''
    thread : temp_thread
    '''
    p[0] = ('thread', p[1][0], p[1][1], p[1][2]) 



# ## POINT

def p_point(p):
    '''
    point : SYMBOL_NAME ASSIGN DATE
    '''
    symbol_table[p[1]] = p[3]
    p[0] = ('point', p[1], p[3], '')  

def p_point1(p):
    '''
    point : SYMBOL_NAME ASSIGN DATE PARAMETER
    '''
    symbol_table[p[1]] = p[3]
    p[0] = ('point', p[1], p[3], p[4])  



# ## INTERVAL

def p_interval(p):
    '''
    interval : SYMBOL_NAME ASSIGN DATE RANGE DATE
    '''
    symbol_table[p[1]] = p[3]
    p[0] = ('interval', p[1], p[3], p[5], '')  

def p_interval1(p):
    '''
    interval : SYMBOL_NAME ASSIGN DATE RANGE DATE PARAMETER
    '''
    symbol_table[p[1]] = p[3]
    p[0] = ('interval', p[1], p[3], p[5], p[6])  



## ERROR
def p_error(p):
    pass


parser = yacc.yacc()

def parse_tl(source, debug = False):
    try:
        ast = parser.parse(source, debug = debug)
        return ast, symbol_table
    except ValueError as message:
        sys.exit(f"ERROR: Parsing error, " + str(message))
    
def ast_get_thread(ast, caption):
    def find_in_section(section, caption):
        for i in section[3]:
            if i[0] == "thread" and i[1] == caption:
                return(i)
        return(None)
    
    def find_in_chart(chart, caption):
        for i in chart:
            if i[0] == "section":
                t = find_in_section(i, caption)
                if t:
                    return(t)
        return(None)
    
    if ast[0] == "chart":
        return(find_in_chart(ast[1], caption))
    if ast[0] == "section":
        return(find_in_section(ast[3], caption))
    return(None)