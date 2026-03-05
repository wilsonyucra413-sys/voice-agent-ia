import spacy
import re

#esto es como un cerebro pequeño que entiende español
# npl=spacy.load("es_core_news_sm")
# #estas palabras son un por si acaso, si la libreria no considera estas palabras un stop word pero lo dudo
# stop_word=["eh","ah","mmm","este","por favor","podrias","quisiera","amm","gracias","llamado","llamar","estos"]
# def LimpiarTexto(texto):
#     #al pasarle el texto a spacy(npl) se convierte cada palabra en token

#     tokens=npl(texto.lower())
#     tokensClean=[]

#     # la r tratara las cadenas como crudas es decir \ puede tratarse como un caracter el
#     # . es para coincidir con cualquier caracter
#     # el + en este caso dice que sea uno o mas caracteres de cualquier tipo .+ => uno o mas caracteres que coincidan
#     # en este caso como ya dijismo que la baarra se tratara como uncaracter especial pero en estecaso es un poco diferente ya que
#     # la barra invertida mas otrocaracter en este caso el . se le quita su significado especial y hace que coincida el caracter literal
#     # es decir que \. => coincida con el .
#     regex=re.compile(r'.+\..+|\..+')

    
#     for token in tokens:
        
#         # 3. Buscamos los VERBOS (Las acciones principales como "encender" o "poner")
        
#         if token.pos_ == "VERB":
#             accion = token.lemma_  # Lematizamos el verbo (ej: "enciende" -> "encender")
#             parametros =[]
            
#             # 4. Buscamos a los "hijos" de ese verbo (las palabras que le pertenecen)
#             for hijo in token.children:
                
#                 isScript=bool(regex.match(hijo.text))
                
#                 # 5. ¡AQUÍ APLICAMOS TU LIMPIEZA! 
#                 # Solo tomamos al hijo si NO es stop word, NO es puntuación, etc.
#                 if (not hijo.is_stop or isScript) and hijo.text not in stop_word and (not hijo.is_punct or isScript) :
                    
#                     parametros.append(hijo.lemma_)
                    
#                     # (Opcional) A veces el objeto tiene otra palabra pegada, ej: "luz" -> "sala"
#                     # Buscamos los "nietos" del verbo
#                 for nieto in hijo.children:
#                     isScriptni=bool(regex.match(nieto.text))
#                     if (not nieto.is_stop or isScriptni) and (not nieto.is_punct or isScriptni) and nieto.text not in stop_word:
#                         parametros.append(nieto.lemma_)
#                         for bisnieto in nieto.children:
#                             isScriptbis=bool(regex.match(bisnieto.text))
#                             if (not bisnieto.is_stop or isScriptbis) and (not bisnieto.is_punct or isScriptbis) and bisnieto.text not in stop_word:
#                                     parametros.append(bisnieto.lemma_)
#             if parametros:
#                 tokensClean.append({
#                     "comando":accion,
#                     "objetivos":parametros
#                 })       
            
#             # 6. Empaquetamos la acción descubierta con sus parámetros limpios
        
#     print(tokensClean)
#         # print(chunk.is_stop)
#         #con esto quiere decir que devulee true si esa palabra no aporta mucho significado a la oracion o que no dan mucha informacion
#         # .is_stop," devuelve true o false si es una palabra vacia/comun spacy ya tiene una diccionario de palabras")
#         # .is_punct," devuelve true o false si es un signo de puntuacion")
#         # .is_alpha," devuelve true o false si esta compuesta solo por letras")
#         # .like_url," devuelve true o false si tiene enlace url")
#         #reglas para el limpiado, que no haya mayuscualas, no se permite emojis, eliminacion de titubeos o muletillas
#         # if chunk.is_stop==False and chunk.text.lower() not in stop_word and (chunk.is_alpha or chunk.is_digit or script or chunk.is_punct):
#         #     tokensClean.append(chunk.lemma_)

#     return tokensClean

# texto_sucio = "Podrias Abrir el Firefox y chrome y podrias ejecutar estos 2 script uno llamado .gitignore y hola.txt"
# resultado = LimpiarTexto(texto_sucio)

# print("Texto original:", texto_sucio)
# for i in resultado:
#     print(i)


#cerebro pequeño que entiende el español
nlp = spacy.load("es_core_news_sm")

# Añadimos más palabras de relleno a ignorar
stop_word = {"eh", "ah", "mmm", "este", "por favor", "podrias", "podrías", "quisiera", "amm", "gracias", "uno", "llamado", "llamar", "estos", "y", "el", "la", "los", "las"}

def LimpiarTexto(texto):
    doc = nlp(texto.lower())

    #expresion regular que toma encuenta auqellos caracteres que seas scripts
    regex = re.compile(r'.+\..+|\..+')
    
    acciones_encontradas =[]
    accion_actual = None
    parametros_actuales =[]
    
    for token in doc:

        isScript = bool(regex.match(token.text))
        
        # 1. ¿ES UN VERBO DE ACCIÓN? (Ignoramos "script" y palabras de cortesía)
        #verifica si es un verbo y si no se encuentra en el diccionario de las palabras y si no es una stop_word y si la expresion con la que se hace comparacion es falsa y si el texto actual es distinto a script ya que por defecto la lista de spacy la palabra script lo toma como si fuese un verbo
        es_verbo_valido = token.pos_ in["VERB", "AUX"] and token.text not in stop_word and token.lemma_ not in stop_word and not isScript and token.text != "script"
        

        #si es un verbo
        if es_verbo_valido:
            # Si ya teníamos una acción anterior guardando parámetros, la empaquetamos
            if accion_actual is not None and len(parametros_actuales) > 0:
                acciones_encontradas.append({
                    "comando": accion_actual,
                    "objetivos": parametros_actuales
                })
            
            # Abrimos una NUEVA caja para la nueva acción
            accion_actual = token.lemma_
            parametros_actuales =[]
            
        # 2. SI NO ES VERBO, PERO YA TENEMOS UNA CAJA ABIERTA, LO EVALUAMOS COMO PARÁMETRO
        elif accion_actual is not None:
            
            if isScript:
                # Si es un script (.gitignore), lo guardamos tal cual
                parametros_actuales.append(token.text)
                
            else:
                # Filtro normal: Que no sea puntuación, stop word, ni basura
                if not token.is_punct and not token.is_stop and token.text not in stop_word:
                    # Guardamos el lema de la palabra
                    parametros_actuales.append(token.lemma_)
                    
    # 3. Al terminar toda la oración, empaquetamos la última caja que quedó abierta
    #si el ultimo verbo es distinto de nonte y hay palabras que no sean verbos empaquetamos la lista
    if accion_actual is not None and len(parametros_actuales) > 0:
        acciones_encontradas.append({
            "comando": accion_actual,
            "objetivos": parametros_actuales
        })
        
    return acciones_encontradas

# --- PRUEBA ---
texto_sucio = "abre el crhome y el notepad"#Podrias Abrir el Firefox y chrome y podrias ejecutar estos 2 script uno llamado .gitignore y hola.txt"
resultado = LimpiarTexto(texto_sucio)

print("Lo que entendió la computadora:")
for i in resultado:
    print(i)