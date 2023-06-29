import ply.yacc as yacc
from src.TablaSimbolos.Traductor import Traductor
from Lexico import tokens, lexer, errores, find_column
from src.Instrucciones.Console import Console
from src.Instrucciones.DeclaracionVariables import DeclaracionVariables
from src.Instrucciones.If import If
from src.Expresiones.Aritmeticas import Aritmeticas
from src.Expresiones.Logicas import Logicas
from src.Expresiones.Relacionales import Relacionales
from src.Helpers.TiposDatos import Tipos
from src.Helpers.OperacionesLogicas import OperacionL
from src.Helpers.OperacionesRelacionales import OperacionR
from src.Helpers.TipoOperacionesAritmeticas import Operacion
from src.Expresiones.Identificador import Identificador
from src.Expresiones.Primitivas import Primitivas
from src.TablaSimbolos.Arbol import Arbol
from src.TablaSimbolos.TablaSimbolos import TablaSimbolos
from src.TablaSimbolos.Error import Error
from src.TablaSimbolos.Simbolo import Simbolo
from src.Instrucciones.LoopFor import LoopFor
from src.Instrucciones.Funciones import Funciones
from src.Instrucciones.LlamadaFunciones import LlamadaFuncion
from src.Instrucciones.ReturnC import Return
from src.Instrucciones.Asignacion import Asignacion
from src.Instrucciones.BreakC import Break
from src.Instrucciones.ContinueC import Continue
from src.Instrucciones.Nativas.toExponential import toExponential
from src.Instrucciones.Nativas.toLower import toLower
from src.Instrucciones.Nativas.toUpper import toUpper
from src.Instrucciones.Nativas.Split import Split
from src.Instrucciones.Nativas.Typeof import TypeOf
from src.Instrucciones.Nativas.toString import toString
from src.Instrucciones.Nativas.toFixed import toFixed
from src.Instrucciones.Nativas.Concat import Concat
from src.Instrucciones.Nativas.Length import Length
from src.Instrucciones.DeclaracionArreglo import DeclaracionArreglo
from src.Expresiones.AccesoArray import AccesoArray
from src.Instrucciones.AsignacionArrelgo import AsignacionArreglo
from src.Instrucciones.Nativas.Push import Push
from src.Instrucciones.Nativas.Number import Number
from src.Instrucciones.LoopForOf import ForOf
from src.Instrucciones.While import While
from src.Instrucciones.LoopForIn import ForIn
from src.TablaSimbolos.AtributoS import AtributoStruct
from src.TablaSimbolos.ElementoStruct import ElementoStruct
from src.Instrucciones.CreacionInterface import CreacionInterface
from src.Instrucciones.DeclaracionObjeto import DeclaracionObjeto
from src.Instrucciones.AsignacionAtributo import AsignacionAtributo
from src.Expresiones.AccesoAtributo import AccesoAtributo
import sys

sys.setrecursionlimit(10000)
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'IGUALDAD', 'DIFERENTE'),
    ('left', 'MENOR', 'MAYOR', 'MAYIGUAL', 'MENIGUAL'),
    ('left','MAS','MENOS'),
    ('left','MODULO'),
    ('left','POR','DIV'),
    ('right','POTENCIA'),
    ('left','PARIZQ', 'PARDER'),
    ('right','UMENOS', 'UNOT'),
)


def p_init(t):
    'init : instrucciones'
    t[0] = t[1]

def p_lista_instrucciones(t): 
    'instrucciones  : instrucciones instruccion'
    if t[2] != "":
        t[1].append(t[2])
    t[0] = t[1]
    
def p_intrucciones_2(t):
    'instrucciones  :  instruccion'
    if t[1] == "":
        t[0] = []
    else:
        t[0] = [t[1]]
        
def p_instrucciones_evaluar(t):
    '''instruccion :  nativas PTYCOMA
                    | declaraciones PTYCOMA
                    | condicional_ifs PTYCOMA
                    | ciclos PTYCOMA
                    | funciones PTYCOMA
                    | llamadaFuncion PTYCOMA
                    | cReturn PTYCOMA
                    | asignaciones PTYCOMA
                    | de_control PTYCOMA
                    | imprimir PTYCOMA
                    | creacionStruct PTYCOMA
                    | nativas
                    | declaraciones
                    | condicional_ifs
                    | ciclos
                    | funciones 
                    | llamadaFuncion 
                    | cReturn 
                    | asignaciones
                    | de_control
                    | imprimir
                    | creacionStruct
                    '''
    t[0] = t[1]
    
    
def p_declaracionObjeto(t):
    '''declaracionObjeto : RLET ID DOSPTS ID IGUAL LLIZQ atributos LLDER
    '''
    t[0] = DeclaracionObjeto(t[2],t[4],t[7],t.lineno(1), find_column(input, t.slice[1]))

def p_creacionStruct(t):
    '''creacionStruct : RINTERFACE ID LLIZQ atributos LLDER
    '''
    t[0] = CreacionInterface(t[2],t[4],t.lineno(1), find_column(input, t.slice[1]))

def p_atributos(t):
    '''atributos : conTipo
                | sinTipo
    '''
    t[0] = t[1]
    
def p_atributosSTipo(t):
    '''sinTipo : sinTipo COMA listaAtr
                | listaAtr
    '''
    if len(t) == 2:
        t[0] = [t[1]]
    else:
        t[1].append(t[3])
        t[0] = t[1]

def p_listaAtr(t):
    '''listaAtr : ID DOSPTS expresion
                
    '''
    t[0] = ElementoStruct(t[1],t[3])

def p_expresionStrucs(t):
    '''expresion : LLIZQ atributos LLDER
    '''
    t[0] = t[2]

def p_atributosTipo(t):
    '''conTipo : conTipo atributo 
                | atributo
    '''
    if len(t) == 2:
        t[0] = [t[1]]
    else:
        t[1].append(t[2])
        t[0] = t[1]
        
def p_atributo(t):
    '''atributo : ID DOSPTS tipo PTYCOMA
                | ID DOSPTS ID PTYCOMA
    '''
    t[0] = AtributoStruct(t[1],t[3])
def p_funcionesNativas(t):
    ''' nativas : exponencial
                | toLower
                | toUpper
                | toFixed
                | splitss
                | typeoff
                | toString
                | String
                | push
                | Concat
                | Length
                | Number
    '''
    t[0] = t[1]

def p_number(t):
    '''Number : NNUMBER PARIZQ expresion PARDER
    '''
    t[0] = Number(t[3],t.lineno(1), find_column(input, t.slice[1]))
def p_push(t):
    ''' push : ID PUNTO NPUSH PARIZQ expresion PARDER
                | ID PUNTO NPUSH PARIZQ CORIZQ paramsC CORDER PARDER
    '''
    if len(t) == 7:
        t[0] = Push(t[1],t[5],t.lineno(1), find_column(input, t.slice[1]))
    else:
        t[0] = Push(t[1],t[6],t.lineno(1), find_column(input, t.slice[1]))
def p_lenght(t):
    ''' Length : ID PUNTO NLENGTH PARIZQ PARDER 
               | ID PUNTO NLENGTH 
               | accesoArreglo PUNTO NLENGTH
               | accesoArreglo PUNTO NLENGTH PARIZQ PARDER
    '''
    t[0] = Length(t[1], t.lineno(1), 10)
    
def p_concat(t):
    ''' Concat : ID PUNTO NCONCAT PARIZQ CORIZQ paramsC CORDER PARDER
    '''
    t[0] = Concat(t[1],t[6],t.lineno(1), find_column(input, t.slice[1]))

# def p_expresionArreglos(t):
#     ''' expresion : CORIZQ paramsC CORDER
#     '''
#     t[0]= t[2]
def p_toFixed(t):
    ''' toFixed : ID PUNTO NFIXED PARIZQ expresion PARDER
    '''
    t[0] = toFixed(t[1],t[5],t.lineno(1), find_column(input, t.slice[1]))

def p_toString(t):
    ''' toString : ID PUNTO NTOSTRING PARIZQ PARDER
    '''
    t[0] = toString(t[1],t.lineno(1), find_column(input, t.slice[1]))

def p_String(t):
    ''' String : NSTRING PARIZQ ID PARDER
    '''
    t[0] = toString(t[3],t.lineno(1), find_column(input, t.slice[1]))

def p_typeoff(t):
    '''typeoff : NTYPEOF PARIZQ expresion PARDER
                | NTYPEOF PARIZQ PARDER
    '''
    if len(t) == 5:
        t[0] = TypeOf(t[3],t.lineno(1), find_column(input, t.slice[1]))
    else:
        t[0] = TypeOf(None,t.lineno(1), find_column(input, t.slice[1]))
def p_splits(t):    
    '''splitss : split
                | splitSin
    '''
    t[0] = t[1]
def p_split(t):
    'split : ID PUNTO NSPLIT PARIZQ expresion PARDER'
    t[0] = Split(t[1],t[5],t.lineno(1), find_column(input, t.slice[1]))
def p_splitsin(t):
    'splitSin : ID PUNTO NSPLIT PARIZQ  PARDER'
    t[0] = Split(t[1],None,t.lineno(1), find_column(input, t.slice[1]))
def p_toLower(t):
    ''' toLower : ID PUNTO NLOWER PARIZQ PARDER
    '''
    t[0] = toLower(t[1],t.lineno(1), find_column(input, t.slice[1]))
def p_toUpper(t):
    ''' toUpper : ID PUNTO NUPPER PARIZQ PARDER
    '''
    t[0] = toUpper(t[1],t.lineno(1), find_column(input, t.slice[1]))
def p_toExponential(t):
    '''exponencial : ID PUNTO NEXP PARIZQ expresion PARDER
    '''
    t[0] = toExponential(t[1],t[5],t.lineno(1), find_column(input, t.slice[1]))

def p_control(t): #agregar continue
    '''de_control : pBreak
                  | pContinue

    '''
    t[0] = t[1]
    
def p_break(t):
    ''' pBreak : RBREAK
    '''
    t[0] = Break(t.lineno(1), find_column(input, t.slice[1]))   

def p_continue(t):
    ''' pContinue : RCONTINUE
    '''
    t[0] = Continue(t.lineno(1), find_column(input, t.slice[1]))    
    
def p_asignaciones(t):
    '''asignaciones : asignacionVariable
                    | asignacionArreglo
                    | asignacionAtributo
    '''
    t[0]= t[1]
    
def p_asignacionAtributo(t):
    '''asignacionAtributo : ID PUNTO ID IGUAL expresion
    '''
    t[0] = AsignacionAtributo(t[1],t[3],t[5],t.lineno(1), find_column(input, t.slice[1]))
def p_asignacionArreglo(t):
    '''asignacionArreglo : ID dimensiones IGUAL expresion
    '''
    t[0] = AsignacionArreglo(t[1], t[2], t[4],t.lineno(1), find_column(input, t.slice[1]))
def p_asignacionVariable(t):
    '''asignacionVariable : ID IGUAL expresion
    '''
    t[0] = Asignacion(t[1], t[3],t.lineno(1), find_column(input, t.slice[1]) )
def p_returnC(t):
    ''' cReturn : RRETURN expresion
    '''
    t[0] = Return(t[2],t.lineno(1), find_column(input, t.slice[1]) )
    

def p_expresion_funcion(t):
    ''' expresion : llamadaFuncion
    '''
    t[0] = t[1]
def p_llamarFuncion(t):
    '''llamadaFuncion : llamadaParam
                        | llamadaSin
    '''
    t[0] = t[1]

def p_llamadaParam(t):
    ''' llamadaParam : ID PARIZQ paramsC PARDER
    '''
    t[0] = LlamadaFuncion(t[1], t[3],t.lineno(1), find_column(input, t.slice[1]) )
    
def p_parametrosL(t):
    ''' parametrosL : parametrosL COMA parametroL
                    | parametroL 
    '''
    
    if len(t) == 2:
        t[0] = [t[1]]
    else:
        t[1].append(t[3])
        t[0] = t[1]

def p_parametroL(t):
    ''' parametroL : ID DOSPTS tipo
                    | RLET ID DOSPTS tipo
                    | ID
                    | ID DOSPTS tipo CORIZQ CORDER
                    | RLET ID DOSPTS tipo CORIZQ CORDER
    '''
    if len(t) == 2:
        t[0] = {'tipo': Tipos.ANY, 'id': t[1]}
    elif len(t) == 4:
        t[0] = {'tipo': t[3], 'id': t[1]}
    elif len(t)==6:
        t[0] = {'tipo': t[3], 'id': t[1]}
    elif len(t)==7:
        t[0] = {'tipo': t[4], 'id': t[2]}
    else:
        t[0] = {'tipo': t[4], 'id': t[2]}

def p_llamadaS(t):
    ''' llamadaSin : ID PARIZQ  PARDER
    '''
    t[0] = LlamadaFuncion(t[1], [],t.lineno(1), find_column(input, t.slice[1]) )

def p_funciones(t):
    '''funciones : funcionesP
                | funcionesV
    '''
    t[0] = t[1]
def p_funcionesP(t):
    '''funcionesP : RFUNCTION ID PARIZQ parametrosL PARDER LLIZQ instrucciones LLDER
                    | RFUNCTION ID  PARIZQ parametrosL PARDER DOSPTS tipo LLIZQ instrucciones LLDER
    '''
    if len(t) == 9:
        t[0] = Funciones(t[2],t[4],t[7],Tipos.ANY,t.lineno(1), find_column(input, t.slice[1]))
    else: 
        t[0] = Funciones(t[2],t[4],t[9],t[7],t.lineno(1), find_column(input, t.slice[1]))
def p_paramsC(t):
    ''' paramsC : paramsC COMA paramC
                | paramC
    '''
    if len(t) == 2:
        t[0] = [t[1]]
    else:
        t[1].append(t[3])
        t[0] = t[1]

def p_paramC(t):
    ''' paramC : expresion
                | CORIZQ paramsC CORDER
    '''
    if len(t)== 2:
        t[0] = t[1]
    else:
        t[0] = t[2]

def p_funcionesV(t):
    '''funcionesV : RFUNCTION ID PARIZQ PARDER LLIZQ instrucciones LLDER
                    | RFUNCTION ID PARIZQ PARDER DOSPTS tipo LLIZQ instrucciones LLDER
    '''
    
    if len(t) == 8:
        t[0] = Funciones(t[2],[],t[6],Tipos.ANY,t.lineno(1), find_column(input, t.slice[1]))
    else: 
        t[0] = Funciones(t[2],[],t[8],t[6],t.lineno(1), find_column(input, t.slice[1]))

def p_imprimir(t):
    'imprimir : RCONSOLE PUNTO RLOG PARIZQ paramsC PARDER'
    t[0] = Console(t[5], t.lineno(1), find_column(input, t.slice[1]))
    
def p_declaraciones(t):
    '''declaraciones : declaracion_normal
                    | declaracion_sin_tipo_normal
                    | declaracion_sin_valor
                    | declaracion_sin_tipo_valor
                    | declaracionArray
                    | declaracionArrayAny
                    | declaracionObjeto
    '''
    t[0] = t[1]
    
def p_declaracionArrayAny(t):
    '''declaracionArrayAny : RLET ID IGUAL CORIZQ paramsC CORDER
    '''
    t[0] = DeclaracionArreglo(t[2],Tipos.ANY,t[5],t.lineno(1), find_column(input, t.slice[1]))
def p_declaracionArray1(t):
    '''declaracionArray : RLET ID DOSPTS tipo CORIZQ CORDER IGUAL CORIZQ paramsC CORDER
                        | RLET ID DOSPTS tipo CORIZQ CORDER
    '''
    if len(t) == 11:
        t[0] = DeclaracionArreglo(t[2],t[4],t[9],t.lineno(1), find_column(input, t.slice[1]))
    else: 
        t[0] = DeclaracionArreglo(t[2],t[4],[],t.lineno(1), find_column(input, t.slice[1]))
def p_declaracion_normal(t):
    'declaracion_normal : RLET ID DOSPTS tipo IGUAL expresion'
    t[0] = DeclaracionVariables(t[2], t[4], t[6], t.lineno(1), find_column(input, t.slice[1]))
    
    
def p_declaracionSinTipoNormal(t):
    '''declaracion_sin_tipo_normal : RLET ID IGUAL expresion
    '''
    t[0] = DeclaracionVariables(t[2], Tipos.ANY, t[4], t.lineno(1), find_column(input, t.slice[1]))
    
def p_declaracionSinValor(t):
    '''declaracion_sin_valor : RLET ID DOSPTS tipo
    '''
    t[0] = DeclaracionVariables(t[2],t[4], None,  t.lineno(1), find_column(input, t.slice[1]))
    
def p_declaracionSinTipoSinValor(t):
    '''declaracion_sin_tipo_valor : RLET ID
    '''
    t[0] = DeclaracionVariables(t[2],Tipos.ANY, None ,t.lineno(1), find_column(input, t.slice[1]))

#####################################

#####################################

def p_condicional_ifs(t):
    'condicional_ifs : bloqueifs'
    t[0] = t[1]

def p_bloqueIfs(t):
    '''bloqueifs : soloif
                | ifelse
    '''
    t[0] = t[1]

def p_soloif(t):
    '''soloif : RIF PARIZQ expresion PARDER LLIZQ instrucciones LLDER
    '''
    t[0] = If(t[3], t[6], None, t.lineno(1), find_column(input, t.slice[1]))

def p_ifelse(t):
    '''ifelse : RIF PARIZQ expresion PARDER LLIZQ instrucciones LLDER  velse
    '''
    t[0] = If(t[3],t[6], t[8], t.lineno(1), find_column(input, t.slice[1]))

def p_velse(t):
    ''' velse : RELSE soloelse
                | RELSE elseif
    '''
    t[0] = t[2]
def p_soloelse(t):
    ''' soloelse : LLIZQ instrucciones LLDER
    '''
    t[0] = t[2]

def p_elseif(t):
    ''' elseif : soloif
                | ifelse
    '''
    t[0] = [t[1]]

def p_ciclos(t):
    '''ciclos : cliclo_for
                | cicloForOf
                | cicloForIn
                | cicloWhile
    '''
    t[0]= t[1]

def p_cicloForin(t):
    '''cicloForIn : RWHILE PARIZQ  expresion PARDER LLIZQ instrucciones LLDER
    '''
    t[0] = While(t[3],t[6], t.lineno(1), find_column(input, t.slice[1]))

def p_cicloWhile(t):
    '''cicloWhile : RFOR PARIZQ declaraciones RIN CORIZQ paramsC CORDER PARDER LLIZQ instrucciones LLDER
                    | RFOR PARIZQ declaraciones RIN expresion PARDER LLIZQ instrucciones LLDER
    '''
    if len(t) == 12:
        t[0] = ForIn(t[3],t[6],t[10], t.lineno(1), find_column(input, t.slice[1]))
    else:
        t[0] = ForIn(t[3],t[5],t[8], t.lineno(1), find_column(input, t.slice[1]))
def p_cicloForOf(t):
    '''cicloForOf : RFOR PARIZQ declaraciones ROF CORIZQ paramsC CORDER PARDER LLIZQ instrucciones LLDER
                    | RFOR PARIZQ declaraciones ROF expresion PARDER LLIZQ instrucciones LLDER
    '''
    if len(t) == 12:
        t[0] = ForOf(t[3],t[6],t[10], t.lineno(1), find_column(input, t.slice[1]))
    else: 
        t[0] = ForOf(t[3],t[5],t[8], t.lineno(1), find_column(input, t.slice[1]))

def p_ciclo_for(t):
    'cliclo_for : RFOR PARIZQ declaraciones PTYCOMA expresion PTYCOMA expresion PARDER LLIZQ instrucciones LLDER'
    t[0] = LoopFor(t[3], t[5], t[7], t[10], t.lineno(1), find_column(input, t.slice[1]))

def p_tipo(t):
    '''tipo : RSTRING
            | RNUMBER
            | RBOOLEAN
            | RANY
            | ID
            '''
    if t[1] == 'string':
        t[0] = Tipos.STRING
    elif t[1] == 'number':
        t[0] = Tipos.NUMBER
    elif t[1] == 'boolean':
        t[0] = Tipos.BOOLEAN
    elif t[1] == 'any':
        t[0] = Tipos.ANY
    else: 
        t[0] = t[1]
    
def p_expresionAgrupada(t):
    '''expresion : PARIZQ expresion PARDER
    '''
    t[0] = t[2]

def p_expresion_binaria(t):
    '''expresion : expresion MAS expresion
                | expresion MENOS expresion
                | expresion POR expresion
                | expresion DIV expresion
                | expresion MODULO expresion
                | expresion POTENCIA expresion
                | expresion IGUALDAD expresion
                | expresion DIFERENTE expresion
                | expresion MAYOR expresion
                | expresion MENOR expresion
                | expresion MAYIGUAL expresion
                | expresion MENIGUAL expresion
                | expresion AND expresion
                | expresion OR expresion

                '''
    if t[2] == '+'  : 
        t[0] = Aritmeticas(t[1], t[3], Operacion.SUMA, t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '-':
        t[0] = Aritmeticas(t[1], t[3], Operacion.RESTA, t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '*': 
        t[0] = Aritmeticas(t[1], t[3], Operacion.MULTI, t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '/': 
        t[0] = Aritmeticas(t[1], t[3], Operacion.DIV, t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '%':
        t[0] = Aritmeticas(t[1], t[3], Operacion.MODULO, t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '^':
        t[0] = Aritmeticas(t[1], t[3], Operacion.POTENCIA, t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '===':
        t[0] = Relacionales(t[1], t[3], OperacionR.IGUALDAD, t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '!==':
        t[0] = Relacionales(t[1], t[3], OperacionR.DIFERENTE, t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '>':
        t[0] = Relacionales(t[1], t[3], OperacionR.MAYOR, t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '<':
        t[0] = Relacionales(t[1], t[3], OperacionR.MENOR, t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '>=':
        t[0] = Relacionales(t[1], t[3], OperacionR.MAYORI, t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '<=':
        t[0] = Relacionales(t[1], t[3], OperacionR.MENORI, t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '&&':
        t[0] = Logicas(t[1], t[3], OperacionL.AND, t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '||':
        t[0] = Logicas(t[1], t[3], OperacionL.OR, t.lineno(2), find_column(input, t.slice[2]))
        
def p_expresion_f_nativas(t):
    ''' expresion : nativas
    '''
    t[0] = t[1]
def p_expresion_unaria(t):
    '''expresion : MENOS expresion %prec UMENOS
                | NOT expresion %prec UNOT
                | expresion INCREMENTO 
                | expresion DECREMENTO 
                '''
                
    if t[1] == '-':
        t[0] = Aritmeticas(None, t[2], Operacion.RESTA, t.lineno(1), find_column(input, t.slice[1]))
    elif t[1] == '!':
        t[0] = Logicas(None, t[2], OperacionL.NOT, t.lineno(1), find_column(input, t.slice[1]))
    elif t[2] == '++':
        t[0] = Aritmeticas(None, t[1], Operacion.INCREMENTO, t.lineno(1), find_column(input, t.slice[2]))
    elif t[2] == '--':
        t[0] = Aritmeticas(None,t[1],Operacion.DECREMENTO, t.lineno(1), find_column(input, t.slice[2]))
        
def p_identificador(t):
    'expresion : ID'
    t[0] = Identificador(t[1], t.lineno(1), find_column(input, t.slice[1]), None)
    
def p_accesoExpre(t):
    '''expresion : accesoArreglo
                | accesoAtributo
    '''
    t[0] = t[1]

def p_listaAccesoAtributo(t):
    '''listaAtributo : listaAtributo atr
                    | atr
    '''
    if len(t) == 2:
        t[0] = [t[1]]
    else:
        t[1].append(t[2])
        t[0] = t[1]
def p_atr(t):
    '''atr : PUNTO ID
    '''
    t[0]= t[2]
def p_accesoAtributo(t):
    '''accesoAtributo : ID listaAtributo
    '''
    t[0] = AccesoAtributo(t[1],t[2], t.lineno(1), find_column(input, t.slice[1]))

def p_masDimensiones(t):
    '''dimensiones : dimensiones dimension
                    | dimension
    '''
    if len(t) == 2:
        t[0] = [t[1]]
    else:
        t[1].append(t[2])
        t[0] = t[1]

def p_dimension(t):
    ''' dimension : CORIZQ expresion CORDER
    '''
    t[0] = t[2]

def p_acccesoArreglo(t):
    ''' accesoArreglo : ID dimensiones
    '''
    t[0] = AccesoArray(t[1],t[2], t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_entero(t):
    'expresion : ENTERO'
    t[0] = Primitivas(Tipos.NUMBER, int(t[1]), t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_decimal(t):
    'expresion : DECIMAL'
    t[0] = Primitivas(Tipos.NUMBER, float(t[1]), t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_cadena(t):
    'expresion : CADENA'
    t[0] = Primitivas(Tipos.STRING, str(t[1]), t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_boolean(t):
    '''expresion : RTRUE
                | RFALSE'''
    if t[1] == 'true':
        t[0] = Primitivas(Tipos.BOOLEAN, True, t.lineno(1), find_column(input, t.slice[1]))
    else:
        t[0] = Primitivas(Tipos.BOOLEAN, False, t.lineno(1), find_column(input, t.slice[1]))
        
        
def p_error(t):
    print(" Error sintáctico en " + str(t.value)+ " "+str(t.lexer.lineno) + " "+str(t.lexer.lexpos)) 
    
    
def parse(inp):
    global errores
    global parser
    errores = []
    parser = yacc.yacc()
    global input
    input = inp
    lexer.lineno = 1
    return parser.parse(inp)



entrada = '''
console.log(10.5/2);
'''


genAux = Traductor()
genAux.limpiarTodo()
generador = genAux.obtenerInstancia()
instrucciones = parse(entrada)
ast = Arbol(instrucciones)
tsg = TablaSimbolos('Global')
ast.setTablaGlobla(tsg)
#print(ast.getInstrucciones())
if ast.getInstrucciones() != None:
    for instruccion in ast.getInstrucciones():
            if isinstance(instruccion, Funciones):
                ast.setFunciones(instruccion)
            if isinstance(instruccion, CreacionInterface):
                value = instruccion.interpretar(ast,tsg)
                if isinstance(value, Error):
                    ast.getErrores().append(value)
                    ast.updateConsola(value.toString())

if ast.getInstrucciones() != None:
    for instruccion in ast.getInstrucciones():
        
        if not(isinstance(instruccion, Funciones) ):
            if not(isinstance(instruccion,CreacionInterface)):
                value = instruccion.interpretar(ast,tsg)
                if isinstance(value, Error):
                    ast.getErrores().append(value)
                    ast.updateConsola(value.toString())
                instruccion.traducir(ast,tsg)
print('##############Consola')
print(ast.getConsola())
print('##############C3D')
print(generador.getCodigo())