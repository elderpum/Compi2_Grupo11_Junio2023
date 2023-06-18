import ply.yacc as yacc
from lexico import  tokens, lexer, errores, reserved
from lexico import col
from .Abstracto.instruccion import Instruccion
from Expresiones.Aritmeticas import Aritmetica
from Expresiones.logicas import Logicas
from Expresiones.callfunct import LLAMADA_EXP
from Expresiones.nativas import Nativa
from Expresiones.Variable import Variable
from Instrucciones.Asignacion import Asignacion
from Instrucciones.break_ import BREAK
from Instrucciones.continue_ import CONTINUE
from Instrucciones.elseif import ELSEIF
from Instrucciones.for_ import FOR
from Instrucciones.Funciones import FUNCION
from Instrucciones.If_ import IF
from Instrucciones.imprimir import Imprimir
from Instrucciones.return_ import RETURN
from Instrucciones.while_ import WHILE
from Tabla.Tipo import Tipos, Nativas, Aritmeticos, Relacionales, Logicas
from Tabla.Errores import Error


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
    'init   : instrucciones'
    t[0] = t[1]

def p_instrucciones(t):
    'instrucciones  : instrucciones instruccion'
    if t[2] != None:
        t[1].append(t[2])
    t[0] = t[1]

def p_instrucciones_ins(t):
    'instrucciones  : instruccion'
    if t[1] == None:
        t[0] = []
    else:
        t[0] = [t[1]]

def p_instruccion(t):
    '''instruccion  : imprimir PUNTOCOMA
                    | asignacion PUNTOCOMA
                    | condicional r_end PUNTOCOMA
                    | whilee r_end PUNTOCOMA
                    | forr r_end PUNTOCOMA
                    | struct PUNTOCOMA
                    | funtionn r_end PUNTOCOMA
                    | llamada PUNTOCOMA
                    | BREAKk PUNTOCOMA
                    | RETURNN PUNTOCOMA
                    | CONTINUEE PUNTOCOMA'''
    t[0] = t[1]

# Condicionales
def p_condicional_else(t):
    'condicional    : if RELSE instrucciones'
    t[0] = IF(t[1], t.lineno(1), col(t.slice[2]), t[3])

def p_condicional(t):
    'condicional    : if'
    t[0] = t[1]
 
def p_break(t):
    '''BREAKk : RBREAK'''
    t[0] = BREAK(t.lineno(1), col(t.slice[1])) 

def p_continue(t):
    '''CONTINUEE : RCONTINUE'''
    t[0] = CONTINUE(t.lineno(1), col(t.slice[1])) 

def p_return(t):
    '''RETURNN : RRETURN'''
    t[0] = RETURN(t.lineno(1), col(t.slice[1])) 

def p_return_expresion(t):
    '''RETURNN : RRETURN expresion'''
    t[0] = RETURN(t.lineno(1), col(t.slice[1]), t[2])

  
def p_if(t):
    'if : RIF expresion instrucciones'
    t[0] = ELSEIF(t[2], t[3], t.lineno(1), col(t.slice[1]))
    
def p_if_elseif(t):
    'if : if RELSEIF expresion instrucciones'
    t[0] = ELSEIF(t[3], t[4], t.lineno(1), col(t.slice[2]), t[1])



#ciclos


def p_ins_while(t):
    'whilee : RWHILE expresion instrucciones'
    t[0] = WHILE(t[2], t[3], t.lineno(1), col(t.slice[1]))

def p_ins_for(t):
    'forr : RFOR ID r_in expresion instrucciones'
    t[0] = FOR(t[2], t[4],t[5],t.lineno(1), col(t.slice[1]))

#asignaciones 
def p_asignacion(t):
    '''asignacion : ID igualT expresion'''
    t[0] = Asignacion(None, t.lineno(1), col(t.slice[2]),t[3], t[1])

def p_asignacionTipo(t):
    '''asignacion : ID igualT expresion dospuntos dospuntos tipo'''
    t[0] = Asignacion(t[6], t.lineno(1), col(t.slice[2]),t[3], t[1])
    
def p_asignacionTipo_id(t):
    '''asignacion : ID igualT expresion dospuntos dospuntos id'''
    t[0] = Asignacion(Tipos.OBJECT, t.lineno(1), col(t.slice[2]),t[3], t[1])

#ASIGNACION ARRAY
#Arrays
def p_asignacion_array_struct(t):
    '''array : ID number_array lista_id igualT expresion'''
    t[0] = Asignacion(None, t.lineno(1), col(t.slice[1]),t[5], t[1], t[3], t[2])

def p_asignacion_array(t):
    '''array : ID number_array igualT expresion'''
    t[0] = Asignacion(None, t.lineno(1), col(t.slice[1]),t[4], t[1], None, t[2])
    
#Asignacion STRUCT
def p_asignacion_STRUCT_variable(t):
    '''asignacion : ID lista_id igualT expresion'''
    t[0] = Asignacion(None, t.lineno(1), col(t.slice[1]),t[4], t[1], t[2])

def p_lista_id(t):
    '''lista_id : lista_id punto id'''
    if t[3] != None:
        t[1].append([t[3], None])
    t[0] = t[1]
    
def p_lista_id_array(t):
    '''lista_id : lista_id punto ID number_array'''
    if t[3] != None:
        t[1].append([t[3], t[4]])
    t[0] = t[1]
    
def p_lista_id_u(t):
    '''lista_id : punto id'''
    if t[2] == None:
        t[0] = []
    else:
        t[0] = [[t[2], None]]

def p_lista_id_u_lista(t):
    '''lista_id : punto ID number_array'''
    if t[2] == None:
        t[0] = []
    else:
        t[0] = [[t[2], t[3]]]
        
def p_llamada(t):
    '''llamada : ID PARIZQ parametro_print PARDER '''
    t[0] = LLAMADA_EXP(t[1], t[3], t.lineno(1), col(t.slice[1]))

def p_llamada_Solo(t):
    '''llamada : ID PARIZQ PARDER '''
    t[0] = LLAMADA_EXP(t[1], [], t.lineno(1), col(t.slice[1]))
#function

def p_function(t):
    '''funtionn : r_function ID PARIZQ PARDER instrucciones'''
    t[0] = FUNCION(t[2],t[5], t.lineno(1), col(t.slice[1]))

def p_function_parametro(t):
    '''funtionn : r_function ID PARIZQ parametros_function PARDER instrucciones'''
    t[0] = FUNCION(t[2],t[6], t.lineno(1), col(t.slice[1]), t[4])
    
def p_parametros_function(t):
    '''parametros_function : parametros_function COMA id'''
    if t[3] != None:
        t[1].append([t[3], Tipos.NOTHING])
    t[0] = t[1]
    
def p_parametros_function2(t):
    '''parametros_function : parametros_function COMA ID dospuntos dospuntos tipo'''
    if t[3] != None:
        t[1].append([t[3], t[6]])
    t[0] = t[1]
    
def p_parametros_function2_id(t):
    '''parametros_function : parametros_function COMA ID dospuntos dospuntos id'''
    if t[3] != None:
        t[1].append([t[3], Tipos.OBJECT])
    t[0] = t[1]
    
def p_parametros_function_unico(t):
    '''parametros_function : id'''
    if t[1] == None:
        t[0] = []
    else:
        t[0] = [[t[1], Tipos.NOTHING]]
    
    
def p_parametros_function_tipo(t):
    '''parametros_function : ID dospuntos dospuntos tipo'''
    if t[1] == None:
        t[0] = []
    else:
        t[0] = [[t[1], t[4]]]
def p_parametros_function_tipo_id(t):
    '''parametros_function : ID dospuntos dospuntos id'''
    if t[1] == None:
        t[0] = []
    else:
        t[0] = [[t[1], Tipos.OBJECT]]

#Structs

def p_struct(t):
    '''struct : r_struct ID parametros_struct r_end'''
    t[0] = STRUCT(t[2], t[3], t.lineno(1), col(t.slice[2]))

def p_mutable_struct(t):
    '''struct : r_mutable r_struct ID parametros_struct r_end'''
    t[0] = STRUCT(t[3], t[4], t.lineno(1), col(t.slice[2]), True)
    
def p_parametros_struct(t):
    '''parametros_struct : parametros_struct parametro_struct'''
    if t[2] != None:
        t[1].append(t[2])
    t[0] = t[1]

def p_parametros_struct_unico(t):
    '''parametros_struct : parametro_struct'''
    if t[1] == None:
        t[0] = []
    else:
        t[0] = [t[1]]

def p_parametro_struct_nulo(t):
    '''parametro_struct : ID ptcoma'''
    if t[1] == None:
        t[0] = []
    else:
        t[0] = [t[1],None]
        
def p_parametro_struct(t):
    '''parametro_struct : ID dospuntos dospuntos tipo ptcoma'''
    if t[1] == None:
        t[0] = []
    else:
        t[0] = [t[1], t[4]]
        
def p_parametro_struct_id(t):
    '''parametro_struct : ID dospuntos dospuntos ID ptcoma'''
    if t[1] == None:
        t[0] = []
    else:
        t[0] = [t[1], Tipos.OBJECT]

#impresiones
##impresiones
def p_print(t):
    'imprimir  : RCONSOLE PUNTO RLOG PARIZQ parametro_print PARDER'
    t[0] = Imprimir(t[3], t.lineno(1), col(t.slice[1]))
    
def p_print_v(t):
    'print  : r_print PARIZQ PARDER'
    t[0] = Imprimir([], t.lineno(1), col(t.slice[1]))
    

def p_parametro_print(t):
    'parametro_print  : parametro_print COMA expresion'
    if t[3] != None:
        t[1].append(t[3])
    t[0] = t[1]

def p_parametro_print_exp(t):
    'parametro_print    : expresion'
    if t[1] == None:
        t[0] = []
    else:
        t[0] = [t[1]]
#tipos
def p_tipo(t):
    '''tipo : RNUMBER
            | RBOOL
            | RSTRING
            | RANY'''
    t[0] = Tipos(t[1].upper())

#Struct Exp
def p_variable(t):
    '''expresion : exp_struct'''
    t[0] = t[1]

def p_Expresion_Struct(t):
    '''exp_struct : exp_struct punto id'''
    t[0] = Variable(t[1],t.lineno(1), col(t.slice[3]),t[3])


def p_Expresion_Struct_lista(t):
    '''exp_struct : exp_struct punto ID number_array''' 
    t[0] = Variable(t[1],t.lineno(1), col(t.slice[3]),t[3],t[4])
    

def p_expresion_struct_id(t):
    '''exp_struct : id'''
    t[0] = Variable(t[1], t.lineno(1), col(t.slice[1]))
#Arrays
#id array
def p_expresion_array_id(t):
    '''exp_struct : ID number_array'''
    t[0] = Variable(t[1], t.lineno(1), col(t.slice[1]),None, t[2])
    
#number array

def p_expresion_id_content_unico(t):
    '''number_array : cizq expresion cder'''
    if t[2] == None:
        t[0] = []
    else:
        t[0] = [t[2]]
        
def p_expresion_id_content(t):
    '''number_array : number_array cizq expresion cder'''
    if t[3] != None:
        t[1].append(t[3])
    t[0] = t[1]

#Expresion_Array
def p_expresion_Array(t):
    '''expresion : cizq expresion_exp cder'''
    t[0] = ARRAY(t[2], t.lineno(1), col(t.slice[1]))

def p_coma_expresion(t):
    '''expresion_exp : expresion_exp COMA expresion'''
    if t[3] != None:
        t[1].append(t[3])
    t[0] = t[1]
    
def p_coma_expresion_unico(t):
    '''expresion_exp : expresion'''
    if t[1] == None:
        t[0] = []
    else:
        t[0] = [t[1]]
        
    
        
#Llamada EXP



def p_expresion_llamada(t):
    '''expresion : ID PARIZQ parametro_print PARDER'''
    t[0] = LLAMADA_EXP(t[1], t[3], t.lineno(1), col(t.slice[1]))
#nativas
def p_nativa(t):
    '''expresion : r_parse PARIZQ tipo COMA expresion PARDER
                 | r_trunc PARIZQ tipo COMA expresion PARDER
                 | r_log PARIZQ expresion COMA expresion PARDER
                 '''
    t[0] = Nativa(t.lineno(1), col(t.slice[6]), t[3], Nativas(t[1].upper()),t[5])

def p_push_expresion(t):
    '''expresion : r_push not PARIZQ expresion COMA expresion PARDER'''
    t[0] = PUSH(t[4], t[6], t.lineno(1), col(t.slice[1]))

def p_pop_expresion(t):
    '''expresion : r_pop not PARIZQ expresion PARDER'''
    t[0] = POP(t[4], t.lineno(1), col(t.slice[1]))
    
def p_length_expresion(t):
    '''expresion : r_length PARIZQ expresion PARDER'''
    t[0] = LENGHT(t[3], t.lineno(1), col(t.slice[1]))

def p_nativa_individual(t):
    '''expresion    : r_trunc PARIZQ expresion PARDER
                    | r_string PARIZQ expresion PARDER
                    | r_typeof PARIZQ expresion PARDER
                    | RTOUPPERCASE PARIZQ expresion PARDER
                    | RTOLOWERCASE PARIZQ expresion PARDER'''    
    t[0] = Nativas(t.lineno(1), col(t.slice[4]), t[3], Tipos_Nativa(t[1].upper()))

#Expresion Rango
def p_expresion_rango(t):
    '''expresion : expresion dospuntos expresion'''
    t[0] = Rango(t[1], t[3], t.lineno(1), col(t.slice[2]))

#Expresion Rango completo
def p_expresion_rango_Todo(t):
    '''expresion : dospuntos'''
    t[0] = Rango(None, None, t.lineno(1), col(t.slice[1]))
    
#expresiones
def p_expresion(t):
    '''expresion : expresion suma expresion
                 | expresion resta expresion
                 | expresion mul expresion
                 | expresion div expresion
                 | expresion elevado expresion
                 | expresion modulo expresion
                 | expresion igual expresion
                 | expresion diferente expresion
                 | expresion mayor expresion
                 | expresion menor expresion
                 | expresion mayor_igual expresion
                 | expresion menor_igual expresion
                 | expresion and expresion
                 | expresion or expresion'''
    if t[2] == '+' or t[2] == '-' or t[2] == '*' or t[2] == '/' or t[2] == '%' or t[2] == '^':
        t[0] = Aritmetica(Aritmeticos(t[2]),t.lineno(1), col(t.slice[2]),t[1],t[3])
    elif t[2] == '==' or t[2] == '!=' or t[2] == '>' or t[2] == '>=' or t[2] == '<' or t[2] == '<=':
        t[0] = Relacional(Relacionales(t[2]),t.lineno(1), col(t.slice[2]),t[1],t[3])
    elif t[2] == '&&' or t[2] == '||':
        t[0] = Logica(Logicas(t[2]),t.lineno(1), col(t.slice[2]),t[1],t[3])

def p_expresion_unaria(t):
    '''expresion    :   resta expresion %prec UMENOS
                    |   not expresion %prec nnot'''
    if t[1] == '-':
        t[0] = Aritmetica(Aritmeticos(t[1]),t.lineno(1), col(t.slice[1]),t[2])
    else:
        t[0] = Logica(Logicas(t[1]),t.lineno(1), col(t.slice[1]),t[2])


   
def p_expresion_primitiva_int(t):
    'expresion    : int'
    t[0] = Primitivo(Tipos.ENTERO, t[1], t.lineno(1), col(t.slice[1]))

def p_expresion_primitiva_float(t):
    'expresion    : decimal'
    t[0] = Primitivo(Tipos.FLOAT, t[1], t.lineno(1), col(t.slice[1]))

def p_expresion_primitiva_char(t):
    'expresion    : char'
    t[0] = Primitivo(Tipos.CHAR, t[1], t.lineno(1), col(t.slice[1]))

def p_expresion_primitiva_string(t):
    'expresion    : string'    
    t[0] = Primitivo(Tipos.STRING, t[1], t.lineno(1), col(t.slice[1]))

def p_expresion_primitiva_bool(t):
    '''expresion    : r_false
                    | r_true'''
    if t[1]=='true':
        t[0] = Primitivo(Tipos.BOOL, True, t.lineno(1), col(t.slice[1]))
    else:
        t[0] = Primitivo(Tipos.BOOL, False, t.lineno(1), col(t.slice[1]))

def p_expresion_primitiva_nothing(t):
    '''expresion : r_nothing'''
    t[0] = Primitivo(Tipos.NOTHING, "nothing", t.lineno(1), col(t.slice[1]))

# def p_variable(t):
#     '''expresion : id'''
#     t[0] = Variable(t[1], t.lineno(1), col(t.slice[1]))

# Definicion de expresiones 
def p_agrupacion_expresion(t):
    'expresion : PARIZQ expresion PARDER'
    t[0] = t[2]
    
###################################
def p_error(p):
    if p:
        errores.append(Error('Syntax',
                   f'error at token {p.value}', p.lineno,  col(p)))
        print(f'Syntax error at token {p.value}', p.lineno, p.lexpos)
        parser.errok()
    else:
        print("Syntax error at EOF")


from ply import yacc
parser = yacc.yacc()


input = ''

def get_errors():
    return errores


def parse(i):
    global to_parse
    to_parse = i
    lexer.lineno = 1
    return parser.parse(i)