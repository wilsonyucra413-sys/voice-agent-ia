import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, 'intenciones.csv')
MODELO_PATH = os.path.join(BASE_DIR, 'modelo.pkl')
VECTOR_PATH = os.path.join(BASE_DIR, 'vectorizador.pkl')

APPS_CONOCIDAS = [
    # Navegadores
    'navegador', 'internet', 'google chrome', 'chrome', 'firefox', 'brave', 'opera', 'edge',
    # Herramientas de Desarrollo
    'visual studio code', 'visual studio', 'vscode', 'sublime text', 'pycharm', 'terminal', 'consola', 'shell',
    # Ofimática y Texto
    'bloc de notas', 'notepad', 'editor de texto', 'word', 'excel', 'powerpoint', 'documentos', 'hojas de calculo', 'write', 'calc',
    # Entretenimiento / Media
    'spotify', 'youtube', 'musica', 'reproductor', 'vlc', 'video', 'steam'
    # Sistema
    'calculadora', 'archivos', 'carpetas', 'explorador', 'configuracion', 'ajustes', 'monitor del sistema',
    # Comunicación
    'discord', 'slack', 'whatsapp', 'telegram', 'zoom'
]
def entrenar ():
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(f"No se encontro el archivo: {CSV_PATH}")

    df = pd.read_csv(CSV_PATH)

    vectorizador = TfidfVectorizer()
    x = vectorizador.fit_transform(df['texto'])
    y = df['intencion']

    modelo = LogisticRegression()
    modelo.fit(x,y)

    with open(MODELO_PATH, 'wb') as f: pickle.dump(modelo, f)
    with open(VECTOR_PATH, 'wb') as f: pickle.dump(vectorizador, f)

    print ("Your training has finished")
    return modelo,vectorizador

def extraer_entidad(texto_limpio):
    texto_limpio = texto_limpio.lower()
    entidades_encontradas = []

    apps_ordenadas = sorted(APPS_CONOCIDAS, key=len, reverse=True)

    for app in APPS_CONOCIDAS:
        if app in texto_limpio:
            entidades_encontradas.append(app)
            texto_limpio = texto_limpio.replace(app, "")
    
    return entidades_encontradas if entidades_encontradas else None

def detectar_intencion(texto_limpio): # FUNCION PRINCIPAL
    if not os.path.exists(MODELO_PATH) or not os.path.exists(VECTOR_PATH):
        modelo, vectorizador = entrenar()
    else:
        with open(MODELO_PATH, 'rb') as f: modelo = pickle.load(f)
        with open(VECTOR_PATH, 'rb') as f: vectorizador = pickle.load(f)
    texto = texto_limpio.lower()
    X_entrada = vectorizador.transform([texto])
    intencion = modelo.predict(X_entrada)[0]

    entidades = extraer_entidad(texto)
    return {
        "intencion": intencion,
        "entidad": entidades
    }

# ESTO ES UN EJEMPLO DE LO QUE DEVOLVERA
# {
#     "intencion": "ABRIR_APP",
#     "entidad": ["firefox", "code"]
# }

if __name__ == "__main__":
    print("--- Iniciando prueba de Herberth ---")
    resultado = detectar_intencion("vamos abriendo el brave y la calculadora por favor")
    print(f"Resultado: {resultado}")