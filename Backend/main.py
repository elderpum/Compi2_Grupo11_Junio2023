from fastapi import APIRouter,FastAPI
import sintactico as gramatica
import Tabla.Arbol as Arbol
import sys
import uvicorn

app = FastAPI()




@app.post('/Compilar')
def analysis(Contenido: str):
    try:
        sys.setrecursionlimit(100000)
        h = gramatica.parse(Contenido)
        ast = Arbol(h)
        ast.ejecutar()
        gramatica.start = ""
        return {"consola": ast.getConsola(), "Simbolo": ast.Lista .getLista(), "Errores": ast.errores, "AST": ast.graphAST()}
    except Exception as e:
        return {"error": str(e)}
    
    
if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=6600,
                reload=True, log_level="info", access_log=False)
