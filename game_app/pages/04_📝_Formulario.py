import streamlit as st
import random
import json
import re
from paths import USUARIOS_DATA

st.markdown(    """
    <style>
    .stApp {
        background: rgb(0,0,0);
        background: linear-gradient(180deg, rgba(0,0,0,1) 0%, rgba(17,9,43,1) 40%, rgba(34,18,87,1) 88%, rgba(56,30,144,1) 100%);
    }
    
    </style>
    """,
    unsafe_allow_html=True)

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
    <div>   
        <h2 style="color: #00ffff; text-align: center; font-family: 'Press Start 2P', cursive;">¡Únete a la aventura de conocimiento!</h2>
        <p style="color: #0099ff; text-align: center; font-family: 'Press Start 2P', cursive;">
            🌟 Regístrate para desafiar tu mente con preguntas emocionantes y ganar increíbles puntos. 🌟
        </p>
        <p style="text-align: center; color: #66ccff; font-family: 'Press Start 2P', cursive;">
            Completa el formulario a continuación para comenzar tu viaje.
        </p>
        <p style="color: #33cc33; text-align: center; font-family: 'Press Start 2P', cursive;">
            ¡Estamos emocionados de tenerte a bordo!
        </p>
    </div>
    """, unsafe_allow_html=True)

# Definir la ruta al archivo user_data.csv para almacenar los registros

# Función para obtener los usernames de los usuarios registrados
def get_usernames():
    usernames = []
    if USUARIOS_DATA.is_file():
        with open(USUARIOS_DATA, 'r', encoding='utf-8') as file:
            data = json.load(file)
            usernames = [user['username'] for user in data]
    return usernames

# Función para almacenar un registro en el archivo CSV
def store_record(record):
    list_record = []  # Lista para almacenar los registros existentes

    # Verificar si el archivo JSON existe y leer los registros existentes
    # Verificar si el archivo JSON existe y leer los registros existentes
    if USUARIOS_DATA.is_file():
        with open(USUARIOS_DATA, 'r', encoding='utf-8') as file:
            try:
                list_record = json.load(file)
            except json.JSONDecodeError:
                # Si el archivo está vacío o no es un JSON válido, inicializar una lista vacía
                list_record = []
    # Verificar si el correo electrónico ya existe en los registros existentes
    email_existente = next((r for r in list_record if r['email'] == record['email']), None)

    if email_existente:
        # Actualizar los datos existentes con los nuevos datos
        email_existente.update(record)

        # Escribir todos los registros actualizados en el archivo JSON
        with open(USUARIOS_DATA, 'w', encoding='utf-8') as file:
            json.dump(list_record, file, ensure_ascii=False, indent=4)

        st.success('Datos actualizados exitosamente!')
    else:
        # Agregar un nuevo registro si el correo electrónico no existe
        list_record.append(record)
        with open(USUARIOS_DATA, 'w', encoding='utf-8') as file:
            json.dump(list_record, file, ensure_ascii=False, indent=4)

        st.success('Registro exitoso!')


# Función para validar el nombre de usuario
def validar_username(username):
    return re.match("^[A-Za-z0-9_]*$", username) is not None

# Obtener la lista de usernames existentes
existing_usernames = get_usernames()

# Definir la función para la página de registro
username = st.text_input('Nombre de usuario')
username_in_use = username in existing_usernames

if username_in_use:
    st.warning('El nombre de usuario ya está en uso. Por favor, elige otro.')

full_name = st.text_input('Nombre Completo')
email = st.text_input('Mail')
birth_date = st.date_input('Fecha de nacimiento')
gender = st.selectbox('Género', ['Masculino', 'Femenino', 'Otro'])

if st.button('Registrarse'):
    if username and full_name and email and birth_date and gender:
        if username_in_use:
            st.error('El nombre de usuario ya está en uso. Por favor, elige otro.')
        else:
            if validar_username(username):
                # Crear el registro
                record = {
                    'username': username,
                    'full_name': full_name,
                    'email': email,
                    'birth_date': str(birth_date),
                    'gender': gender
                }
                # Guardar el registro en el archivo
                store_record(record)
                # Almacenar el nombre de usuario en session_state
                st.session_state['username'] = username
            else:
                st.error('El nombre de usuario no debe contener caracteres especiales.')
    else:
        st.warning('Por favor completa todos los campos.')