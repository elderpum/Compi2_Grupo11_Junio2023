import sys
from flask import Flask, request
from flask_cors import CORS
from flask.helpers import url_for
from werkzeug.utils import redirect
import json
from src.TablaSimbolos.TablaSimbolos import TablaSimbolos
from src.TablaSimbolos.Error import Error
from src.TablaSimbolos.Arbol import Arbol
from src.Instrucciones.Funciones import Funciones
from src.Instrucciones.CreacionInterface import CreacionInterface
from src.TablaSimbolos.Traductor import Traductor
from Sintactico import parse as Analizar
from Lexico import errores, tokens, lexer


app = Flask(__name__)
app.config["DEBUG"] = True
CORS(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.post('/Compilar')
def salida():
    try:
        sys.setrecursionlimit(100000)
        global tmp_val
        tmp_val = request.json['Contenido'] 
        global Tabla
        genAux = Traductor()
        genAux.limpiarTodo()
        generador = genAux.obtenerInstancia()
        Tabla = {}
        instrucciones = Analizar(tmp_val)
        ast = Arbol(instrucciones)
        TsgGlobal = TablaSimbolos('Global')
        ast.setTablaGlobla(TsgGlobal)
        if ast.getInstrucciones() != None:
            for instruccion in ast.getInstrucciones():
                if isinstance(instruccion, Funciones):
                    ast.setFunciones(instruccion)
                if isinstance(instruccion, CreacionInterface):
                    value = instruccion.interpretar(ast, TsgGlobal)
                    if isinstance(value, Error):
                        ast.getErrores().append(value)
                        ast.updateConsola(value.toString())
        for error in errores:
            ast.setErrores(error)

        if ast.getInstrucciones() != None:
            for instruccion in ast.getInstrucciones():
                if not (isinstance(instruccion, Funciones)):
                    if not (isinstance(instruccion, CreacionInterface)):
                        value = instruccion.interpretar(ast, TsgGlobal)
                        if isinstance(value, Error):
                            ast.getErrores().append(value)
                            ast.updateConsola(value.toString())
                        instruccion.traducir(ast, TsgGlobal)

        global Simbolos
        Simbolos = ast.getTablaGlobal().getTabla()
        consola = str(ast.getConsola())
        c3d = str(generador.getCodigo())
        print('Consola: ', consola)
        print('Errores: ', ast.errores)
        diccioErrores = []
        diccioSimbolos = []
        for simbolo in ast.getTablaSimbolosGlobalInterpretada().values():
            objSimbolos = {
                'entorno': simbolo.entorno,
                'identificador': simbolo.identificador,
                'tipo': str(simbolo.tipo),
                'fila': simbolo.fila,
                'columna': simbolo.columna
            }
            diccioSimbolos.append(objSimbolos)
        for error in ast.errores:
            objError = {
                'tipo': error.tipo,
                'descripcion': error.descripcion,
                'linea': error.linea,
                'columna': error.columna,
                'fecha': error.fecha.strftime('%Y-%m-%d')
            }
            diccioErrores.append(objError)
        print(ast.getTablaSimbolosGlobalInterpretada())
        return json.dumps({'consola': consola, 'errores': diccioErrores, 'simbolos': diccioSimbolos, 'c3d': c3d})
    except Exception as e:
        return {"Error": str(e)}


if __name__ == '__main__':
    app.run(debug=True, port=5500)
