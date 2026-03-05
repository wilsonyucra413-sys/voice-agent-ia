import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Agent Voice Interface", layout="centered")

def elegant_voice_ui():
    html_code = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Syncopate:wght@400;700&family=Space+Grotesk:wght@300;400;600&display=swap');

        :root {
            --primary-glow: #00f2ff;
            --secondary-glow: #7000ff;
            --bg-dark: #050505;
            --text-color: #ffffff;
        }

        body {
            background-color: transparent;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            font-family: 'Space Grotesk', sans-serif;
            color: var(--text-color);
            overflow: hidden;
        }

        .main-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 20px;
        }

        /* Título */
        .header {
            font-family: 'Syncopate', sans-serif;
            font-size: 0.8rem;
            letter-spacing: 8px;
            color: rgba(255,255,255,0.4);
            text-transform: uppercase;
            margin-bottom: 20px;
        }

        /* Orb y HUD */
        .orb-container {
            position: relative;
            width: 200px;
            height: 200px;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .ring {
            position: absolute;
            border-radius: 50%;
            border: 1px solid rgba(0, 242, 255, 0.1);
            transition: all 0.4s ease;
        }

        .outer-ring {
            width: 100%;
            height: 100%;
            border-left: 2px solid var(--primary-glow);
            animation: rotate 8s linear infinite;
        }

        .inner-ring {
            width: 75%;
            height: 75%;
            border-right: 2px solid var(--secondary-glow);
            animation: rotate-reverse 5s linear infinite;
        }

        .core-orb {
            width: 100px;
            height: 100px;
            background: radial-gradient(circle, #111 0%, #000 100%);
            border-radius: 50%;
            z-index: 5;
            border: 1px solid rgba(255,255,255,0.05);
            display: flex;
            justify-content: center;
            align-items: center;
            transition: all 0.3s ease;
        }

        /* Cronómetro */
        .timer-box {
            font-size: 2.5rem;
            font-weight: 300;
            letter-spacing: -1px;
            margin: 10px 0;
            height: 60px;
            color: var(--text-color);
            opacity: 0.3;
            transition: all 0.3s;
        }

        .timer-box span {
            font-size: 1rem;
            color: var(--primary-glow);
        }

        /* EL BOTÓN DE ESPACIO VISUAL */
        .space-key {
            width: 220px;
            height: 50px;
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 12px;
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: 'Syncopate', sans-serif;
            font-size: 0.6rem;
            letter-spacing: 4px;
            color: rgba(255,255,255,0.5);
            background: rgba(255,255,255,0.02);
            transition: all 0.1s ease;
            box-shadow: 0 4px 0 rgba(255,255,255,0.1);
            margin-top: 20px;
        }

        /* ESTADO ACTIVO (Cuando se presiona Espacio) */
        .active .outer-ring { animation-duration: 1s; opacity: 1; }
        .active .inner-ring { animation-duration: 0.8s; opacity: 1; }
        
        .active .core-orb {
            transform: scale(1.1);
            box-shadow: 0 0 40px rgba(0, 242, 255, 0.2);
            border-color: var(--primary-glow);
        }

        .active .timer-box {
            opacity: 1;
            text-shadow: 0 0 15px rgba(255,255,255,0.3);
        }

        .active .space-key {
            transform: translateY(4px);
            box-shadow: 0 0px 0 transparent;
            background: var(--primary-glow);
            color: #000;
            border-color: var(--primary-glow);
            text-shadow: none;
            box-shadow: 0 0 20px rgba(0, 242, 255, 0.4);
        }

        @keyframes rotate { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
        @keyframes rotate-reverse { from { transform: rotate(360deg); } to { transform: rotate(0deg); } }

    </style>

    <div class="main-container" id="ui-app">
        <div class="header">Neural Voice Agent</div>
        
        <div class="orb-container">
            <div class="ring outer-ring"></div>
            <div class="ring inner-ring"></div>
            <div class="core-orb">
                <div id="visualizer"></div>
            </div>
        </div>

        <div class="timer-box" id="timer">00:00<span>.00</span></div>

        <div class="space-key" id="space-btn">SPACE</div>
    </div>

    <script>
        let startTime;
        let timerInterval;
        let isPressed = false;

        const app = document.getElementById('ui-app');
        const timerDisplay = document.getElementById('timer');
        const spaceBtn = document.getElementById('space-btn');

        function updateTimer() {
            const now = new Date().getTime();
            const diff = now - startTime;
            const m = Math.floor(diff / 60000);
            const s = Math.floor((diff % 60000) / 1000);
            const ms = Math.floor((diff % 1000) / 10);
            
            timerDisplay.innerHTML = 
                `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}<span>.${String(ms).padStart(2, '0')}</span>`;
        }

        window.addEventListener('keydown', (e) => {
            if (e.code === 'Space' && !isPressed) {
                e.preventDefault();
                isPressed = true;
                startTime = new Date().getTime();
                app.classList.add('active');
                timerInterval = setInterval(updateTimer, 10);
            }
        });

        window.addEventListener('keyup', (e) => {
            if (e.code === 'Space' && isPressed) {
                isPressed = false;
                clearInterval(timerInterval);
                app.classList.remove('active');
                
                // Efecto de guardado sutil antes de resetear
                setTimeout(() => {
                    if(!isPressed) {
                        timerDisplay.innerHTML = "00:00<span>.00</span>";
                    }
                }, 1200);
            }
        });
    </script>
    """
    components.html(html_code, height=600)

# Streamlit Styling
st.markdown("""
    <style>
        .stApp { background-color: #050505; }
        header {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

elegant_voice_ui()