import random
import subprocess
import time
import urllib.parse

import psutil

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
    "archivo": "nautilus",  
    "carpeta": "nautilus",  
    "explorador": "nautilus",
    "configuracion": "gnome-control-center",
    "ajustes": "gnome-control-center",

    # Comunicación
    "discord": "discord",
    "slack": "slack",
    "telegram": "telegram-desktop",
    "zoom": "zoom",
}
# TRADUCCIÓN DE PROCESOS (Para que cerrar funcione en Ubuntu)
MAPA_PROCESOS = {
    "libreoffice": "soffice.bin",
    "code": "code",
    "nautilus": "nautilus",
    "google-chrome": "chrome",
    "gnome-calculator": "gnome-calculator"
}

def abrir_app(nombre_app):
    nombre_app = nombre_app.lower()
    if nombre_app not in MAPA_APPS:
        return False, f"No conozco la aplicación '{nombre_app}'"

    comando_completo = MAPA_APPS[nombre_app]
    binario = comando_completo.split()[0] # Ej: 'libreoffice'

    # Validar si está instalado
    valido, mensaje = validar_apertura_app(binario)
    if not valido:
        return False, mensaje

    try:
        # Ejecutamos y nos olvidamos (esto evita que el script espere a la app)
        subprocess.Popen(comando_completo.split(), start_new_session=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # En Ubuntu, si el comando no dio error inmediato, asumimos que abrió bien
        return True, f"Abriendo {nombre_app}"

    except Exception as e:
        return False, f"Error al intentar abrir {nombre_app}: {str(e)}"

def cerrar_app(nombre_app):
    procesos_cerrados = 0
    nombre_app = nombre_app.lower()

    # 1. BUSCAR EL NOMBRE REAL DEL PROCESO
    # Si el usuario dice "visual studio code", buscamos en el mapa y obtenemos "code"
    nombre_proceso_real = MAPA_APPS.get(nombre_app, nombre_app)
    
    # Si el comando tiene argumentos (ej: "libreoffice --writer"), nos quedamos solo con la primera palabra
    nombre_proceso_real = nombre_proceso_real.split()[0]

    try:
        for proceso in psutil.process_iter(["pid", "name"]):
            try:
                # Obtenemos el nombre del proceso actual en el sistema
                proc_name = proceso.info.get("name").lower()
                
                # 2. COMPARACIÓN INTELIGENTE
                # Comprobamos si el nombre real (code) o el nombre común (visual studio code) 
                # están en el nombre del proceso del sistema
                if nombre_proceso_real in proc_name or nombre_app in proc_name:
                    proceso.kill()
                    procesos_cerrados += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        if procesos_cerrados > 0:
            return True, f"Se cerró {nombre_app} correctamente"
    
        # 3. SI FALLA, INTENTAR UN COMANDO DE SISTEMA (KILLALL) como último recurso
        else:
            try:
                subprocess.run(["killall", nombre_proceso_real], check=True, stderr=subprocess.DEVNULL)
                return True, f"Se cerró {nombre_app} usando killall"
            except:
                return False, f"No se encontró {nombre_app} abierto en el sistema"

    except Exception as e:
        return False, f"Error al intentar cerrar {nombre_app}: {str(e)}"

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
        "Hola, dime qué necesitas.",
    ]

    return True, random.choice(saludos)


def despedirse():
    despedidas = [
        "Hasta luego, que tengas un buen día.",
        "Nos vemos pronto.",
        "Adiós, cuídate mucho.",
        "Hasta la próxima.",
        "Fue un placer ayudarte, hasta luego.",
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
        return {"exito": False, "mensaje": "Intención no reconocida"}

    return {"exito": exito, "mensaje": mensaje}