import spacy
import re

nlp = spacy.load("es_core_news_sm")

# Palabras que Arnold eliminará siempre
stop_word = {"eh", "ah", "mmm", "este", "por favor", "podrias", "quisiera", "amm", "gracias", "asi", "que", "voy", "a", "poner", "quiero", "el", "la", "los", "las"}

verbos_gatillo = {
    "buscar", "busca", "investigar", "googlear", "consultar", "significa",
    "reproducir", "reproduce", "pon", "poner", "escuchar", "ver"
}

saludos_despedidas = {
    "hola", "hey", "buenos", "buenas", "dias", "tardes", "noches",
    "adios", "adiós", "hasta", "luego", "chao", "bye", "nos", "vemos"
}

def LimpiarTexto(texto):
    if not texto: return ""
    tokens = nlp(texto.lower())
    tokensClean = []
    modo_busqueda = False
    regex = re.compile(r'.+\..+|\..+')

    for token in tokens:
        if modo_busqueda:
            tokensClean.append(token.text)
            continue
        if token.text in saludos_despedidas:
            tokensClean.append(token.text)
            continue
        if token.text in verbos_gatillo or token.lemma_ in verbos_gatillo:
            modo_busqueda = True
            tokensClean.append(token.lemma_) # Convierte "busca" -> "buscar"
            continue
        isScript = bool(regex.match(token.text))
        if (not token.is_stop or isScript) and token.text not in stop_word and (not token.is_punct or isScript):
            tokensClean.append(token.lemma_)
    return " ".join(tokensClean)