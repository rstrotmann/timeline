import re
from timeline.tlutils import tl_colors
import ply.lex as lex
import ply.yacc as yacc
from datetime import datetime
import dateutil.parser
import sys

states = ()
current_year = ""

reserved = {}

tokens = [
    'START_THREAD', 'EQUALS', 'ASSIGN', 'SYMBOL_NAME', 'DATE', 'COMMENT', 'INT', 'START_SECTION',
    'ADD', 'TIMEUNIT', 'RANGE', 'END', 'BEGIN', 'COLOR'
] + list(reserved.values())

next_state = ''

t_EQUALS = r'\='
t_ASSIGN = r':'
t_INT = r'[0-9]+'
t_ADD = r'\+'
t_ignore = ' \t\n'


## THREADS

def t_BEGIN(t):
    r'BEGIN'
    t.value = "BEGIN"
    return t

def t_END(t):
    r'END'
    t.value = "END"
    return t

def t_START_SECTION(t):
    r'section\s+(.*)\n'
    temp = re.match(r'section\s+(.*)\s*\n', t.value)
    t.value = temp.groups()[0]
    return t

def t_START_THREAD(t):
    r'thread\s+(.*)\n'
    temp = re.match(r'thread\s+(.*)\s*\n', t.value)
    t.value = temp.groups()[0]
    return t


## GENERIC

def t_COLOR(t):
    r'color\s+(white|red|blue|yellow|violet|green|aqua)'
    # print("|".join(list(tl_colors.keys())))
    temp = re.match(r'color\s+(white|red|blue|yellow|violet|green|aqua)', t.value)
    t.value = temp.groups()[0]
    return t

def t_TIMEUNIT(t):
    r'days|workdays|months'
    return t

def t_COMMENT(t):
    r'\#.*\n'
    # t.value = t.value.strip()
    t.value = None
    # return t

def t_DATE(t):
    r'([0-9]{1,2})[\.-]([0-9]{1,2}|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|January|Februrary|March|April|June|July|August|September|October|November|December)([\.-]([0-9]{2,4}))?'
    temp = re.match(r'([0-9]{1,2})[\.\-]([0-9]{1,2}|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|January|Februrary|March|April|June|July|August|September|October|November|December)([\.\-]([0-9]{2,4}))?', t.value)

    # print(temp.groups())
    global current_year

    if temp.groups()[3]:
        current_year = temp.groups()[3]

    if current_year == "":
        print("----- VALUE ERROR -----")
        print("No year defined")
        sys.exit(1)

    t.value = temp.groups()[0] + "-" + temp.groups()[1] + "-" + current_year
    return t

def t_RANGE(t):
    r'to|\-'
    return t

def t_SYMBOL_NAME(t):
    r'[a-zA-Z_\.\-][a-zA-Z_0-9\.\- ]*\n?'
    t.value = t.value.strip()
    return t
       
def t_error(t):
    if lexer.debug:
        print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

## LEXER

next_state = ''
lexer = lex.lex()

def lex(source, debug=False):
    lexer.debug = debug
    lexer.input(source)
    if debug:
        while True:
            tok = lexer.token()
            if not tok:
                break
            print(f'{tok.type}\t({tok.value})')
    return(lexer)