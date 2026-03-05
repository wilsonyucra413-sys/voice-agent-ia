import whisper
import sounddevice as sd
import numpy as np
from pynput import keyboard
import tempfile
import scipy.io.wavfile as wav
import os

model = whisper.load_model("base")

samplerate = 16000
grabando = False
audio_data = []

def callback(indata, frames, time, status):
    global audio_data, grabando
    if grabando:
        audio_data.append(indata.copy())

def on_press(key):
    global grabando, audio_data

    if key == keyboard.Key.space and not grabando:
        print("🎤 Grabando...")
        audio_data = []
        grabando = True

def on_release(key):
    global grabando, audio_data

    if key == keyboard.Key.space and grabando:
        grabando = False
        print("Procesando...")

        if len(audio_data) == 0:
            print("No se capturó audio")
            return

        audio_np = np.concatenate(audio_data, axis=0)

        # convertir a int16
        audio_np = (audio_np * 32767).astype(np.int16)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
            wav.write(f.name, samplerate, audio_np)

            result = model.transcribe(f.name)
            texto = result["text"].strip()

            print("Texto detectado:", texto)

            os.remove(f.name)

stream = sd.InputStream(
    samplerate=samplerate,
    channels=1,
    dtype="float32",
    callback=callback
)

stream.start()

print("Mantén presionado ESPACIO para hablar")

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()       

#pip install pynput sounddevice numpy scipy openai-whisper     
# sudo apt install ffmpeg      
# sudo apt install ffmpeg portaudio19-dev         
# pip install torch --index-url https://download.pytorch.org/whl/cpu        
# portaudio19-dev → permite compilar y usar backend de audio en Linux. Es requerido por sounddevice.
# ffmpeg → se usa para procesar, convertir y leer muchos formatos de audio/video (Whisper lo usa internamente).
# torch → es el motor matemático de redes neuronales que ejecuta Whisper.
# pynput → detecta el teclado (tu espacio para grabar).
# numpy y scipy → manipulan la señal de audio.
# openai-whisper → el modelo de reconocimiento de voz. 
