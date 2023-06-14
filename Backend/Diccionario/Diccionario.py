from ..Tabla.Tipo import Tipos
from ..Tabla.Tipo import Aritmeticos

Dic_Aritmetica = {
    #SUMA
    "INT64+INT64":[Tipos.ENTERO, Aritmeticos.SUMA],
    "INT64+FLOAT64":[Tipos.FLOAT, Aritmeticos.SUMA],
    "FLOAT64+INT64":[Tipos.FLOAT, Aritmeticos.SUMA],
    "FLOAT64+FLOAT64":[Tipos.FLOAT, Aritmeticos.SUMA],
    "STRING*STRING":[Tipos.STRING, Aritmeticos.SUMA],
    "STRING^INT64":[Tipos.STRING, Aritmeticos.MULTIPLICACION],
    #RESTA
    "INT64-INT64":[Tipos.ENTERO, Aritmeticos.RESTA],
    "INT64-FLOAT64":[Tipos.FLOAT, Aritmeticos.RESTA],
    "FLOAT64-INT64":[Tipos.FLOAT, Aritmeticos.RESTA],
    "FLOAT64-FLOAT64":[Tipos.FLOAT, Aritmeticos.RESTA],
    #multiplicacion
    "INT64*INT64":[Tipos.ENTERO, Aritmeticos.MULTIPLICACION],
    "INT64*FLOAT64":[Tipos.FLOAT, Aritmeticos.MULTIPLICACION],
    "FLOAT64*INT64":[Tipos.FLOAT, Aritmeticos.MULTIPLICACION],
    "FLOAT64*FLOAT64":[Tipos.FLOAT, Aritmeticos.MULTIPLICACION],
    #división
    "NUMBER/NUMBER":[Tipos.NUMBER, Aritmeticos.DIVISION],
    #modulo
    "NUMBER%NUMBER":[Tipos.NUMBER, Aritmeticos.MODULO],
    #elevado
    "NUMBER^NUMBER":[Tipos.NUMBER, Aritmeticos.POTENCIA],
}

D_Relacional = {
    # ==
    "INT64==INT64": Tipos.BOOL,
    "FLOAT64==INT64": Tipos.BOOL,
    "FLOAT64==FLOAT64": Tipos.BOOL,
    "INT64==FLOAT64": Tipos.BOOL,
    
    "NOTHING==NOTHING": Tipos.BOOL,
    "RANGE==RANGE": Tipos.BOOL,
    "STRUCT==STRUCT": Tipos.BOOL,
    "ARRAY==ARRAY": Tipos.BOOL,
    "OBJECT==NOTHING": Tipos.BOOL,
    "OBJECT==OBJECT": Tipos.BOOL,
    
    "STRING==STRING": Tipos.BOOL,
    "BOOL==BOOL": Tipos.BOOL,
    # !=
    "INT64!=INT64": Tipos.BOOL,
    "FLOAT64!=INT64": Tipos.BOOL,
    "FLOAT64!=FLOAT64": Tipos.BOOL,
    "INT64!=FLOAT64": Tipos.BOOL,
    "STRING!=STRING": Tipos.BOOL,
    "BOOL!=BOOL": Tipos.BOOL,
    "NOTHING!=NOTHING": Tipos.BOOL,
    "RANGE!=RANGE": Tipos.BOOL,
    "STRUCT!=STRUCT": Tipos.BOOL,
    "ARRAY!=ARRAY": Tipos.BOOL,
    "OBJECT!=NOTHING": Tipos.BOOL,
    "OBJECT!=OBJECT": Tipos.BOOL,
    # >=
    "INT64>=INT64": Tipos.BOOL,
    "FLOAT64>=INT64": Tipos.BOOL,
    "FLOAT64>=FLOAT64": Tipos.BOOL,
    "INT64>=FLOAT64": Tipos.BOOL,
    "STRING>=STRING": Tipos.BOOL,
    "BOOL>=BOOL": Tipos.BOOL,
    # <=
    "INT64<=INT64": Tipos.BOOL,
    "FLOAT64<=INT64": Tipos.BOOL,
    "FLOAT64<=FLOAT64": Tipos.BOOL,
    "INT64<=FLOAT64": Tipos.BOOL,
    "STRING<=STRING": Tipos.BOOL,
    "BOOL<=BOOL": Tipos.BOOL,
    # >
    "INT64>INT64": Tipos.BOOL,
    "FLOAT64>INT64": Tipos.BOOL,
    "FLOAT64>FLOAT64": Tipos.BOOL,
    "INT64>FLOAT64": Tipos.BOOL,
    "STRING>STRING": Tipos.BOOL,
    "BOOL>BOOL": Tipos.BOOL,
    # <
    "INT64<INT64": Tipos.BOOL,
    "FLOAT64<INT64": Tipos.BOOL,
    "FLOAT64<FLOAT64": Tipos.BOOL,
    "INT64<FLOAT64": Tipos.BOOL,
    "STRING<STRING": Tipos.BOOL,
    "BOOL<BOOL": Tipos.BOOL
}

D_LOGICA = {
    'BOOL&&BOOL': 'and',
    'BOOL||BOOL': 'or',
    '!BOOL': 'not'
}


D_NATIVA = {
    #parse
    'PARSE-INT64-STRING':['int(valor)', Tipos.ENTERO],
    'PARSE-FLOAT64-STRING':['float(valor)', Tipos.FLOAT],
    #tofixed
    'TOFIXED-NUMBER':['float(math.trunc(valor))', Tipos.NUMBER],
    #string
    'STRING-NUMBER':['str(valor)',Tipos.STRING],
    
    #uppercase y lowercase
    'UPPERCASE-STRING':['valor.upper()',Tipos.STRING],
    'LOWERCASE-STRING':['valor.lower()',Tipos.STRING],
    
    #ARREGLOS
    'PUSH-ARREGLO':['h'],
    'POP-ARREGLO':['hh'],
    'LENGTH-ARREGLO':['hhh']
}