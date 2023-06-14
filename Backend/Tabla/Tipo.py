from enum import Enum


class Tipos(Enum):
    NULL = 'NULL'
    NUMBER = 'NUMBER'
    BOOLEAN = 'BOOLEAN'
    STRING = 'STRING'
    ANY = 'ANY'
    ARREGLO = 'ARREGLO'
    STRUCT = 'STRUCT'
    FUNCTION = 'FUNCTION'

class Aritmeticos(Enum):
    SUMA = '+'
    RESTA = '-'
    MULTIPLICACION = '*'
    DIVISION = '/'
    POTENCIA = '^'
    MODULO = '%'

class Nativas(Enum):
    TOFIXED = 'TOFIXED'
    TOEXPONENTIAL = 'TOEXPONENTIAL'
    TYPEOF = 'TOSTRING'
    LOWERCASE = 'LOWERCASE'
    UPPERCASE = 'UPPERCASE'
    SPLIT = 'SPLIT'
    CONCAT = 'CONCAT'

class Relacionales(Enum):
    MAYOR = '>'
    MENOR = '<'
    MAYORIGUAL = '>='
    MENORIGUAL = '<='
    IGUAL = '==='
    DISTINTO = '!=='

class Logicas(Enum):
    OR = '||'
    AND = '&&'
    NOT = '!'


class CICLICO(Enum):
    BREAK= 'BREAK'
    CONTINUE= 'CONTINUE'
    RETURN= 'RETURN'




