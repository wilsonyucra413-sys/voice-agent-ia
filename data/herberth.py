import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle
import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, 'intenciones.csv')
MODELO_PATH = os.path.join(BASE_DIR, 'modelo.pkl')
VECTOR_PATH = os.path.join(BASE_DIR, 'vectorizador.pkl')

APPS_CONOCIDAS = [
    'navegador', 'internet', 'google chrome', 'chrome', 'firefox', 'brave', 'opera', 'edge',
    'visual studio code', 'visual studio', 'vscode', 'sublime text', 'pycharm', 'terminal', 'consola', 'shell',
    'bloc de notas', 'notepad', 'editor de texto', 'word', 'excel', 'powerpoint', 'documentos', 'hojas de calculo', 'write', 'calc',
    'spotify', 'youtube', 'musica', 'reproductor', 'vlc', 'video', 'steam',
    'calculadora', 'archivos', 'carpetas', 'explorador', 'configuracion', 'ajustes', 'monitor del sistema',
    'discord', 'slack', 'whatsapp', 'telegram', 'zoom'
]

GATILLOS_BUSQUEDA = [
    'busca en youtube', 'reproduce el video de', 'reproduce', 'pon musica de', 
    'pon el video de', 'pon', 'busca en internet', 'busca que es', 'investiga sobre', 
    'quien es', 'googlea', 'busca', 'que es'
]

def entrenar ():
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(f"No se encontro el archivo: {CSV_PATH}")

    df = pd.read_csv(CSV_PATH)

    vectorizador = TfidfVectorizer(ngram_range=(1, 2)) 
    x = vectorizador.fit_transform(df['texto'])
    y = df['intencion']

    modelo = LogisticRegression(class_weight='balanced')
    modelo.fit(x,y)

    with open(MODELO_PATH, 'wb') as f: pickle.dump(modelo, f)
    with open(VECTOR_PATH, 'wb') as f: pickle.dump(vectorizador, f)

    print ("Your training has finished")
    return modelo,vectorizador

def extraer_entidad(texto_limpio, intencion):
    texto_limpio = texto_limpio.lower()
    
    if intencion in ["BUSCAR_WEB", "BUSCAR_YOUTUBE"]:
        consulta = texto_limpio
        for gatillo in sorted(GATILLOS_BUSQUEDA, key=len, reverse=True):
            if texto_limpio.startswith(gatillo):
                consulta = texto_limpio.replace(gatillo, "", 1)
                break
        return [consulta.strip()]

    if intencion in ["ABRIR_APP", "CERRAR_APP"]:
        encontradas = []
        temp_texto = texto_limpio
        for app in sorted(APPS_CONOCIDAS, key=len, reverse=True):
            if app in temp_texto:
                encontradas.append(app)
                temp_texto = temp_texto.replace(app, "")
        return encontradas if encontradas else None

    return None

def detectar_intencion(texto_limpio): # FUNCION PRINCIPAL
    if not os.path.exists(MODELO_PATH) or not os.path.exists(VECTOR_PATH):
        modelo, vectorizador = entrenar()
    else:
        with open(MODELO_PATH, 'rb') as f: modelo = pickle.load(f)
        with open(VECTOR_PATH, 'rb') as f: vectorizador = pickle.load(f)
    
    texto = texto_limpio.lower()
    X_entrada = vectorizador.transform([texto])
    intencion = modelo.predict(X_entrada)[0]

    entidades = extraer_entidad(texto,intencion)

    return {
        "intencion": intencion,
        "entidad": entidades
    }

# ESTO ES UN EJEMPLO DE LO QUE DEVOLVERA
# {
#     "intencion": "ABRIR_APP",
#     "entidad": ["firefox", "code"]
# }

# if __name__ == "__main__":

#     pruebas = [
#         "abre el brave y el terminal",
#         "reproduce tuna papita",
#         "busca que es el esternocleidomastoideo",
#         "apaga la computadora",
#         "hola agente"
#     ]
#     for p in pruebas:
#         res = detectar_intencion(p)
#         print(f"ENTRADA: {p}")
#         print(f"SALIDA:  {res}\n")