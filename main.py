import streamlit as st
import streamlit.components.v1 as components
import threading
import os
import time
from streamlit.runtime.scriptrunner import add_script_run_ctx

# --- 1. IMPORTACIONES (Verificadas) ---
from audio.javier import iniciar_escucha_voz
from nlp.nlp import LimpiarTexto               # ARNOLD
from data.herberth import detectar_intencion   # HERBERTH
from executor.executor import ejecutar_accion  # CRISTHIAN
from audio.habla import decir 

# Configuración de página
st.set_page_config(page_title="Neural Agent Interface", layout="centered")

# Inicializar estados de sesión
if "texto_limpio" not in st.session_state: st.session_state.texto_limpio = ""
if "intencion" not in st.session_state: st.session_state.intencion = ""
if "entidad" not in st.session_state: st.session_state.entidad = ""
if "mensaje_sistema" not in st.session_state: st.session_state.mensaje_sistema = ""
if "ejecutar_rerun" not in st.session_state: st.session_state.ejecutar_rerun = False

# --- LÓGICA DEL HILO PROCESADOR ---
def hilo_procesador_voz():
    while True:
        try:
            texto_raw = iniciar_escucha_voz()
            
            # SOLUCIÓN AL NONETYPE: Si no hay audio, volver al inicio del bucle
            if texto_raw is None or not str(texto_raw).strip():
                continue 

            # Ahora es seguro usar Arnold
            texto_limpio = LimpiarTexto(str(texto_raw))
            
            resultado_ia = detectar_intencion(texto_limpio)
            intencion = resultado_ia["intencion"]
            entidades = resultado_ia["entidad"]
            
            entidad_final = entidades[0] if (entidades and len(entidades) > 0) else None
            
            # Ejecución
            res_acc = ejecutar_accion(intencion, entidad_final)
            mensaje_final = res_acc["mensaje"]

            # Hablar (Siempre intentamos hablar el resultado)
            threading.Thread(target=decir, args=(mensaje_final,), daemon=True).start()

            # Actualizar UI
            st.session_state.texto_limpio = texto_limpio
            st.session_state.intencion = intencion
            st.session_state.entidad = str(entidad_final) if entidad_final else ""
            st.session_state.mensaje_sistema = mensaje_final
            st.session_state.ejecutar_rerun = True 
                
        except Exception as e:
            # Si algo explota, el agente avisa por voz
            err_msg = "No puedo ejecutar esa accion."
            print(f"ERROR CRÍTICO: {e}")
            threading.Thread(target=decir, args=(err_msg,), daemon=True).start()
            time.sleep(1)
# Iniciar hilo de fondo
if "voz_activa" not in st.session_state:
    hilo = threading.Thread(target=hilo_procesador_voz, daemon=True)
    add_script_run_ctx(hilo) 
    hilo.start()
    st.session_state.voz_activa = True

# --- DISEÑO ELEGANTE (FRONTEND) ---
def elegant_voice_ui():
    html_code = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Syncopate:wght@400;700&family=Space+Grotesk:wght@300;400;600&display=swap');
        :root { --primary-glow: #00f2ff; --secondary-glow: #7000ff; --text-color: #ffffff; }
        body { background-color: transparent; margin: 0; display: flex; justify-content: center; align-items: center; height: 100vh; font-family: 'Space Grotesk', sans-serif; color: var(--text-color); overflow: hidden; }
        .main-container { display: flex; flex-direction: column; align-items: center; gap: 20px; }
        .orb-container { position: relative; width: 180px; height: 180px; display: flex; justify-content: center; align-items: center; }
        .ring { position: absolute; border-radius: 50%; border: 1px solid rgba(0, 242, 255, 0.1); transition: all 0.4s ease; }
        .outer-ring { width: 100%; height: 100%; border-left: 2px solid var(--primary-glow); animation: rotate 8s linear infinite; }
        .inner-ring { width: 75%; height: 75%; border-right: 2px solid var(--secondary-glow); animation: rotate-reverse 5s linear infinite; }
        .core-orb { width: 90px; height: 90px; background: radial-gradient(circle, #111 0%, #000 100%); border-radius: 50%; z-index: 5; border: 1px solid rgba(255,255,255,0.05); }
        .timer-box { font-size: 2.2rem; font-weight: 300; letter-spacing: -1px; margin: 10px 0; height: 50px; color: var(--text-color); opacity: 0.3; }
        .timer-box span { font-size: 0.9rem; color: var(--primary-glow); }
        .space-key { width: 200px; height: 45px; border: 1px solid rgba(255,255,255,0.2); border-radius: 10px; display: flex; justify-content: center; align-items: center; font-family: 'Syncopate', sans-serif; font-size: 0.55rem; letter-spacing: 4px; color: rgba(255,255,255,0.5); background: rgba(255,255,255,0.02); }
        
        .active .outer-ring { animation-duration: 1s; opacity: 1; }
        .active .inner-ring { animation-duration: 0.8s; opacity: 1; }
        .active .core-orb { transform: scale(1.1); box-shadow: 0 0 30px rgba(0, 242, 255, 0.3); border-color: var(--primary-glow); }
        .active .timer-box { opacity: 1; text-shadow: 0 0 15px rgba(255,255,255,0.3); }
        .active .space-key { transform: translateY(4px); background: var(--primary-glow); color: #000; box-shadow: 0 0 20px rgba(0, 242, 255, 0.4); }

        @keyframes rotate { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
        @keyframes rotate-reverse { from { transform: rotate(360deg); } to { transform: rotate(0deg); } }
    </style>
    <div class="main-container" id="ui-app">
        <div style="font-family:'Syncopate'; font-size:0.7rem; letter-spacing:8px; color:rgba(255,255,255,0.3); margin-bottom:10px;">Neural Agent</div>
        <div class="orb-container">
            <div class="ring outer-ring"></div>
            <div class="ring inner-ring"></div>
            <div class="core-orb"></div>
        </div>
        <div class="timer-box" id="timer">00:00<span>.00</span></div>
        <div class="space-key">HOLD SPACE</div>
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
                setTimeout(() => { if(!isPressed) timerDisplay.innerHTML = "00:00<span>.00</span>"; }, 1000);
            }
        });
    </script>
    """
    components.html(html_code, height=500)

st.markdown("""<style>.stApp { background-color: #050505; } header {visibility: hidden;} footer {visibility: hidden;}</style>""", unsafe_allow_html=True)

elegant_voice_ui()

# --- HUD DE RESULTADOS (DATOS SINCRONIZADOS) ---
if st.session_state.intencion:
    st.markdown(f"""
        <div style="text-align: center; font-family: 'Space Grotesk'; margin-top: -40px;">
            <div style="color: #00f2ff; font-family: 'Syncopate'; font-size: 0.6rem; letter-spacing: 4px; opacity: 0.6;">
                {st.session_state.intencion} {('• ' + st.session_state.entidad) if st.session_state.entidad else ''}
            </div>
            <div style="color: white; font-size: 1.2rem; margin: 8px 0; font-weight: 300;">
                "{st.session_state.texto_limpio}"
            </div>
            <div style="color: #888; font-size: 0.75rem; font-style: italic; border-top: 1px solid #222; padding-top: 10px; width: 280px; margin: 0 auto;">
                {st.session_state.mensaje_sistema}
            </div>
        </div>
    """, unsafe_allow_html=True)
if st.session_state.ejecutar_rerun:
    st.session_state.ejecutar_rerun = False
    st.rerun()