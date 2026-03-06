import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle
import os

from nlp.nlp import LimpiarTexto

# Rutas de archivos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, 'intenciones.csv')
MODELO_PATH = os.path.join(BASE_DIR, 'modelo.pkl')
VECTOR_PATH = os.path.join(BASE_DIR, 'vectorizador.pkl')

# Herberth: Lista de palabras que la IA debe identificar
# He incluido versiones en singular porque Arnold (NLP) lematiza las palabras
APPS_CONOCIDAS = [
    # Navegadores
    'google chrome', 'chrome', 'firefox', 'brave', 'opera', 'edge', 'navegador', 'internet',
    
    # Desarrollo
    'visual studio code', 'vscode', 'visual studio', 'sublime text', 'pycharm', 
    'terminal', 'consola', 'shell',
    
    # Ofimática
    'bloc de notas', 'notepad', 'editor de texto', 'gedit',
    'word', 'excel', 'powerpoint', 'documentos', 'hoja de calculo',
    
    # Media
    'spotify', 'vlc', 'steam', 'musica', 'video', 'youtube',
    
    # Sistema (Ubuntu)
    'calculadora', 'archivos', 'archivo', 'carpeta', 'explorador', 
    'configuracion', 'ajustes', 'ajuste', 'monitor del sistema',
    
    # Comunicación
    'discord', 'slack', 'telegram', 'zoom', 'whatsapp'
]
# SOLUCIÓN: Gatillos simplificados para que coincidan con la limpieza de Arnold
GATILLOS_BUSQUEDA = [
    'buscar youtube', 'reproducir video', 'reproducir', 'poner musica', 
    'poner video', 'poner', 'buscar internet', 'buscar', 'investigar', 
    'googlear', 'significar', 'que ser'
]

def entrenar():
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(f"No se encontro el archivo: {CSV_PATH}")

    df = pd.read_csv(CSV_PATH)

    # SOLUCIÓN CRÍTICA: Limpiamos el CSV con la función de Arnold ANTES de entrenar
    # Así el modelo aprende que "abrir navegador" es lo mismo que "abre el navegador"
    df['texto_limpio'] = df['texto'].apply(LimpiarTexto)

    vectorizador = TfidfVectorizer(ngram_range=(1, 2)) 
    x = vectorizador.fit_transform(df['texto_limpio']) # Entrenamos con texto limpio
    y = df['intencion']

    modelo = LogisticRegression(class_weight='balanced')
    modelo.fit(x, y)

    with open(MODELO_PATH, 'wb') as f: pickle.dump(modelo, f)
    with open(VECTOR_PATH, 'wb') as f: pickle.dump(vectorizador, f)

    print("Entrenamiento finalizado con éxito (Datos Limpios).")
    return modelo, vectorizador

def extraer_entidad(texto_limpio, intencion):
    texto_limpio = texto_limpio.lower()
    
    if intencion in ["BUSCAR_WEB", "BUSCAR_YOUTUBE"]:
        consulta = texto_limpio
        # Ordenamos gatillos por longitud para no cortar palabras mal
        for gatillo in sorted(GATILLOS_BUSQUEDA, key=len, reverse=True):
            if texto_limpio.startswith(gatillo):
                consulta = texto_limpio.replace(gatillo, "", 1)
                break
        return [consulta.strip()]

    if intencion in ["ABRIR_APP", "CERRAR_APP"]:
        encontradas = []
        for app in APPS_CONOCIDAS:
            if app in texto_limpio:
                encontradas.append(app)
        return encontradas if encontradas else None
    return None

def detectar_intencion(texto_limpio):
    # Si no existen los archivos o si el CSV cambió, re-entrenamos
    if not os.path.exists(MODELO_PATH) or not os.path.exists(VECTOR_PATH):
        modelo, vectorizador = entrenar()
    else:
        with open(MODELO_PATH, 'rb') as f: modelo = pickle.load(f)
        with open(VECTOR_PATH, 'rb') as f: vectorizador = pickle.load(f)
    
    X_entrada = vectorizador.transform([texto_limpio.lower()])
    intencion = modelo.predict(X_entrada)[0]
    entidades = extraer_entidad(texto_limpio, intencion)

    return {
        "intencion": intencion,
        "entidad": entidades
    }