import re
import ply.lex as lex
from sintactico import to_parse


errores = []

# Lista de palabras reservadas
reserved = {
    'let'           :   'RLET',
    'string'        :   'RSTRING',
    'touppercase'   :   'RTOUPPERCASE',
    'tolowercase'   :   'RTOLOWERCASE',
    'tofixed'       :   'RTOFIXED',
    'toexponential' :   'RTOEXPONENTIAL',
    'tosting'       :   'RTOSTRING',
    'split'         :   'RSPLIT',
    'typeof'        :   'RTYPEOF',
    'concat'        :   'RCONCAT',
    'null'          :   'RNULL',
    'any'           :   'RANY',
    'number'        :   'RNUMBER',
    'boolean'       :   'RBOOL',
    'true'          :   'RTRUE',
    'false'         :   'RFALSE',
    'console'       :   'RCONSOLE',
    'log'           :   'RLOG',
    'interface'     :   'RINTERFACE',
    'void'          :   'RVOID',
    'function'      :   'RFUNCTION',
    'for'           :   'RFOR',
    'of'            :   'ROF',
    'while'         :   'RWHILE',
    'break'         :   'RBREAK',
    'continue'      :   'RCONTINUE',
    'return'        :   'RRETURN',
    'if'            :   'RIF',
    'else'          :   'RELSE',
    'elseif'        :   'RELSEIF',
    'push'          :   'RPUSH',
    'pop'           :   'RPOP',
    'length'        :   'RLENGTH',
    'interface'     :   'RINTERFACE',


}

tokens = [
    'PUNTO',
    'COMA',
    'PUNTOCOMA',
    'DOSPUNTOS',
    'IGUAL',
    'MAS',
    'MENOS',
    'POR',
    'DIVI',
    'POTENCIA',
    'MODULO',
    'MENOR',
    'MAYOR',
    'MENORIGUAL',
    'MAYORIGUAL',
    'IGUALIGUAL',
    'DIFERENTE',
    'AND',
    'OR',
    'NOT',
    'PARIZQ',
    'PARDER',
    'CORIZQ',
    'CORDER',
    'LLAVEIZQ',
    'LLAVEDER',
    'ID',
    'NUMBER',
    'DECIMAL',
    'CADENA',
] + list(reserved.values())

#Tokens
t_PUNTO         = r'\.'
t_COMA          = r','
t_PUNTOCOMA     = r';'
t_DOSPUNTOS     = r':'

t_IGUAL         = r'='
t_MAS           = r'\+'
t_MENOS         = r'-'
t_POR           = r'\*'
t_DIVI          = r'/'
t_POTENCIA      = r'\^'
t_MODULO        = r'%'

t_MENOR         = r'<'
t_MAYOR         = r'>'
t_MENORIGUAL    = r'<='
t_MAYORIGUAL    = r'>='
t_IGUALIGUAL    = r'==='
t_DIFERENTE     = r'!=='
t_AND           = r'&&'
t_OR            = r'\|\|'
t_NOT           = r'!'

t_PARIZQ        = r'\('
t_PARDER        = r'\)'
t_CORIZQ        = r'\['
t_CORDER        = r'\]'
t_LLAVEIZQ      = r'{'
t_LLAVEDER      = r'}'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_CADENA(t):
    r'\".*?\"'
    t.value = t.value[1:-1] # quitar comillas
    return t

def t_ENTERO(t):	
    r'\d+'
    t.value = int(t.value)
    return t

def t_DECIMAL(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Comentarios y tabulaciones
def t_com_simple(t):
    r'\/\/.*\n'
    t.lexer.lineno += 1

def t_com_mult(t):
    r'\/\*(.|\n)*?\*\/'
    t.lexer.lineno += t.value.count('\n')

t_ignore = ' \t'

#Error
def t_error(t):
    t.lexer.skip(1)

def find_column(inp, tk):
    line_start = inp.rfind('\n', 0, tk.lexpos) + 1
    return (tk.lexpos - line_start) + 1

def col(token):
    return (token.lexpos - (to_parse.rfind('\n', 0, token.lexpos) + 1)) + 1


lexer = lex.lex(reflags = re.IGNORECASE)