import ply.yacc as yacc
from lexico import tokens,lexer,errores,find_column


precedence = (
    ('left','OR'),
    ('left','AND'),
    ('left','IGUALIGUAL','DIFERENTE'),
    ('left','MENOR','MAYOR','MENORIGUAL','MAYORIGUAL'),
    ('left','MAS','MENOS'),
    ('left','POR','DIVI','MODULO'),
    ('right','NOT'),
    ('right','POTENCIA')
)

# Definicion de la gramatica para typecraft

def p_init(t):
    'init : instrucciones'
    t[0] = t[1]

def 