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
        "hola agente",
        "abrir el navegador brave",
        "reproducir musica youtube",
        "corre el script",
        "adiós",
        "quien eres tu",
        "abre la calculadora",
        "hola"
    ]
    
    print("\n" + "="*80)
    print(f"{'FRASE ENTRADA':<30} | {'INTENCION':<20} | {'ENTIDAD'}")
    print("-" * 80)

    for frase in pruebas:
        texto_procesar = frase.lower()
        
        intento = detectar_intencion(texto_procesar)
        entidad = extraer_entidad(texto_procesar)
        
        display_entidad = entidad if entidad else "---"
        
        print(f"{frase:<30} | {intento:<20} | {display_entidad}")

    print("="*80 + "\n")