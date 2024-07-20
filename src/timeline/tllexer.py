import re
import ply.lex as lex

states = ()
current_year = ""

reserved = {}

tokens = [
    'START_THREAD', 'EQUALS', 'ASSIGN', 'DATE', 'COMMENT',
    'PARAMETER', 'INT', 'START_SECTION', 'SECTION', 'THREAD',
    'ADD', 'TIMEUNIT', 'RANGE', 'END', 'BEGIN', 'COLOR',
    'SOURCE', 'IMPORT', 'ALL', 'ALIAS', 'MARKER', 'SYMBOL_NAME'
] + list(reserved.values())

next_state = ''

t_EQUALS = r'\='
t_ASSIGN = r':'
t_INT = r'[0-9]+'
t_ADD = r'\+'
t_ignore = ' \t\n'


## IMPORTS

def t_SOURCE(t):
    r'source\s+(.*)\n'
    temp = re.match(r'source\s+(.*)\n', t.value)
    t.value = temp.groups()[0]
    return t

def t_IMPORT(t):
    r'IMPORT\s+(.*)\s+FROM\s+(.*)(\(.*\))?'
    temp = re.match(r'IMPORT\s+(.*)\s+FROM\s+([a-zA-Z_0-9\.\- ]+)\s*?(\(.*\))?', t.value)
    t.value = (temp.groups()[0], temp.groups()[1], temp.groups()[2])
    return(t)

def t_ALL(t):
    r'\*'
    return(t)


## CHART

def t_BEGIN(t):
    r'BEGIN'
    t.value = "BEGIN"
    return t

def t_END(t):
    r'END'
    t.value = "END"
    return t

def t_MARKER(t):
    r'marker|MARKER'
    t.value = "MARKER"
    return t


## SECTIONS

def t_SECTION(t):
    r'section|SECTION'
    t.value = "SECTION"
    return t


## THREADS

def t_THREAD(t):
    r'thread|THREAD'
    t.value = "THREAD"
    return t


## GENERIC

def t_COLOR(t):
    r'color\s+(white|red|blue|yellow|violet|green|aqua)'
    temp = re.match(r'color\s+(white|red|blue|yellow|violet|green|aqua)', t.value)
    t.value = temp.groups()[0]
    return t

def t_TIMEUNIT(t):
    r'days|workdays|months'
    return t

def t_COMMENT(t):
    r'\#.*\n'
    t.value = None

def t_DATE(t):
    r'([0-9]{1,2})[\.-]([0-9]{1,2}|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|January|Februrary|March|April|June|July|August|September|October|November|December)([\.-]([0-9]{2,4}))?'
    temp = re.match(r'([0-9]{1,2})[\.\-]([0-9]{1,2}|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|January|Februrary|March|April|June|July|August|September|October|November|December)([\.\-]([0-9]{2,4}))?', t.value)

    global current_year

    if temp.groups()[3]:
        current_year = temp.groups()[3]

    if current_year == "":
        raise ValueError(f"no year defined in '{t.value}'")

    t.value = temp.groups()[0] + "-" + temp.groups()[1] + "-" + current_year
    return t

def t_RANGE(t):
    r'to|\-'
    return t

def t_PARAMETER(t):
    r'\(.*\)'
    temp = re.match(r'\((.*)\)', t.value)
    t.value = temp.groups()[0]
    return t

def t_SYMBOL_NAME(t):
    r'[a-zA-Z_\.\-][a-zA-Z_0-9\.\- ]*'
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