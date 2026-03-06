import streamlit as st
import streamlit.components.v1 as components
import threading
import os
from streamlit.runtime.scriptrunner import add_script_run_ctx

# Importaciones de tus módulos
from audio.javier import iniciar_escucha_voz
from nlp.nlp import LimpiarTexto
from data.herberth import detectar_intencion 
from executor.executor import ejecutar_accion # <--- Importamos el ejecutor

# 1. Configuración de página
st.set_page_config(page_title="Neural Agent Interface", layout="centered")

# Inicializar estados de sesión
if "texto_limpio" not in st.session_state:
    st.session_state.texto_limpio = ""
if "intencion" not in st.session_state:
    st.session_state.intencion = ""
if "entidades" not in st.session_state:
    st.session_state.entidades = None
if "mensaje_sistema" not in st.session_state:
    st.session_state.mensaje_sistema = ""

# --- LÓGICA DEL HILO PROCESADOR Y EJECUTOR ---
def hilo_procesador_voz():
    while True:
        try:
            # 1. JAVIER: Escucha
            texto_raw = iniciar_escucha_voz()
            print(texto_raw)
            if texto_raw and len(texto_raw.strip()) > 0:
                # 2. ARNOLD: Limpia
                texto_limpio = texto_raw
                
                # 3. HERBERTH: Clasifica
                resultado_ia = detectar_intencion(texto_limpio)
                intencion = resultado_ia["intencion"]
                entidades = resultado_ia["entidad"]
                print(intencion, entidades)
                # 4. EXECUTOR: Ejecutar la acción en el sistema
                mensajes_ejecucion = []
                
                # Si hay varias entidades (ej: dos apps), ejecutamos para cada una
                if entidades and isinstance(entidades, list):
                    for ent in entidades:
                        res_acc = ejecutar_accion(intencion, ent)
                        mensajes_ejecucion.append(res_acc["mensaje"])
                else:
                    # Si no hay entidades (ej: un saludo o apagar), ejecutamos una vez
                    res_acc = ejecutar_accion(intencion, None)
                    mensajes_ejecucion.append(res_acc["mensaje"])
                
                # Unir mensajes para mostrar en pantalla
                mensaje_final = " | ".join(mensajes_ejecucion)

                # Actualizar st.session_state
                st.session_state.texto_limpio = texto_limpio
                st.session_state.intencion = intencion
                st.session_state.entidades = entidades
                st.session_state.mensaje_sistema = mensaje_final
                
                # Imprimir en consola del servidor (como pediste)
                print(f"\n[SISTEMA] Acción: {intencion}")
                print(f"[SISTEMA] Mensaje: {mensaje_final}\n")
                
                st.rerun()
                
        except Exception as e:
            print(f"Error en el ciclo de ejecución: {e}")

# Iniciar hilo
if "voz_activa" not in st.session_state:
    hilo = threading.Thread(target=hilo_procesador_voz, daemon=True)
    add_script_run_ctx(hilo) 
    hilo.start()
    st.session_state.voz_activa = True

# --- DISEÑO ---
def elegant_voice_ui():
    html_code = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Syncopate:wght@400;700&family=Space+Grotesk:wght@300;400;600&display=swap');
        :root { --primary-glow: #00f2ff; --secondary-glow: #7000ff; --bg-dark: #050505; --text-color: #ffffff; }
        body { background-color: transparent; margin: 0; display: flex; justify-content: center; align-items: center; height: 100vh; font-family: 'Space Grotesk', sans-serif; color: var(--text-color); overflow: hidden; }
        .main-container { display: flex; flex-direction: column; align-items: center; gap: 20px; }
        .orb-container { position: relative; width: 200px; height: 200px; display: flex; justify-content: center; align-items: center; }
        .ring { position: absolute; border-radius: 50%; border: 1px solid rgba(0, 242, 255, 0.1); transition: all 0.4s ease; }
        .outer-ring { width: 100%; height: 100%; border-left: 2px solid var(--primary-glow); animation: rotate 8s linear infinite; }
        .inner-ring { width: 75%; height: 75%; border-right: 2px solid var(--secondary-glow); animation: rotate-reverse 5s linear infinite; }
        .core-orb { width: 100px; height: 100px; background: radial-gradient(circle, #111 0%, #000 100%); border-radius: 50%; z-index: 5; border: 1px solid rgba(255,255,255,0.05); }
        .timer-box { font-size: 2.5rem; font-weight: 300; letter-spacing: -1px; margin: 10px 0; height: 60px; color: var(--text-color); opacity: 0.3; }
        .timer-box span { font-size: 1rem; color: var(--primary-glow); }
        .space-key { width: 220px; height: 50px; border: 1px solid rgba(255,255,255,0.2); border-radius: 12px; display: flex; justify-content: center; align-items: center; font-family: 'Syncopate', sans-serif; font-size: 0.6rem; letter-spacing: 4px; color: rgba(255,255,255,0.5); background: rgba(255,255,255,0.02); }
        
        .active .outer-ring { animation-duration: 1s; opacity: 1; }
        .active .inner-ring { animation-duration: 0.8s; opacity: 1; }
        .active .core-orb { transform: scale(1.1); box-shadow: 0 0 40px rgba(0, 242, 255, 0.2); border-color: var(--primary-glow); }
        .active .timer-box { opacity: 1; text-shadow: 0 0 15px rgba(255,255,255,0.3); }
        .active .space-key { transform: translateY(4px); background: var(--primary-glow); color: #000; box-shadow: 0 0 20px rgba(0, 242, 255, 0.4); }

        @keyframes rotate { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
        @keyframes rotate-reverse { from { transform: rotate(360deg); } to { transform: rotate(0deg); } }
    </style>
    <div class="main-container" id="ui-app">
        <div style="font-family:'Syncopate'; font-size:0.8rem; letter-spacing:8px; color:rgba(255,255,255,0.4); margin-bottom:20px;">Neural Voice Agent</div>
        <div class="orb-container">
            <div class="ring outer-ring"></div>
            <div class="ring inner-ring"></div>
            <div class="core-orb"></div>
        </div>
        <div class="timer-box" id="timer">00:00<span>.00</span></div>
        <div class="space-key">SPACE</div>
    </div>
    <script>
        let startTime; let timerInterval; let isPressed = false;
        const app = document.getElementById('ui-app');
        const timerDisplay = document.getElementById('timer');
        window.addEventListener('keydown', (e) => {
            if (e.code === 'Space' && !isPressed) {
                e.preventDefault(); isPressed = true;
                startTime = new Date().getTime();
                app.classList.add('active');
                timerInterval = setInterval(() => {
                    const now = new Date().getTime();
                    const diff = now - startTime;
                    const m = Math.floor(diff / 60000);
                    const s = Math.floor((diff % 60000) / 1000);
                    const ms = Math.floor((diff % 1000) / 10);
                    timerDisplay.innerHTML = `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}<span>.${String(ms).padStart(2, '0')}</span>`;
                }, 10);
            }
        });
        window.addEventListener('keyup', (e) => {
            if (e.code === 'Space' && isPressed) {
                isPressed = false;
                clearInterval(timerInterval);
                app.classList.remove('active');
                setTimeout(() => { if(!isPressed) timerDisplay.innerHTML = "00:00<span>.00</span>"; }, 1200);
            }
        });
    </script>
    """
    components.html(html_code, height=550)

st.markdown("""<style>.stApp { background-color: #050505; } header {visibility: hidden;} footer {visibility: hidden;}</style>""", unsafe_allow_html=True)

elegant_voice_ui()

# --- HUD DE RESULTADOS ---
if st.session_state.intencion:
    entidades = " • ".join(st.session_state.entidades) if st.session_state.entidades else "SISTEMA"
    st.markdown(f"""
        <div style="text-align: center; font-family: 'Space Grotesk'; margin-top: -30px;">
            <div style="color: #00f2ff; font-family: 'Syncopate'; font-size: 0.6rem; letter-spacing: 4px;">{st.session_state.intencion}</div>
            <div style="color: white; font-size: 1.3rem; margin: 5px 0;">"{st.session_state.texto_limpio}"</div>
            <div style="color: #7000ff; font-size: 0.8rem; font-weight: 600; text-transform: uppercase; margin-bottom: 10px;">{entidades}</div>
            <div style="color: #555; font-size: 0.75rem; font-style: italic; border-top: 1px solid #222; padding-top: 10px; width: 300px; margin: 0 auto;">
                {st.session_state.mensaje_sistema}
            </div>
        </div>
    """, unsafe_allow_html=True)