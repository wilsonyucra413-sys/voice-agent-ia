import subprocess
import psutil
import time
from verifier.verifier import validar_apertura_app


def abrir_app(nombre_app):

    valido, mensaje = validar_apertura_app(nombre_app)

    if not valido:
        return False, mensaje

    try:
        subprocess.Popen(nombre_app)
        time.sleep(3)

        for proceso in psutil.process_iter(['name']):
            if nombre_app.lower() in proceso.info['name'].lower():
                return True, f"{nombre_app} se abrió correctamente"

        return False, f"No se detectó el proceso {nombre_app}"

    except Exception as e:
        return False, f"Error al abrir {nombre_app}: {str(e)}"


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