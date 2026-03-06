import spacy
import re

# Cargamos el modelo
nlp = spacy.load("es_core_news_sm")

# Lista de palabras basura o relleno que queremos ignorar AL PRINCIPIO
stop_word = {"eh", "ah", "mmm", "este", "por favor", "podrias", "quisiera", "amm", "gracias", "asi", "que", "voy", "a", "poner", "quiero", "el", "la", "los", "las"}

# Verbos que activan el "Modo Búsqueda" (preservar el texto exacto)
verbos_gatillo = {
    # Búsqueda
    "buscar", "busca", "investigar", "googlear", "consultar","significa"
    
    # Multimedia
    "reproducir", "reproduce", "pon", "poner", "escuchar", "ver",
    
    # Comunicación
    "enviar", "mandar", "escribir", "responder", "avisar",
    
    # Utilidades
    "traducir", "anotar", "recordar", "definir", "calcular",
    
    # Interacción
    "decir", "di", "repetir", "deletrear"
}

def LimpiarTexto(texto):
    tokens = nlp(texto.lower())
    tokensClean = []
    
    # Esta es la "Bandera". Empieza apagada (False).
    modo_busqueda = False
    
    # Tu Regex para detectar archivos con punto (scripts)
    regex = re.compile(r'.+\..+|\..+')

    for token in tokens:
        
        # ---------------------------------------------------------
        # CASO 1: ¿YA ACTIVAMOS EL MODO BÚSQUEDA?
        # ---------------------------------------------------------
        if modo_busqueda:
            # Si la bandera está levantada, guardamos TODO (incluido "que", "el", "la")
            # tal cual lo dijo el usuario (.text), sin lematizar.
            tokensClean.append(token.text)
            continue # Saltamos al siguiente token

        # ---------------------------------------------------------
        # CASO 2: ¿ES ESTE TOKEN UN ACTIVADOR? (Ej: "buscar", "reproducir")
        # ---------------------------------------------------------
        # Verificamos si la palabra o su lema está en nuestros gatillos
        if token.text in verbos_gatillo or token.lemma_ in verbos_gatillo:
            modo_busqueda = True
            tokensClean.append(token.lemma_) # Guardamos el verbo normalizado (ej: "reproducir")
            continue

        # ---------------------------------------------------------
        # CASO 3: LIMPIEZA NORMAL (Modo estricto)
        # ---------------------------------------------------------
        # Si no estamos buscando, aplicamos las reglas estrictas de siempre:
        # Quitamos stop words, puntuación y basura.
        
        isScript = bool(regex.match(token.text))
        
        # Si NO es stop word (o es script) Y NO es basura Y (NO es puntuación o es script)
        if (not token.is_stop or isScript) and token.text not in stop_word and (not token.is_punct or isScript):
            tokensClean.append(token.lemma_)

    # Unimos todo en una sola cadena de texto
    return " ".join(tokensClean)


# texto_sucio = "quiero que busques la lombriz"

# resultado = LimpiarTexto(texto_sucio)

# print("Texto original:", texto_sucio)
# print("Texto limpio:", resultado)