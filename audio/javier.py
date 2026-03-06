import whisper
import sounddevice as sd
import numpy as np
from pynput import keyboard
import tempfile
import scipy.io.wavfile as wav
import os
import torch

# CARGAR EL MODELO FUERA
print("Cargando modelo Whisper...")
# Si te sigue dando error de memoria, cambia "medium" por "small"
device = "cuda" if torch.cuda.is_available() else "cpu"
MODELO_WHISPER = whisper.load_model("medium").to(device)

def iniciar_escucha_voz():
    samplerate = 16000
    resultado = [""] 
    estado = {"grabando": False, "audio_data": []}

    def audio_callback(indata, frames, time, status):
        if estado["grabando"]:
            estado["audio_data"].append(indata.copy())

    def on_press(key):
        if key == keyboard.Key.space and not estado["grabando"]:
            estado["audio_data"] = []
            estado["grabando"] = True

    def on_release(key):
        if key == keyboard.Key.space and estado["grabando"]:
            estado["grabando"] = False
            if len(estado["audio_data"]) > 0:
                audio_np = np.concatenate(estado["audio_data"], axis=0)
                audio_np = (audio_np * 32767).astype(np.int16)
                
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
                    wav.write(f.name, samplerate, audio_np)
                    # Transcribir con el modelo global
                    result = MODELO_WHISPER.transcribe(f.name)
                    resultado[0] = result["text"].strip()
                    os.remove(f.name)
                return False # Detiene el listener para devolver el string

    stream = sd.InputStream(samplerate=samplerate, channels=1, dtype="float32", callback=audio_callback)
    stream.start()

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    stream.stop()
    stream.close()
    return resultado[0]