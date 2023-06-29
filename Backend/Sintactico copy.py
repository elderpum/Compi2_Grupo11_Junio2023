import ply.yacc as yacc
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


precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'IGUALDAD', 'DIFERENTE'),
    ('left', 'MENOR', 'MAYOR', 'MAYIGUAL', 'MENIGUAL'),
    ('left','MAS','MENOS'),
    ('left','POR','DIV','MODULO'),
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
    '''instruccion : imprimir PTYCOMA
                    | declaracion_normal PTYCOMA
                    | condicional_ifs PTYCOMA
                    | cliclo_for PTYCOMA
                    '''
    t[0] = t[1]
    
def p_instrucciones_evaluar_1(t):
    '''instruccion : imprimir
                    | declaracion_normal
                    | condicional_ifs
                    | cliclo_for
                    '''
    t[0] = t[1]
    
def p_imprimir(t):
    'imprimir : RCONSOLE PUNTO RLOG PARIZQ expresion PARDER'
    t[0] = Console(t[5], t.lineno(1), find_column(input, t.slice[1]))
    
def p_declaracion_normal(t):
    'declaracion_normal : RLET ID DOSPTS tipo IGUAL expresion'
    t[0] = DeclaracionVariables(t[2], t[4], t[6], t.lineno(1), find_column(input, t.slice[1]))

def p_condicional_ifs(t):
    'condicional_ifs : RIF PARIZQ expresion PARDER LLIZQ instruciones LLDER'
    t[0] = If(t[3], t[5], None, t.lineno(1), find_column(input, t.slice[1]))

def p_instruccionifvacio(t):
    'condicional_ifs : RIF PARIZQ expresion PARDER LLIZQ LLDER'
    t[0] = If(t[2], None, None, t.lineno(1), t.lexpos(1))


def p_condicional_if_else(t):
    'condicional_ifs : RIF PARIZQ expresion PARDER LLIZQ instrucciones LLDER RELSE LLIZQ instrucciones LLDER'
    t[0] = If(t[3], t[6], t[10], t.lineno(1), find_column(input, t.slice[1]))
    
def p_condicional_if_elsevacio(t):
    'condicional_ifs : RIF PARIZQ expresion PARDER LLIZQ instrucciones LLDER RELSE LLIZQ LLDER'
    t[0] = If(t[3], t[6], None, t.lineno(1), find_column(input, t.slice[1]))
    

def p_condicional_if_else_if(t):
    'condicional_ifs :  RIF PARIZQ expresion PARDER LLIZQ instrucciones LLDER RELSE condicional_ifs'
    t[0] = If(t[3], t[6], None, t.lineno(1), find_column(input, t.slice[1]))
    
def p_condicional_if(t):
    'condicional_ifs : RIF PARIZQ expresion PARDER LLIZQ instrucciones LLDER'
    t[0] = If(t[3], t[6], None, t.lineno(1), find_column(input, t.slice[1]))

def p_ciclo_for(t):
    'cliclo_for : RFOR PARIZQ declaracion_normal PTYCOMA expresion PTYCOMA expresion PARDER LLIZQ instrucciones LLDER'
    t[0] = LoopFor(t[3], t[5], t[7], t[10], t.lineno(1), find_column(input, t.slice[1]))

def p_tipo(t):
    '''tipo : RSTRING
            | RNUMBER
            | RBOOLEAN'''
    if t[1] == 'string':
        t[0] = Tipos.STRING
    elif t[1] == 'number':
        t[0] = Tipos.NUMBER
    elif t[1] == 'boolean':
        t[0] = Tipos.BOOLEAN
    

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
        t[0] = Aritmeticas(None, t[1], Operacion.INCREMENTO, t.lineno(1), find_column(input, t.slice[1]))
    elif t[2] == '--':
        t[0] = Aritmeticas(None,t[1],Operacion.DECREMENTO, t.lineno(1), find_column(input, t.slice[1]))
        
def p_identificador(t):
    'expresion : ID'
    t[0] = Identificador(t[1], t.lineno(1), find_column(input, t.slice[1]), None)
    
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



entrada = '''let a : number = 5;
let b : number = 10;
let c : number = 15;
let saludo : string = "hola Aby, espero estes mejor";
if (true) {
    let a : number = 25;
    let b : number = 50;
    if(a===5){
        console.log("Ya salio compi 2");
        console.log("El valor de c es: ");
        console.log(c);
    }else if(a===25){
        console.log("Ya salio dasdascompi 2");
    }
    console.log(a%2);
    console.log(b);
}
/*for(let iterador = 0; i<10: i++){
    console.log(i);
}*/
console.log(a);
console.log(b);
console.log(10/2);
console.log(!true);
console.log(!false);
console.log("Al fin solucione el error de los strings" );
'''


instrucciones = parse(entrada)
ast = Arbol(instrucciones)
tsg = TablaSimbolos('Global')
ast.setTablaGlobla(tsg)
#print(ast.getInstrucciones())

if ast.getInstrucciones() != None:
    for instruccion in ast.getInstrucciones():
        value = instruccion.interpretar(ast,tsg)
        if isinstance(value, Error):
            ast.getErrores().append(value)
            ast.updateConsola(value.toString())
print(ast.getConsola())