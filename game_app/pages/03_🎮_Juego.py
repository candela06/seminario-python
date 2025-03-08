import random
import streamlit as st
import pandas as pd
import pathlib
import json
import csv

from unidecode import unidecode
import trivia
import datetime
import sys

import trivia.pytrivia
import trivia.trivia_game
from pages.Ranking import mostrar_ranking

ROOTDIR = pathlib.Path(__file__).resolve().parents[2]  # Esto va dos niveles hacia arriba, de Datos.py a grupo08
sys.path.append(str(ROOTDIR))
from path import AR_DATA, LAGOS_DATA, CONECTIVIDAD_DATA, CENSO




# ruta para el archivo de usuarios registrados
path = pathlib.Path('..','game_app','user_data','user_data.json')
# ruta para el archivo de partidas realizadas
PARTIDAS_DATA = pathlib.Path('.','user_data','partidas.csv')


tematicas = ['Aeropuertos','Lagos','Conectividad','Censo 2022']
dificultad = ['Facil','Medio','Dificil']

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
# Inicializacion del estado del juego
# Esto asegura que el estado del juego se inicialice solo una vez, almacenando información relevante sobre el estado actual del juego.
if "game_state" not in st.session_state:
    st.session_state["game_state"] = {
        "state": "NO_CREADO",
        "quiz_state":False,
        "user": None,
        "user_answers_list": [],
        "correct_answers_list": [],
        "preguntas": [],
        "saved": False, 
    }

# Selección de Usuario y Configuración del Juego

# si es una nueva partida
if st.session_state.game_state["state"] == "NO_CREADO":
    

# Crear el mensaje de bienvenida
    st.markdown(
    """
    <body class="star">
        <div>
            <h2 style="text-align: center; color: #00ffff;font-family: 'Press Start 2P', cursive;animation: glowing 1.5s infinite; text-shadow: 0 0 10px #00ffff, 0 0 20px #00ff00, 0 0 30px #0000ff, 0 0 40px #ff00ff;">¡Bienvenido a Pytrivia!</h2>
            <p class="welcome-text" style="color: #00ffff; text-align: center"><em>Estamos encantados de tenerte aquí. Prepárate para una experiencia emocionante y desafiante.</em></p>
            <p class="instruction-text"><strong>Instrucciones:</strong></p>
            <ul class="welcome-text">
                <li>Elige la dificultad y la temática del juego.</li>
                <li>Responde a las preguntas lo mejor que puedas.</li>
                <li>Gana puntos y compite con otros jugadores.</li>
            </ul>
            <p class="welcome-text" style="color: #00ffff"><i>✨¡Buena suerte y diviértete!✨</i></p>
        </div>
    </body>
    """,
    unsafe_allow_html=True
)    
  
    
    
    with path.open(mode='r') as f:
        data = json.load(f)
    usuarios = [usuario['username'] for usuario in data]

# sección para seleccionar usuario, tematica y dificultad
    usuario = st.selectbox("Usuario",usuarios,index=None,placeholder="Seleccione usuario")
    if usuario != None:
        tema = st.selectbox("Temática",["Lagos","Conectividad a internet","Aeropuertos","Censo"],index=None,placeholder="Seleccione tematica")
        if tema != None:
            dificultad = st.selectbox("Difucultad",["Facil","Medio","Dificil"],index=None,placeholder="Seleccione dificultad")   
            if dificultad != None:
                jugar = st.button("Jugar")
                if jugar:
                    # se instancia un objeto Jugador, será quién jugará una partida
                    jugador = trivia.pytrivia.Jugador(tema,usuario,datetime.datetime.now(),dificultad,0)
                    st.session_state.game_state["state"] = "NUEVO"
                    # se guardar el jugador en session_state para no perderlo al recargar la pagina
                    st.session_state.game_state["user"] = jugador
                    st.experimental_rerun()
    else: 
        st.page_link("pages/04_📝_Formulario.py", label="Registrate", icon="📝")


# Manejo de estado del Juego  

if st.session_state.game_state["state"] == "NUEVO":
    st.markdown(f"""
    <div>
         <h2 style="text-align: center; color: #00ffff;font-family: 'Press Start 2P', cursive;animation: glowing 1.5s infinite; text-shadow: 0 0 10px #00ffff, 0 0 20px #00ff00, 0 0 30px #0000ff, 0 0 40px #ff00ff;">¡A jugar, {st.session_state.game_state['user'].get_usuario()}!</h2>
        <p></p>
    </div>
    """,
    unsafe_allow_html=True)
   # st.write(f"¡Bienvenido al juego {st.session_state.game_state['user'].get_usuario()}!")
    st.session_state.game_state['state'] ='EN_PROCESO'

# comienza el juego de preguntas y respuestas
if  st.session_state.game_state["state"] == "EN_PROCESO":   
    with st.form('Preguntas'):
        aux =[] # lista auxiliar para guardar las respuestas del usuario al recargar la pagina
    
    # inicio del juego      
        for i in range(1,6):
            # False: se genera una pregunta, True: evita que la respuesta correcta cambie al recargar la pagina
            if not st.session_state.game_state['quiz_state']:
                # realiza la pregunta y devuelve la respuesta esperada
                correct_answer = trivia.trivia_game.pregunta(st.session_state.game_state['user'].get_tematica(), st.session_state.game_state['user'].get_dificultad(), i)
                # agrego la respuesta correcta de la pregunta en la lista de la session_state
                st.session_state.game_state['correct_answers_list'].append(correct_answer[0])
                st.session_state.game_state['preguntas'].append(correct_answer[1])
                # a la espera de una respuesta y agrego un input vacío en la lista auxiliar
            aux.append(st.text_input("Respuesta:", key=f"respuesta_usuario_{i}").upper())
        st.session_state.game_state['quiz_state'] = True
        rta = st.form_submit_button('Enviar respuestas') # recarga la pagina y la lista auxiliar levanta las respuestas del usuario

        if rta:
            st.session_state.game_state['user_answers_list'] = aux 
            # calculo el puntaje y lo seteo al jugador
            score = st.session_state.game_state['user'].calcular_puntos(st.session_state.game_state['user_answers_list'], st.session_state.game_state['correct_answers_list'])
            st.session_state.game_state['user'].set_puntos(score)
            # cambio el estado del juego
            st.session_state.game_state['state'] = 'MOSTRAR_PUNTAJE'
            st.experimental_rerun()



# siguiente estado        
if st.session_state.game_state["state"] == "MOSTRAR_PUNTAJE":
    st.markdown("""
        
        <h2 style="color: #FFC300; text-align: center;">⭐ ¡Partida finalizada! ⭐</h2>
        <p style="text-align: center;"> <i>Guardá tu partida para poder ver tu posición en el ranking</i></p>
    """, unsafe_allow_html=True)
    # se muestran las preguntas con sus respuestas, si acertó o no
    i = 0
    for elemento in st.session_state.game_state["preguntas"]:
        i += 1
        trivia.trivia_game.question_design(elemento[0], elemento[1], i,st.session_state.game_state['user'].get_tematica())
        
        # limpio las respuestas para evitar tildes, numeros, espacios y diferencia entre mayusculas y minusculas
        respuesta_correcta = unidecode(str(elemento[0][elemento[1][-1]]).strip().upper())
        respuesta_usuario = unidecode(str(st.session_state.game_state['user_answers_list'][i-1]).strip().upper())

        if respuesta_correcta == respuesta_usuario:
            st.success(f'Tu respuesta: {st.session_state.game_state["user_answers_list"][i-1]}')
            st.success(f'¡Bien! La respuesta era {st.session_state.game_state["correct_answers_list"][i-1]}')
        else:
            st.error(f'Tu respuesta: {st.session_state.game_state["user_answers_list"][i-1]}')
            st.error(f'No... Te equivocaste 😔. La respuesta era: {st.session_state.game_state["correct_answers_list"][i-1]}')
    
    # enseña los puntos en pantalla  

    #Mostrar ranking histórico y puesto del usuario actual
    mostrar_ranking(st.session_state.game_state['user'].get_usuario())    
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button('Guardar partida', disabled=st.session_state.game_state.get('saved', False)):
            # se guarda la partida
            st.session_state.game_state['saved'] = True
            # Se crea un DataFrame de Pandas a partir del diccionario del estado del juego del usuario en la sesión de Streamlit
            jugador_df = pd.DataFrame([st.session_state.game_state['user'].to_dict()])
            # Se verifica si existe el archivo PARTIDAS_DATA
            if PARTIDAS_DATA.exists():
                try:
                    # Se intenta leer el archivo como un DataFrame de Pandas
                    data = pd.read_csv(PARTIDAS_DATA)
                    # Si el DataFrame leído no está vacío
                    if not data.empty:
                        # Se concatena el DataFrame del jugador con el DataFrame existente, ignorando el índice original
                        updated = pd.concat([data, jugador_df], ignore_index=True)
                    else:
                        # Si el DataFrame leído está vacío, se utiliza solo el DataFrame del jugador
                        updated = jugador_df
                # Se maneja la excepción EmptyDataError (archivo vacío o sin datos)
                except pd.errors.EmptyDataError:
                    # Se utiliza solo el DataFrame del jugador en este caso también
                    updated = jugador_df
            else:
                # Si el archivo PARTIDAS_DATA no existe, se utiliza solo el DataFrame del jugador
                updated = jugador_df
            # Se guarda el DataFrame actualizado en el archivo PARTIDAS_DATA sin índice
            updated.to_csv(PARTIDAS_DATA, index=False)
            st.experimental_rerun()
    

    with col2:
        if st.button("Volver a jugar"):
            st.session_state.game_state["state"] = "NUEVO"
            st.session_state.game_state["saved"] = False
            st.session_state.game_state['quiz_state'] = False
            st.session_state.game_state['user_answers_list'] = []
            st.session_state.game_state['correct_answers_list'] = []
            st.session_state.game_state['preguntas'] = []
            st.experimental_rerun()

    with col3:
        if st.button("Cerrar Sesión"):
            del st.session_state['game_state']
            st.markdown('<meta http-equiv="refresh" content="0;url=game_app/pages/03_🎮_Juego.py">', unsafe_allow_html=True)
            st.experimental_rerun()

    


            





