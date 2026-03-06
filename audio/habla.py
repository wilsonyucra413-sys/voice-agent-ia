import edge_tts
import asyncio
import pygame
import os
import tempfile

# Configuración de la voz
# Opciones sugeridas: es-MX-DaliaNeural (Mujer) o es-ES-AlvaroNeural (Hombre)
VOZ = "es-MX-DaliaNeural" 

def decir(texto):
    """Función puente para ejecutar la parte asíncrona desde el hilo de Streamlit"""
    if not texto:
        return
    try:
        # Ejecutamos el bucle de eventos asíncrono
        asyncio.run(_generar_y_reproducir(texto))
    except Exception as e:
        print(f"Error en la función decir: {e}")

async def _generar_y_reproducir(texto):
    # 1. Crear un archivo temporal único
    # Usamos mktemp para tener la ruta, pero lo manejamos nosotros
    fd, output_path = tempfile.mkstemp(suffix=".mp3")
    os.close(fd) # Cerramos el descriptor de archivo para que Pygame pueda usarlo

    try:
        # 2. Generar el audio con Edge TTS
        communicate = edge_tts.Communicate(texto, VOZ)
        await communicate.save(output_path)

        # 3. Inicializar PyGame Mixer si no está listo
        if not pygame.mixer.get_init():
            pygame.mixer.init()

        # 4. Reproducir
        pygame.mixer.music.load(output_path)
        pygame.mixer.music.play()

        # 5. Esperar a que termine de hablar (IMPORTANTE)
        # Usamos asyncio.sleep para no bloquear el procesador
        while pygame.mixer.music.get_busy():
            await asyncio.sleep(0.1)
        
        # 6. Descargar el archivo de la memoria (CRUCIAL para poder borrarlo)
        pygame.mixer.music.unload()

    except Exception as e:
        print(f"Error en la generación/reproducción de voz: {e}")

    finally:
        # 7. Limpiar el archivo temporal
        if os.path.exists(output_path):
            try:
                os.remove(output_path)
            except Exception as e:
                print(f"No se pudo borrar el temporal: {e}")