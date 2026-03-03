import subprocess
import psutil
import time
import shutil
import socket


# 🔎 Verificar si hay internet
def hay_internet():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False


# 🔎 Verificar si la app existe
def app_instalada(nombre_app):
    return shutil.which(nombre_app) is not None


# 🚀 Abrir aplicación con validaciones
def abrir_app(nombre_app):

    # 1️⃣ Verificar si está instalada
    if not app_instalada(nombre_app):
        return False, f"La aplicación '{nombre_app}' no está instalada"

    # 2️⃣ Si es navegador, verificar internet
    if nombre_app in ["firefox", "google-chrome", "chromium"]:
        if not hay_internet():
            return False, "No hay conexión a internet"

    try:
        subprocess.Popen(nombre_app)
        time.sleep(3)

        # 3️⃣ Verificar si el proceso está activo
        for proceso in psutil.process_iter(['name']):
            if nombre_app.lower() in proceso.info['name'].lower():
                return True, f"{nombre_app} se abrió correctamente"

        return False, f"No se detectó el proceso {nombre_app}"

    except Exception as e:
        return False, f"Error al abrir {nombre_app}: {str(e)}"


# 🧾 Ejecutar script
def ejecutar_script(ruta_script):
    try:
        resultado = subprocess.run(
            ["python3", ruta_script],
            capture_output=True,
            text=True
        )

        if resultado.returncode == 0:
            return True, "Script ejecutado correctamente"
        else:
            return False, resultado.stderr

    except Exception as e:
        return False, f"Error ejecutando script: {str(e)}"


# 🎯 Función principal
def ejecutar_accion(intencion, entidad):

    if intencion == "ABRIR_APP":
        exito, mensaje = abrir_app(entidad)

    elif intencion == "EJECUTAR_SCRIPT":
        exito, mensaje = ejecutar_script(entidad)

    else:
        return {
            "exito": False,
            "mensaje": "Intención no reconocida"
        }

    return {
        "exito": exito,
        "mensaje": mensaje
    }