from ..Tabla.Tipo import Tipos
from ..Tabla.Tipo import Aritmeticos

Dic_Aritmetica = {
    #SUMA
    "NUMBER+NUMBER":[Tipos.NUMBER, Aritmeticos.SUMA],
    "NUMBER+STRING":[Tipos.STRING, Aritmeticos.SUMA],
    "STRING+STRING":[Tipos.STRING, Aritmeticos.SUMA],
    "NUMBER*NUMBER":[Tipos.NUMBER, Aritmeticos.RESTA],
    "NUMBER*NUMBER":[Tipos.NUMBER, Aritmeticos.MULTIPLICACION],
    "NUMBER/NUMBER":[Tipos.NUMBER, Aritmeticos.DIVISION],
    "NUMBER%NUMBER":[Tipos.NUMBER, Aritmeticos.MODULO],
    "NUMBER^NUMBER":[Tipos.NUMBER, Aritmeticos.POTENCIA],
}

D_Relacional = {
    # ===
    "NUMBER===NUMBER": Tipos.BOOL,
    "STRING===STRING": Tipos.BOOL,
    "BOOL===BOOL": Tipos.BOOL,
    "STRUCT===STRUCT": Tipos.BOOL,
    "ARRAY===ARRAY": Tipos.BOOL,
 
    "NUMBER!==NUMBER": Tipos.BOOL,
    "STRING!==STRING": Tipos.BOOL,
    "BOOL!==BOOL": Tipos.BOOL,
    "STRUCT!==STRUCT": Tipos.BOOL,
    "ARRAY!==ARRAY": Tipos.BOOL,

    "NUMBER!>=NUMBER": Tipos.BOOL,
    "NUMBER<=NUMBER": Tipos.BOOL,
    "NUMBER>NUMBER": Tipos.BOOL,
    "NUMBER<NUMBER": Tipos.BOOL,
}

D_LOGICA = {
    'BOOLEAN&&BOOLEAN': 'AND',
    'BOOLEAN||BOOLEAN': 'OR',
    '!BOOLEAN': 'NOT'
}


D_NATIVA = {
    #tofixed
    'TOFIXED-NUMBER':['float(math.trunc(valor))', Tipos.NUMBER],
    #tostring
    'TOSTRING-NUMBER':['str(valor)',Tipos.STRING],
    
    #uppercase y lowercase
    'UPPERCASE-STRING':['valor.upper()',Tipos.STRING],
    'LOWERCASE-STRING':['valor.lower()',Tipos.STRING],
    
    #ARREGLOS
    'PUSH-ARREGLO':['h'],
    'POP-ARREGLO':['hh'],
    'LENGTH-ARREGLO':['hhh']
}