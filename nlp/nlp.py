import spacy
import re
from spacy import displacy
#esto es como un cerebro pequeño que entiende español
npl=spacy.load("es_core_news_sm")

#estas palabras son un por si acaso la libreria no considera estas palabras un stop word pero lo dudo
stop_word=["eh","ah","mmm","este","por favor","podrias","quisiera","amm","gracias"]
def LimpiarTexto(texto):
    #al pasarle el texto a spacy(npl) se convierte cada palabra en token

    tokens=npl(texto)
    tokensClean=[]

    # la r tratara las cadenas como crudas es decir \ puede tratarse como un caracter el
    # . es para coincidir con cualquier caracter
    # el + en este caso dice que sea uno o mas caracteres de cualquier tipo .+ => uno o mas caracteres que coincidan
    # en este caso como ya dijismo que la baarra se tratara como uncaracter especial pero en estecaso es un poco diferente ya que
    # la barra invertida mas otrocaracter en este caso el . se le quita su significado especial y hace que coincida el caracter literal
    # es decir que \. => coincida con el .
    regex=re.compile(r'.+\..+|\..+')

   
    for chunk in tokens:
        # print(chunk)
        script=bool(regex.match(chunk.text) )
        # print(chunk.is_stop)
        #con esto quiere decir que devulee true si esa palabra no aporta mucho significado a la oracion o que no dan mucha informacion
        # .is_stop," devuelve true o false si es una palabra vacia/comun spacy ya tiene una diccionario de palabras")
        # .is_punct," devuelve true o false si es un signo de puntuacion")
        # .is_alpha," devuelve true o false si esta compuesta solo por letras")
        # .like_url," devuelve true o false si tiene enlace url")
        #reglas para el limpiado, que no haya mayuscualas, no se permite emojis, eliminacion de titubeos o muletillas
        if chunk.is_stop==False and chunk.text.lower() not in stop_word and (chunk.is_alpha or chunk.is_digit or script or chunk.is_punct):
            tokensClean.append(chunk.lemma_.lower())

    return " ".join(tokensClean)


texto_sucio = "podrias abrir el firefox y chrome y ejecutar estos 2 script uno llamado .gitignore y hola.txt"

resultado = LimpiarTexto(texto_sucio)

print("Texto original:", texto_sucio)
print("Texto limpio:", resultado)