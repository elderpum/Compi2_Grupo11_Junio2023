<<<<<<< HEAD
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

@app.route('/', methods = ['GET'])
def raiz():
    return {"mensaje":"Es en compilar, aqui no regresa nada crack"}


@app.route('/compilar', methods = ["POST","GET"])
def compilar():
    if request.method == "POST":
        entrada = request.data.decode("utf-8")
        entrada = json.loads(entrada)
        print(entrada)
        global tmp_val
        tmp_val = entrada["codigo"]
        return redirect(url_for("salida"))
    else:
        return {"mensaje": "No compilado"}

@app.route('/salida')
def salida():
    global tmp_val
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
                    value = instruccion.interpretar(ast,TsgGlobal)
                    if isinstance(value, Error):
                        ast.getErrores().append(value)
                        ast.updateConsola(value.toString())
    for error in errores:
        ast.setErrores(error)

    if ast.getInstrucciones() != None:
        for instruccion in ast.getInstrucciones():
            if not(isinstance(instruccion, Funciones)):
                if not(isinstance(instruccion,CreacionInterface)):
                    value = instruccion.interpretar(ast,TsgGlobal)
                    if isinstance(value, Error):
                        ast.getErrores().append(value)
                        ast.updateConsola(value.toString())
                    instruccion.traducir(ast,TsgGlobal)

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
            'descripcion' : error.descripcion,
            'linea':error.linea,
            'columna':error.columna,
            'fecha':error.fecha.strftime('%Y-%m-%d')
        }
        diccioErrores.append(objError)
    print(ast.getTablaSimbolosGlobalInterpretada())
    return json.dumps({'consola':consola,'errores': diccioErrores, 'simbolos': diccioSimbolos, 'c3d':c3d })



if __name__ == '__main__':
    app.run(debug = True, port = 5500)
=======
from fastapi import FastAPI
import gramatica
from Tabla.Arbol import Arbol
import sys
import uvicorn
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/Compilar')
def analysis(Contenido: str):
    try:
        global start
        global parse
        sys.setrecursionlimit(100000)
        h = gramatica.parse(Contenido)
        ast = Arbol(h)
        ast.ejecutar()
        gramatica.start = ""
        return {"consola": ast.getConsola(), "Simbolo": ast.Lista.getLista(), "Errores": ast.errores, "AST": ast.graphAST()}
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=6600,
                reload=True, log_level="info", access_log=False)
>>>>>>> main
