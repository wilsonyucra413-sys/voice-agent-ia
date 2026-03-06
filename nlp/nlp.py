import spacy
import re
from spacy import displacy
npl=spacy.load("es_core_news_sm")
stop_word=["eh","ah","mmm","este","por favor","podrias","quisiera","amm","gracias","perra","puta","puto","zorra","carajo","mierda"]
def LimpiarTexto(texto):

    tokens=npl(texto)
    tokensClean=[]

    regex=re.compile(r'.+\..+|\..+')
    for chunk in tokens:

        script=bool(regex.match(chunk.text) )
        if chunk.is_stop==False and chunk.text.lower() not in stop_word and (chunk.is_alpha or chunk.is_digit or script):
            tokensClean.append(chunk.lemma_.lower())

    return " ".join(tokensClean)


# texto_sucio = "!!!podrias abrir el firefox y chrome y ejecutar estos 2 script uno llamado .gitignore y hola.txt"

# resultado = LimpiarTexto(texto_sucio)

# print("Texto original:", texto_sucio)
# print("Texto limpio:", resultado)