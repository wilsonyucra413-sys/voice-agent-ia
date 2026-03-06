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
    
}
# 3. COMANDOS DE SISTEMA (Verbos permitidos que NO activan búsqueda, pero son útiles)
# Si el usuario dice "caminar", como no está aquí, lo borramos.
comandos_sistema = {
    "abrir", "abre", 
    "cerrar", "cierra", 
    "apagar", "enciende", "prende", 
    "ejecutar", "crear", "borrar",
    "saludar", "despedir", "hola", "adios"
}

saludos_despedidas = {
    "hola", "hey", "buenos", "buenas", "dias", "tardes", "noches",
    "adios", "adiós", "hasta", "luego", "chao", "bye", "nos", "vemos"
}

def LimpiarTexto(texto):
    tokens = nlp(texto.lower())
    tokensClean = []
    
    modo_busqueda = False
    regex = re.compile(r'.+\..+|\..+')

    for token in tokens:
        
        # --- CASO 1: MODO BÚSQUEDA ACTIVO ---
        if modo_busqueda:
            tokensClean.append(token.text)
            continue

        # --- CASO 2: ¿ES UN SALUDO O DESPEDIDA? (NUEVO) ---
        # Si la palabra está en nuestra lista blanca, la guardamos EXACTA (token.text)
        # y usamos 'continue' para saltar las reglas de limpieza normales.
        if token.text in saludos_despedidas:
            tokensClean.append(token.text)
            continue

        # --- CASO 3: ¿ES UN GATILLO DE BÚSQUEDA? ---
        if token.text in verbos_gatillo or token.lemma_ in verbos_gatillo:
            modo_busqueda = True
            tokensClean.append(token.lemma_)
            continue

        # --- CASO 4: LIMPIEZA NORMAL ---
        isScript = bool(regex.match(token.text))
        
        # Filtro estricto: No basura, no stop words (excepto scripts)
        if (not token.is_stop or isScript) and token.text not in stop_word and (not token.is_punct or isScript):
            tokensClean.append(token.lemma_)

    return " ".join(tokensClean)


# texto_sucio = "abrir visuals studio code"

# resultado = LimpiarTexto(texto_sucio)

# print("Texto original:", texto_sucio)
# print("Texto limpio:", resultado)