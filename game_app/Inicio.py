import streamlit as st
import random
from paths import FORM_PATH, GAME_PATH, RANKING_PATH, STATISTICS_PATH

st.set_page_config(
    page_title="PyTrivia - Grupo 08",
    page_icon="🎮",
)

#Esto define el estilo de la aplicación, cambiando el color de fondo.
st.markdown(  
    """
    <style>
    .stApp {
        background: rgb(0,0,0);
        background: linear-gradient(180deg, rgba(0,0,0,1) 0%, rgba(17,9,43,1) 40%, rgba(34,18,87,1) 88%, rgba(56,30,144,1) 100%);
        
    }
    
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

    .welcome-message {
        background-color: #e0ffff;
        padding: 20px;
        border-radius: 10px;
        font-family: Arial, sans-serif;
        color: 00ffff;
    }

    @keyframes glowing {
        50% { text-shadow: 0 0 20px #00ffff, 0 0 30px #00ffff, 0 0 40px #00ffff, 0 0 50px #00ffff; }
        100% { text-shadow: 0 0 10px #00ffff, 0 0 20px #00ffff, 0 0 30px #00ffff, 0 0 40px #00ffff; }
    }
    .welcome-text {
        font-size: 18px;
        color: white;
    }

    .instruction-text {
        font-size: 15px;
        font-family: 'Press Start 2P', cursive;
        animation: glowing 1.5s infinite; 
        text-shadow: 0 0 10px #00ffff, 0 0 20px #00ff00, 0 0 30px #0000ff, 0 0 40px #ff00ff;
    }

    .star {
        position: fixed;
        width: 2.5px;
        height: 2.5px;
        background: white;
        box-shadow: 999px 999px white;
        animation: blink 1.5s infinite;
    }
    @keyframes blink {
        0%, 100% { opacity: 0.2; }
        50% { opacity: 1; }
    }
        </style>
    """,
    unsafe_allow_html=True)

stars_html = ""
for _ in range(100):  # Puedes ajustar el número de estrellas
    top = random.randint(0, 100)
    left = random.randint(0, 100)
    delay = random.uniform(0, 1.5)
    stars_html += f'<div class="star" style="top:{top}%;left:{left}%;animation-delay:{delay}s;"></div>'

st.markdown(
f"""
<body>
    {stars_html}
</body>
""",
unsafe_allow_html=True
)


def main():
    st.markdown(
        """
        <body class="star">
            <div>
                <h2 style="text-align: center; color: #00ffff; font-family: 'Press Start 2P', cursive; animation: glowing 1.5s infinite; text-shadow: 0 0 10px #00ffff, 0 0 20px #00ff00, 0 0 30px #0000ff, 0 0 40px #ff00ff;">
                    ¡Bienvenido a PyTrivia! 👋🎮
                </h2>
                <p class="welcome-text" style="color: #66ccff; text-align: center">
                    <em>Con PyTrivia podrás poner a prueba tus conocimientos en diversas temáticas. 🎆</em>
                </p>
                <p class="instruction-text"><strong>Cómo comenzar a Jugar:</strong></p>
                <ul class="welcome-text">
                    <li><span>1. Regístrate.</span></li>
                    <li><span>2. Selecciona una dificultad: Fácil, Media o Alta.</span></li>
                    <li><span>3. Elige una temática para tus preguntas.</span></li>
                    <li><span>4. Responde las preguntas dentro del tiempo límite (si aplica).</span></li>
                    <li><span>5. Acumula puntos y revisa tu posición en el ranking.</span></li>
                </ul>
            </div>
        </body>
        """,
        unsafe_allow_html=True
    )
    # Explicación del parámetro dificultad de forma más divertida
    st.markdown("<h3 style='color:#66ccff;' class='difficulty-levels'>¿Cómo te enfrentarás al desafío? Elige tu nivel de valentía:</h2>", unsafe_allow_html=True)
    st.markdown(
        """
        <ul class="difficulty-levels">
            <li>💤 <b> Modo Siesta (FÁCIL):</b> ¡Tranquilo! Tendrás dos pistas como cojines suaves.</li>
            <li>🔎 <b> Modo Sherlock (MEDIA):</b> Una ayudita como una lupa en la niebla.</li>
            <li>🔥 <b> Modo Fuego (ALTA):</b> ¡Sin red! Te lanzas al abismo sin pistas. ¿Eres un héroe o un kamikaze?</li>
        </ul>
        <p class="welcome-text" style="color: #33cc33"><i>✨¡Buena suerte y diviértete!✨</i></p>
        """,
        unsafe_allow_html=True
    )

    # Menú de navegación
    st.markdown("""<h2 style="text-align: center; font-family: 'Press Start 2P', cursive; animation: glowing 1.5s infinite; text-shadow: 0 0 10px #00ffff, 0 0 20px #00ff00, 0 0 30px #0000ff, 0 0 40px #ff00ff;"> 
                ¡Comencemos!
                </h2>""", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button(":dart: Ir al Juego", key="game"):
            st.switch_page(GAME_PATH)
    with col2:
        if st.button(":memo: Registrate", key="form"):
            st.switch_page(FORM_PATH)
    with col3:
        if st.button(":crossed_swords: Ver Ranking", key="ranking"):
            st.switch_page(RANKING_PATH)
    with col4:
        if st.button(":bar_chart: Info sobre partidas", key="statistics"):
            st.switch_page(STATISTICS_PATH)

if __name__ == "__main__":
    main()