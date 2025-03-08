import streamlit as st
from paths import PARTIDAS_DATA, FORM_PATH
import pandas as pd
import random

st.markdown(
    """
    <style>
    .stApp {
        background: rgb(0,0,0);
        background: linear-gradient(180deg, rgba(0,0,0,1) 0%, rgba(17,9,43,1) 40%, rgba(34,18,87,1) 88%, rgba(56,30,144,1) 100%);
        font-family: 'Arial', sans-serif;
        color: #00ffff;
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
        padding: 20px;45
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

st.markdown("""
    <h1 style="text-align: center; font-family: 'Press Start 2P', cursive;animation: glowing 1.5s infinite; text-shadow: 0 0 10px #00ffff, 0 0 20px #00ff00, 0 0 30px #0000ff, 0 0 40px #ff00ff;">Ranking Histórico</h1>
    """, unsafe_allow_html=True)

# Función para cargar datos
def cargar_partidas():
    if PARTIDAS_DATA.exists():
        with open(PARTIDAS_DATA, 'r', encoding='utf-8') as file:
            return pd.read_csv(file)
    else:
        return pd.DataFrame(columns=['username', 'fecha', 'tematica', 'dificultad', 'puntos'])

# Función para mostrar el ranking
def mostrar_ranking(usuario_actual=None):  
    """
    Esta función muestra el ranking histórico de los usuarios en función de los puntos acumulados.
    
    Parámetros:
    usuario_actual (str): El nombre de usuario actual para resaltar su posición en el ranking.
    
    Returns:
    None
    """
    partidas = cargar_partidas()
    
    # Calcular puntos acumulados por usuario
    puntos_acumulados = partidas.groupby('username')['puntos'].sum().reset_index()
    puntos_acumulados = puntos_acumulados.sort_values(by='puntos', ascending=False).reset_index(drop=True)
    # Añadir columna de puesto
    puntos_acumulados['puesto'] = puntos_acumulados.index + 1
    # Tomar los primeros 15
    top_15 = puntos_acumulados.head(15)
    
    st.markdown("""
    <h3 style="color: #00ffff; text-align: center; font-family: 'Press Start 2P', cursive;animation: glowing 1.5s infinite; text-shadow: 0 0 10px #00ffff, 0 0 20px #00ff00, 0 0 30px #0000ff, 0 0 40px #ff00ff;">🏆 Top 15 🏆</h3>
    """, unsafe_allow_html=True)
    # Estilos CSS para los primeros tres puestos
    css_styles = """
    <style>
    .rank-1 {
        font-family: 'Press Start 2P';
        font-weight: bold;
        font-size: 22px;
        color: gold;
    }
    .rank-2 {
        font-family: 'Press Start 2P';
        font-weight: bold;
        font-size: 20px;
        color:silver;
    }
    .rank-3 {
        font-family: 'Press Start 2P';
        font-weight: bold;
        font-size: 18px;
        color:#cd7f32;
    }
    .rank-other {
        font-family: 'Press Start 2P';
        font-size: 14px;
        color:white;
    }
    .user-current {
        background-color:#33cc33;
        font-family: 'Press Start 2P';
        font-size: 16px;
        color: white;
    }
    </style>
    """
    st.markdown(css_styles, unsafe_allow_html=True)

    
    # Mostrar tabla de ranking con colores para los primeros tres puestos
    for idx, row in top_15.iterrows():
        css_class = "rank-other"
        if idx == 0:
            css_class = "rank-1"
        elif idx == 1:
            css_class = "rank-2"
        elif idx == 2:
            css_class = "rank-3"
        elif row['username'] == usuario_actual:
            css_class = "user-current"

        st.markdown(f"<div class='{css_class}'>"
                    f"<strong> {row['puesto']}</strong>° {row['username']} - {row['puntos']} puntos"
                    "</div>", unsafe_allow_html=True)

    # Mostrar resultado del usuario actual
    if usuario_actual:
        if usuario_actual in puntos_acumulados['username'].values:
            st.markdown("""
    <h3 style="text-align: center; font-family: 'Press Start 2P', cursive;animation: glowing 1.5s infinite; text-shadow: 0 0 10px #00ffff, 0 0 20px #00ff00, 0 0 30px #0000ff, 0 0 40px #ff00ff;">Tu posición</h3>
    """, unsafe_allow_html=True)
            usuario_puntaje = puntos_acumulados[puntos_acumulados['username'] == usuario_actual]
            posicion = usuario_puntaje['puesto'].values[0]
            st.markdown(f"""<h3 style=" color: #33cc33; text-align: center; font-family:'Press Start 2P', cursive; font-size: 18px">{usuario_actual}</h3>""", unsafe_allow_html=True)
            st.markdown(f"""<h4 style="text-align: center;font-family:'Press Start 2P', cursive; font-size:14px">Puntaje Acumulado: {usuario_puntaje['puntos'].values[0]}</h3>""", unsafe_allow_html=True)
            st.markdown(f"""<h4 style="text-align: center; font-family: 'Press Start 2P', cursive; font-size: 14px">Posición en el Ranking: {posicion}</h3>""", unsafe_allow_html=True)
        else:
            st.markdown("")
            st.warning(f"El usuario {usuario_actual} no tiene partidas registradas")
            if st.button(":memo: Registrate"):
                st.switch_page(FORM_PATH)

usuario_actual = st.sidebar.text_input("Ingresá tu usuario y mirá tu posición en el Ranking")
    
def main():
    mostrar_ranking(usuario_actual)
    
if __name__ == "__main__":
    main()
    

