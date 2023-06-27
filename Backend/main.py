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
