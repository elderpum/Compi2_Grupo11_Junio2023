from Tabla.Simbolo import Tipos
from Tabla.Tipo import Aritmeticos

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
    "NUMBER===NUMBER": Tipos.BOOLEAN,
    "STRING===STRING": Tipos.BOOLEAN,
    "BOOL===BOOL": Tipos.BOOLEAN,
    "STRUCT===STRUCT": Tipos.BOOLEAN,
    "ARRAY===ARRAY": Tipos.BOOLEAN,
 
    "NUMBER!==NUMBER": Tipos.BOOLEAN,
    "STRING!==STRING": Tipos.BOOLEAN,
    "BOOL!==BOOL": Tipos.BOOLEAN,
    "STRUCT!==STRUCT": Tipos.BOOLEAN,
    "ARRAY!==ARRAY": Tipos.BOOLEAN,

    "NUMBER!>=NUMBER": Tipos.BOOLEAN,
    "NUMBER<=NUMBER": Tipos.BOOLEAN,
    "NUMBER>NUMBER": Tipos.BOOLEAN,
    "NUMBER<NUMBER": Tipos.BOOLEAN,
}

D_LOGICA = {
    'BOOLEAN&&BOOLEAN': 'AND',
    'BOOLEAN||BOOLEAN': 'OR',
    '!BOOLEAN': 'NOT'
}


D_NATIVA = {
    #tofixed
    'TOFIXED-NUMBER-NUMBER':['float(math.trunc(valor))', Tipos.NUMBER],
    'CONCAT-STRING-STRING':['', Tipos.STRING],
    'CONCAT-ARRAY-STRING':['', Tipos.ARRAY],
    #tostring
    'TOSTRING-NUMBER':['str(valor)',Tipos.STRING],
    'TOSTRING-BOOLEAN':['str(valor)',Tipos.STRING],

    #uppercase y lowercase
    'UPPERCASE-STRING':['valor.upper()',Tipos.STRING],
    'LOWERCASE-STRING':['valor.lower()',Tipos.STRING],
    
    #ARREGLOS
    'PUSH-ARREGLO':['h'],
    'POP-ARREGLO':['hh'],
    'LENGTH-ARREGLO':['hhh']
}