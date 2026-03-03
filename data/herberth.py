import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle
import os

CSV_PATH = 'intenciones.csv'
MODELO_PATH = 'modelo.pkl'
VECTOR_PATH = 'vectorizador.pkl'

def entrenar ():
    df = pd.read_csv(CSV_PATH)

    vectorizador = TfidfVectorizer()
    x = vectorizador.fit_transform(df['texto'])
    y = df['intencion']

    modelo = LogisticRegression()
    modelo.fit(x,y)

    with open(MODELO_PATH, 'wb') as f: pickle.dump(modelo, f)
    with open(VECTOR_PATH, 'wb') as f: pickle.dump(vectorizador, f)

    print ("Your training has finished")

def detectar_intencion(texto):
    if not os.path.exists(MODELO_PATH):
        entrenar()
    
    with open(MODELO_PATH, 'rb') as f: modelo = pickle.load(f)
    with open(VECTOR_PATH, 'rb') as f: vectorizador = pickle.load(f)

    X_entrada = vectorizador.transform([texto])
    intencion = modelo.predict(X_entrada)[0]

    return intencion

def extraer_entidad(texto):
    palabras = texto.split()
    if len(palabras) > 1:
        return palabras[-1]
    return None

if __name__ == "__main__":
    entrenar()
    
    pruebas = [
        "hola que tal agente",
        "puedes abrir el brave",
        "ponme algo de musica",
        "corre mi script",
        "ya me voy adios",
        "quien eres",
        "abre la calculadora rapido"
    ]
    
    print("\n--- TEST DE ESTRÉS DE LA IA ---")
    for t in pruebas:
        prediccion = detectar_intencion(t.lower())
        print(f"FRASE: {t:30} | INTENCION: {prediccion}")