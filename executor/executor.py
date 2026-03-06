import subprocess
import psutil
import time
import urllib.parse
import random
from verifier.verifier import validar_apertura_app

MAPA_APPS = {

    # Navegadores
    "google chrome": "google-chrome",
    "chrome": "google-chrome",
    "firefox": "firefox",
    "brave": "brave-browser",
    "opera": "opera",
    "edge": "microsoft-edge",

    # Desarrollo
    "visual studio code": "code",
    "vscode": "code",
    "visual studio": "code",
    "sublime text": "subl",
    "pycharm": "pycharm",
    "terminal": "gnome-terminal",
    "consola": "gnome-terminal",
    "shell": "gnome-terminal",

    # Ofimática
    "bloc de notas": "gedit",
    "editor de texto": "gedit",
    "notepad": "gedit",
    "word": "libreoffice --writer",
    "excel": "libreoffice --calc",
    "powerpoint": "libreoffice --impress",

    # Media
    "spotify": "spotify",
    "vlc": "vlc",
    "steam": "steam",

    # Sistema
    "calculadora": "gnome-calculator",
    "archivos": "nautilus",
    "carpetas": "nautilus",
    "explorador": "nautilus",
    "configuracion": "gnome-control-center",
    "ajustes": "gnome-control-center",

    # Comunicación
    "discord": "discord",
    "slack": "slack",
    "telegram": "telegram-desktop",
    "zoom": "zoom"
}


def abrir_app(nombre_app):

    nombre_app = nombre_app.lower()

    if nombre_app not in MAPA_APPS:
        return False, f"No conozco la aplicación '{nombre_app}'"

    comando_real = MAPA_APPS[nombre_app]

    valido, mensaje = validar_apertura_app(comando_real.split()[0])

    if not valido:
        return False, mensaje

    try:
        subprocess.Popen(comando_real.split())
        time.sleep(3)

        for proceso in psutil.process_iter(['name']):
            if proceso.info['name'] and comando_real.split()[0] in proceso.info['name'].lower():
                return True, f"{nombre_app} se abrió correctamente"

        return False, f"No se detectó el proceso {nombre_app}"

    except Exception as e:
        return False, f"Error al abrir {nombre_app}: {str(e)}"


def cerrar_app(nombre_app):

    procesos_cerrados = 0

    try:
        for proceso in psutil.process_iter(['pid', 'name']):
            if proceso.info['name'] and nombre_app.lower() in proceso.info['name'].lower():
                proceso.kill()
                procesos_cerrados += 1

        if procesos_cerrados > 0:
            return True, f"Se cerraron {procesos_cerrados} procesos de {nombre_app}"
        else:
            return False, f"No se encontraron procesos de {nombre_app} abiertos"

    except Exception as e:
        return False, f"Error al cerrar {nombre_app}: {str(e)}"


def apagar_equipo():
    try:
        subprocess.run(["shutdown", "now"])
        return True, "El equipo se está apagando"

    except Exception as e:
        return False, f"Error al apagar el equipo: {str(e)}"


def buscar_web(consulta):
    try:
        consulta_codificada = urllib.parse.quote(consulta)
        url = f"https://www.google.com/search?q={consulta_codificada}"

        subprocess.Popen(["firefox", url])

        return True, f"Buscando '{consulta}' en Google"

    except Exception as e:
        return False, f"Error al buscar en la web: {str(e)}"


def buscar_youtube(consulta):
    try:
        consulta_codificada = urllib.parse.quote(consulta)
        url = f"https://www.youtube.com/results?search_query={consulta_codificada}"

        subprocess.Popen(["firefox", url])

        return True, f"Buscando '{consulta}' en YouTube"

    except Exception as e:
        return False, f"Error al buscar en YouTube: {str(e)}"


def saludar():
    saludos = [
        "Hola, ¿en qué puedo ayudarte?",
        "¡Hola! ¿Qué necesitas?",
        "Buenos días, ¿en qué te ayudo?",
        "¡Hey! Estoy listo para ayudarte.",
        "Hola, dime qué necesitas."
    ]

    return True, random.choice(saludos)


def despedirse():
    despedidas = [
        "Hasta luego, que tengas un buen día.",
        "Nos vemos pronto.",
        "Adiós, cuídate mucho.",
        "Hasta la próxima.",
        "Fue un placer ayudarte, hasta luego."
    ]

    return True, random.choice(despedidas)


def ejecutar_accion(intencion, entidad=None):

    if intencion == "ABRIR_APP":
        exito, mensaje = abrir_app(entidad)

    elif intencion == "CERRAR_APP":
        exito, mensaje = cerrar_app(entidad)

    elif intencion == "APAGAR_EQUIPO":
        exito, mensaje = apagar_equipo()

    elif intencion == "BUSCAR_WEB":
        exito, mensaje = buscar_web(entidad)

    elif intencion == "BUSCAR_YOUTUBE":
        exito, mensaje = buscar_youtube(entidad)

    elif intencion == "SALUDO":
        exito, mensaje = saludar()

    elif intencion == "DESPEDIDA":
        exito, mensaje = despedirse()

    else:
        return {
            "exito": False,
            "mensaje": "Intención no reconocida"
        }

    return {
        "exito": exito,
        "mensaje": mensaje
    }