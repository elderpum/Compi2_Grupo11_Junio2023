import ply.yacc as yacc
from lexico import to_parse, errores, reserved,lexer,tokens, col
from Expresiones.Aritmeticas import Aritmetica
from Expresiones.logicas import Logicas
from Expresiones.callfunct import LLAMADA_EXP
from Expresiones.nativas import Nativas
from Expresiones.Variable import Variable
from Expresiones.array_ import ARRAY
from Expresiones.push_ import PUSH
from Expresiones.pop_ import POP
from Expresiones.primitivas import Primitivo
from Expresiones.relacionales import Relacional
from Expresiones.lenght_ import LENGHT
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
from Instrucciones.struct_ import STRUCT
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
                    | array PUNTOCOMA
                    | condicional PUNTOCOMA
                    | whilee PUNTOCOMA
                    | forr PUNTOCOMA
                    | struct PUNTOCOMA
                    | functionn PUNTOCOMA
                    | llamada PUNTOCOMA
                    | BREAKk PUNTOCOMA
                    | RETURNN PUNTOCOMA
                    | CONTINUEE PUNTOCOMA
                    | PUSHH PUNTOCOMA
                    | POPP PUNTOCOMA
                    | LENGHTT PUNTOCOMA
                    '''
    t[0] = t[1]


#push, pop, lenght

def p_pushh(t):
    '''PUSHH : RPUSH  PARIZQ expresion COMA expresion PARDER'''
    t[0] = PUSH(t[3], t[5], t.lineno(1), col(t.slice[1]))

def p_popp(t):
    '''POPP : RPOP PARIZQ expresion PARDER'''
    t[0] = POP(t[3], t.lineno(1), col(t.slice[1]))
    
def p_lengthh(t):
    '''LENGHTT : RLENGTH PARIZQ expresion PARDER'''
    t[0] = LENGHT(t[3], t.lineno(1), col(t.slice[1]))


# Condicionales
def p_condicional_else(t):
    'condicional    : if_ RELSE LLAVEIZQ  instrucciones LLAVEDER'
    t[0] = IF(t[1], t.lineno(1), col(t.slice[2]), t[4])

def p_condicional(t):
    'condicional    : if_'
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
    'if_ : RIF PARIZQ expresion PARDER LLAVEIZQ instrucciones LLAVEDER'
    t[0] = ELSEIF(t[3], t[6], t.lineno(1), col(t.slice[1]))
    
def p_if_elseif(t):
    'if_ : if_ RELSEIF PARIZQ expresion PARDER LLAVEIZQ instrucciones LLAVEDER'
    t[0] = ELSEIF(t[4], t[7], t.lineno(1), col(t.slice[2]), t[1])

#ciclos
def p_ins_while(t):
    'whilee : RWHILE PARIZQ  expresion PARDER LLAVEIZQ instrucciones LLAVEDER'
    t[0] = WHILE(t[3], t[6], t.lineno(1), col(t.slice[1]))

def p_ins_for(t):
    'forr : RFOR PARIZQ RLET ID ROF expresion PARDER LLAVEIZQ instrucciones LLAVEDER'
    t[0] = FOR(t[4], t[6],t[9],t.lineno(1), col(t.slice[1]))

def p_ins_for_incr(t):
    'forr : RFOR PARIZQ RLET ID ROF expresion PUNTOCOMA expresion PARDER LLAVEIZQ instrucciones LLAVEDER'
    t[0] = FOR(t[3], t[6],t[5],t.lineno(1), col(t.slice[1]), t[8])

#asignaciones 
def p_asignacion(t):
    '''asignacion : RLET ID  IGUAL expresion'''
    t[0] = Asignacion(None, t.lineno(1), col(t.slice[2]),t[4], t[2])

def p_asignacionTipo(t):
    '''asignacion : RLET ID DOSPUNTOS tipo IGUAL expresion'''
    t[0] = Asignacion(t[4], t.lineno(1), col(t.slice[2]),t[6], t[2])
    
def p_asignacionTipo_id(t):
    '''asignacion : RLET ID DOSPUNTOS ID IGUAL expresion'''
    t[0] = Asignacion(Tipos.OBJECT, t.lineno(1), col(t.slice[2]),t[6], t[2])

#ASIGNACION ARRAY
def p_asignacion_array_struct(t):
    '''array : ID number_array lista_id IGUAL expresion'''
    '''array : RLET ID number_array lista_id IGUAL expresion'''
    t[0] = Asignacion(None, t.lineno(1), col(t.slice[1]),t[5], t[1], t[3], t[2])

def p_asignacion_array(t):
    '''array : RLET ID number_array IGUAL expresion'''
    t[0] = Asignacion(None, t.lineno(1), col(t.slice[1]),t[4], t[1], None, t[2])
    
#Asignacion STRUCT
def p_asignacion_STRUCT_variable(t):
    '''asignacion : ID lista_id IGUAL expresion'''
    t[0] = Asignacion(None, t.lineno(1), col(t.slice[1]),t[4], t[1], t[2])

def p_lista_id(t):
    '''lista_id : lista_id PUNTO ID'''
    if t[3] != None:
        t[1].append([t[3], None])
    t[0] = t[1]
    
def p_lista_id_array(t):
    '''lista_id : lista_id PUNTO ID number_array'''
    if t[3] != None:
        t[1].append([t[3], t[4]])
    t[0] = t[1]
    
def p_lista_id_u(t):
    '''lista_id : PUNTO ID'''
    if t[2] == None:
        t[0] = []
    else:
        t[0] = [[t[2], None]]

def p_lista_id_u_lista(t):
    '''lista_id : PUNTO ID number_array'''
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
    '''functionn : RFUNCTION ID PARIZQ PARDER LLAVEIZQ instrucciones LLAVEDER'''
    t[0] = FUNCION(t[2],t[6], t.lineno(1), col(t.slice[1]))

def p_function_parametro(t):
    '''functionn : RFUNCTION ID PARIZQ parametros_function PARDER  LLAVEIZQ instrucciones LLAVEDER'''
    t[0] = FUNCION(t[2],t[7], t.lineno(1), col(t.slice[1]), t[4])
    
def p_parametros_function(t):
    '''parametros_function : parametros_function COMA ID'''
    if t[3] != None:
        t[1].append([t[3], Tipos.ANY])
    t[0] = t[1]
    
def p_parametros_function2(t):
    '''parametros_function : parametros_function COMA ID DOSPUNTOS  tipo'''
    if t[3] != None:
        t[1].append([t[3], t[6]])
    t[0] = t[1]
    
def p_parametros_function2_id(t):
    '''parametros_function : parametros_function COMA ID DOSPUNTOS  ID'''
    if t[3] != None:
        t[1].append([t[3], Tipos.OBJECT])
    t[0] = t[1]
    
def p_parametros_function_unico(t):
    '''parametros_function : ID'''
    if t[1] == None:
        t[0] = []
    else:
        t[0] = [[t[1], Tipos.ANY]]
    
    
def p_parametros_function_tipo(t):
    '''parametros_function : ID DOSPUNTOS tipo'''
    if t[1] == None:
        t[0] = []
    else:
        t[0] = [[t[1], t[4]]]
def p_parametros_function_tipo_id(t):
    '''parametros_function : ID DOSPUNTOS ID'''
    if t[1] == None:
        t[0] = []
    else:
        t[0] = [[t[1], Tipos.OBJECT]]

#Structs

def p_struct(t):
    '''struct : RINTERFACE ID LLAVEIZQ parametros_struct LLAVEDER'''
    t[0] = STRUCT(t[2], t[4], t.lineno(1), col(t.slice[2]))

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
    '''parametro_struct : ID PUNTOCOMA'''
    if t[1] == None:
        t[0] = []
    else:
        t[0] = [t[1],None]
        
def p_parametro_struct(t):
    '''parametro_struct : ID DOSPUNTOS tipo PUNTOCOMA'''
    if t[1] == None:
        t[0] = []
    else:
        t[0] = [t[1], t[4]]
        
def p_parametro_struct_id(t):
    '''parametro_struct : ID DOSPUNTOS ID PUNTOCOMA'''
    if t[1] == None:
        t[0] = []
    else:
        t[0] = [t[1], Tipos.OBJECT]

#impresiones
def P_imprimir(t):
    'imprimir  : RCONSOLE PUNTO RLOG PARIZQ parametro_print PARDER'
    t[0] = Imprimir(t[5], t.lineno(1), col(t.slice[1]))
    
def p_print_v(t):
    'imprimir  : RCONSOLE PUNTO RLOG PARIZQ PARDER'
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
            | RANY
            | RNULL'''
    t[0] = Tipos(t[1].upper())

#Struct Exp
def p_variable(t):
    '''expresion : exp_struct'''
    t[0] = t[1]

def p_Expresion_Struct(t):
    '''exp_struct : exp_struct PUNTO ID'''
    t[0] = Variable(t[1],t.lineno(1), col(t.slice[3]),t[3])


def p_Expresion_Struct_lista(t):
    '''exp_struct : exp_struct PUNTO ID number_array''' 
    t[0] = Variable(t[1],t.lineno(1), col(t.slice[3]),t[3],t[4])
    

def p_expresion_struct_id(t):
    '''exp_struct : ID'''
    t[0] = Variable(t[1], t.lineno(1), col(t.slice[1]))
#Arrays
#id array
def p_expresion_array_id(t):
    '''exp_struct : ID number_array'''
    t[0] = Variable(t[1], t.lineno(1), col(t.slice[1]),None, t[2])
    
#number array

def p_expresion_id_content_unico(t):
    '''number_array : CORIZQ expresion CORDER'''
    if t[2] == None:
        t[0] = []
    else:
        t[0] = [t[2]]
        
def p_expresion_id_content(t):
    '''number_array : number_array CORIZQ expresion CORDER'''
    if t[3] != None:
        t[1].append(t[3])
    t[0] = t[1]

#Expresion_Array
def p_expresion_Array(t):
    '''expresion : CORIZQ expresion_exp CORDER'''
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


def p_push_expresion(t):
    '''expresion : RPUSH NOT PARIZQ expresion COMA expresion PARDER'''
    t[0] = PUSH(t[4], t[6], t.lineno(1), col(t.slice[1]))

def p_pop_expresion(t):
    '''expresion : RPOP NOT PARIZQ expresion PARDER'''
    t[0] = POP(t[4], t.lineno(1), col(t.slice[1]))
    
def p_length_expresion(t):
    '''expresion : RLENGTH PARIZQ expresion PARDER'''
    t[0] = LENGHT(t[3], t.lineno(1), col(t.slice[1]))
#nativas
def p_nativa_individual(t):
    '''expresion    : RTOFIXED PARIZQ expresion PARDER
                    | RTOSTRING PARIZQ expresion PARDER
                    | RTOEXPONENTIAL PARIZQ expresion PARDER
                    | RTYPEOF PARIZQ expresion PARDER
                    | RTOUPPERCASE PARIZQ expresion PARDER
                    | RTOLOWERCASE PARIZQ expresion PARDER'''    
    t[0] = Nativas(t.lineno(1), col(t.slice[4]), t[3], Nativas(t[1].upper()))
  
#expresiones
def p_expresion(t):
    '''expresion : expresion MAS expresion
                 | expresion MENOS expresion
                 | expresion POR expresion
                 | expresion DIVI expresion
                 | expresion POTENCIA expresion
                 | expresion MODULO expresion
                 | expresion IGUALIGUAL expresion
                 | expresion DIFERENTE expresion
                 | expresion MAYOR expresion
                 | expresion MENOR expresion
                 | expresion MAYORIGUAL expresion
                 | expresion MENORIGUAL expresion
                 | expresion AND expresion
                 | expresion OR expresion'''
    if t[2] == '+' or t[2] == '-' or t[2] == '*' or t[2] == '/' or t[2] == '%' or t[2] == '^':
        t[0] = Aritmetica(Aritmeticos(t[2]),t.lineno(1), col(t.slice[2]),t[1],t[3])
    elif t[2] == '==' or t[2] == '!=' or t[2] == '>' or t[2] == '>=' or t[2] == '<' or t[2] == '<=':
        t[0] = Relacional(Relacionales(t[2]),t.lineno(1), col(t.slice[2]),t[1],t[3])
    elif t[2] == '&&' or t[2] == '||':
        t[0] = Logicas(Logicas(t[2]),t.lineno(1), col(t.slice[2]),t[1],t[3])

def p_expresion_unaria(t):
    '''expresion    :  NOT expresion'''
    t[0] = Logicas(Logicas(t[1]),t.lineno(1), col(t.slice[1]),t[2])


   
def p_expresion_primitiva_int(t):
    'expresion    : RNUMBER'
    t[0] = Primitivo(Tipos.NUMBER, t[1], t.lineno(1), col(t.slice[1]))

def p_expresion_primitiva_string(t):
    'expresion    : RSTRING'    
    t[0] = Primitivo(Tipos.STRING, t[1], t.lineno(1), col(t.slice[1]))

def p_expresion_primitiva_bool(t):
    '''expresion    : RFALSE
                    | RTRUE'''
    if t[1]=='true':
        t[0] = Primitivo(Tipos.BOOLEAN, True, t.lineno(1), col(t.slice[1]))
    else:
        t[0] = Primitivo(Tipos.BOOLEAN, False, t.lineno(1), col(t.slice[1]))

def p_expresion_primitiva_any(t):
    '''expresion : RANY'''
    t[0] = Primitivo(Tipos.ANY, "any", t.lineno(1), col(t.slice[1]))

# def p_variable(t):
#     '''expresion : ID'''
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