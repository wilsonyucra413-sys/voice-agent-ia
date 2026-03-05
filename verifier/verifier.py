import shutil
import socket

def hay_internet():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False


def app_instalada(nombre_app):
    return shutil.which(nombre_app) is not None


def validar_apertura_app(nombre_app):

    if not app_instalada(nombre_app):
        return False, f"La aplicación '{nombre_app}' no está instalada"

    if nombre_app in ["firefox", "google-chrome", "chromium"]:
        if not hay_internet():
            return False, "No hay conexión a internet"

    return True, "Validación correcta"