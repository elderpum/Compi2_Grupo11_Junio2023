import re
import ply.lex as lex

errores = []
reservadas = {
    'console'       : 'RCONSOLE',
    'log'           : 'RLOG',
    'null'          : 'RNULL',
    'string'        : 'RSTRING',
    'number'        : 'RNUMBER',
    'boolean'       : 'RBOOLEAN',
    'any'           : 'RANY',
    'interface'     : 'RINTERFACE',
    'toFixed'       : 'NFIXED',
    'toExponential' : 'NEXP',
    'toString'      : 'NTOSTRING',
    'String'        : 'NSTRING',
    'toLowerCase'   : 'NLOWER',
    'toUpperCase'   : 'NUPPER',
    'split'         : 'NSPLIT',
    'concat'        : 'NCONCAT',
    'length'        : 'NLENGTH',
    'typeof'        : 'NTYPEOF',
    'Number'        : 'NNUMBER',
    'push'          : 'NPUSH',
    'let'           : 'RLET',
    'function'      : 'RFUNCTION',
    'if'            : 'RIF',
    'else'          : 'RELSE',
    'while'         : 'RWHILE',
    'for'           : 'RFOR',
    'of'            : 'ROF',
    'in'            : 'RIN',
    'break'         : 'RBREAK',
    'continue'      : 'RCONTINUE',
    'return'        : 'RRETURN',
    'true'          : 'RTRUE',
    'false'         : 'RFALSE'
}

tokens = [
    'PUNTO',
    'PTYCOMA',
    'COMA',
    'DOSPTS',
    'PARIZQ',
    'PARDER',
    'CORIZQ',
    'CORDER',
    'LLIZQ',
    'LLDER',
    'INCREMENTO',
    'DECREMENTO',
    'MAS',
    'MENOS',
    'POR',
    'DIV',
    'MODULO',
    'POTENCIA',
    'MAYOR',
    'MENOR',
    'MAYIGUAL',
    'MENIGUAL',
    'IGUALDAD',
    'IGUAL',
    'DIFERENTE',
    'OR',
    'AND',
    'NOT',
    'ENTERO',
    'DECIMAL',
    'CADENA',
    'ID',
] + list(reservadas.values())

#definicion de tokens 
t_PUNTO         = r'\.'
t_PTYCOMA        = r'\;'
t_COMA        = r'\,'
t_DOSPTS        = r'\:'
t_PARIZQ          = r'\('
t_PARDER          = r'\)'
t_CORIZQ          = r'\['
t_CORDER          = r'\]'
t_LLIZQ          = r'\{'
t_LLDER          = r'\}'
t_INCREMENTO    = r'\+\+'
t_DECREMENTO    = r'\-\-'
t_MAS           = r'\+'
t_MENOS         = r'\-'
t_POR           = r'\*'
t_DIV           = r'\/'
t_MODULO           = r'\%'
t_POTENCIA           = r'\^'
t_MAYOR             = r'\>'
t_MENOR             = r'\<'
t_MAYIGUAL             = r'\>\='
t_MENIGUAL          = r'\<\='
t_IGUALDAD             = r'\=\=\='
t_DIFERENTE             = r'\!\=\='
t_IGUAL         = r'\='
t_OR            = r'\|\|'
t_AND            = r'\&\&'
t_NOT            = r'\!'

def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float value too large %d", t.value)
        t.value = 0
    return t
def t_ENTERO(n):
    r'\d+'
    try:
        if(n.value != None):
            n.value = int(n.value)
        else:
            n.value = 'nothing'
    except ValueError:
        print("Valor del entero demasiado grande %d", n.value)
        n.value = 0
    return n



def t_CADENA(t):
    r'(\".*?\")'
    t.value = t.value[1:-1] #Se remueven las comillas de la entrada
    t.value = t.value.replace('\\t','\t')
    t.value = t.value.replace('\\n','\n')
    t.value = t.value.replace('\\"','\"')
    t.value = t.value.replace("\\'","\'")
    t.value = t.value.replace('\\\\','\\')
    return t
    
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reservadas.get(t.value,'ID')# Check for reserved words
    return t

def t_Com_Simple(t):
    r'\/\/.*'
    t.lexer.lineno += 1
    
def t_Com_Multiple(t):
    r'\/\*(.|\n)*?\*\/'
    t.lexer.lineno += t.value.count('\n')
    
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = " \t"

def t_error(t):
    t.lexer.skip(1)
    

def find_column(inp, tk):
    line_start = inp.rfind('\n', 0, tk.lexpos) + 1
    return (tk.lexpos - line_start) + 1

lexer = lex.lex(reflags = re.IGNORECASE)
