import ply.yacc as yacc
from tllexer import *

symbol_table = {}


def p_expression_atomic(p):
    '''
    expression : point
               | interval
               | thread
               | section
               | chart
    '''
    p[0] = p[1]


## CHART

def p_chart(p):
    '''
    temp_chart : BEGIN section
    '''
    p[0] = [p[2]]

def p_chart2(p):
    '''
    temp_chart : temp_chart section
    '''
    p[0] = p[1]
    p[0].append(p[2])

def p_chart1(p):
    '''
    chart : temp_chart END
    '''
    p[0] = ('chart', p[1])



# ## SECTION

def p_section(p):
    '''
    temp_section : START_SECTION thread
    '''
    # p[0] = (p[1], [p[2]])
    p[0] = (p[1], "transparent", [p[2]])

def p_section_color(p):
    '''
    temp_section : START_SECTION COLOR thread
    '''
    # p[0] = (p[1], [p[2]])
    p[0] = (p[1], p[2], [p[3]])

    
def p_section1(p):
    '''
    temp_section : temp_section thread
    '''
    p[0] = p[1]
    # p[0][1].append(p[2])
    p[0][2].append(p[2])


def p_section2(p):
    '''
    section : temp_section
    '''
    # p[0] = ('section', p[1][0], p[1][1]) 
    p[0] = ('section', p[1][0], p[1][1], p[1][2]) 


# ## THREAD

def p_thread(p):
    '''
    temp_thread : START_THREAD point
                | START_THREAD interval
    '''
    # print(f'start thread {p[1]}')
    p[0] = (p[1], [p[2]])

def p_thread1(p):
    '''
    temp_thread : temp_thread point
                | temp_thread interval
    '''
    # print('append point to thread')
    p[0] = p[1]
    p[0][1].append(p[2])

def p_thread2(p):
    '''
    thread : temp_thread
    '''
    p[0] = ('thread', p[1][0], p[1][1]) 


def p_point(p):
    '''
    point : SYMBOL_NAME ASSIGN DATE
    '''
    symbol_table[p[1]] = p[3]
    # print(f'add point symbol {p[1]}')
    p[0] = ('point', p[1], p[3])  

def p_interval(p):
    '''
    interval : SYMBOL_NAME ASSIGN DATE RANGE DATE
    '''
    symbol_table[p[1]] = p[3]
    p[0] = ('interval', p[1], p[3], p[5])  



def p_error(p):
    # print(f'Syntax error: {p}')
    pass


parser = yacc.yacc()

def parse_tl(source, debug = False):
    try:
        ast = parser.parse(source, debug = debug)
        return ast, symbol_table
    except:
        return None, None
