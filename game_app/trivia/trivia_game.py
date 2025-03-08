from ntpath import join
import streamlit as st
import pandas as pd
import pathlib
import random
import sys
import json
from unidecode import unidecode

ROOTDIR = pathlib.Path(__file__).resolve().parents[2]  # Esto va dos niveles hacia arriba, de Datos.py a grupo08
sys.path.append(str(ROOTDIR))
from path import AR_DATA, LAGOS_DATA, CONECTIVIDAD_DATA, CENSO

def question_design(fila_random,atributos,i,tema):
    """
    Diseña y muestra una pregunta en la interfaz de Streamlit basada en el tema y los atributos proporcionados.

    Parameters:
    ----------
    fila_random : pd.Series
        Una fila aleatoria del DataFrame que contiene los datos de la pregunta.
    atributos : list
        Lista de atributos a mostrar en la pregunta. El último elemento de la lista es la respuesta correcta.
    i : int
        Número de la pregunta para mostrar en el encabezado.
    tema : str
        Tema de la pregunta, que determina el formato de presentación de los atributos.

    Returns:
    -------
    None
        Esta función no devuelve ningún valor. Muestra la pregunta en la interfaz de Streamlit.

    Notes:
    -----
    - Si el tema es 'Conectividad a internet', se muestran los atributos específicos excluyendo la lista de conexiones y la respuesta correcta. 
      Las conexiones que están activas se muestran en una lista separada.
    - Para otros temas, se muestran todos los atributos excepto el último, que es la respuesta correcta.
    - La respuesta correcta se muestra siempre al final.
    """
    st.markdown(f'### Pregunta #{i}')
    
    if tema == 'Conectividad a internet':
        # Mostrar los atributos específicos
        for element in atributos[:-1]:  # Excluye la lista de conexiones y la respuesta correcta
            if isinstance(element, list):
                continue
            st.markdown(f'**{element}:** {fila_random[element]}')
        
        # Mostrar las conexiones en una lista
        conexiones = [element for element in atributos[2] if fila_random[element] == 'SI']
        st.markdown(f'**Conexiones:** {", ".join(conexiones)}')

    
    else:    
        for element in atributos[:-1]:
            st.markdown(f'**{element}** {fila_random[element]}')
    
    st.markdown(f'**{atributos[-1]}**')

def mostrar_pregunta_lagos(dificultad_seleccionada,i):
    """
    Muestra una pregunta sobre lagos en la interfaz de Streamlit basada en la dificultad seleccionada.

    Parameters:
    ----------
    dificultad_seleccionada : str
        Nivel de dificultad seleccionado por el usuario ('Facil', 'Medio', 'Dificil').
    i : int
        Número de la pregunta para mostrar en el encabezado.

    Returns:
    -------
    tuple
        Una tupla que contiene la respuesta correcta y un tuple adicional con la fila de datos y los atributos utilizados para la pregunta.

    Notes:
    -----
    - La función carga los datos de los lagos, selecciona una fila aleatoria y mezcla los atributos antes de mostrarlos.
    - En función de la dificultad seleccionada, se proporcionan diferentes niveles de pistas para la respuesta correcta si el atributo es 'Superficie (km²)'.
    - Para otros atributos, se procesa la respuesta correcta y se llama a la función 'ayudas' para proporcionar pistas basadas en la dificultad.
    - La respuesta correcta se muestra al final.
    """
    data = pd.read_csv(LAGOS_DATA)
    atributos = ['Nombre', 'Ubicación', 'Superficie (km²)']
    # obetener una fila random
    fila_random = data.sample().iloc[0]
    # Mezcla aleatoriamente el orden de los atributos
    random.shuffle(atributos)
    # Desempaqueta la lista de atributos en variables individuales
    question_design(fila_random,atributos,i,'Lagos')

    # En Lagos se debe contemplar que la respuesta sea numerica para las ayudas
    if atributos[-1] == 'Superficie (km²)':
        respuesta_correcta = fila_random[atributos[-1]]

        if dificultad_seleccionada == 'Facil':
            st.write(' :blue-background[*Vamos tranqui... Tienes dos pistas*]')
            st.write(f' :blue-background[*es {"par" if respuesta_correcta % 2 == 0 else "impar" }*]')
            st.write(f' :blue-background[*está entre ({int(respuesta_correcta) - 5},{int(respuesta_correcta) + 5})*]')
        elif dificultad_seleccionada == 'Medio':
            st.write(f' :blue-background[*Una ayudita... Está entre ({int(respuesta_correcta) - 5},{int(respuesta_correcta) + 5})*]')
        else:
            st.write(' :blue-background[*¡Me siento con suerte! Sin pistas*]')
        st.write(f' :blue[{int(respuesta_correcta)}]')

    else:
        respuesta_correcta= unidecode(fila_random[atributos[-1]]).upper()
        word_displayed = respuesta_correcta.split(' ')    
        ayudas(dificultad_seleccionada,word_displayed)
        
    

    answer_tuple = (respuesta_correcta, (fila_random, atributos))

    return answer_tuple

def mostrar_pregunta_censo(dificultad_seleccionada,i):
    """
    Muestra una pregunta del juego de preguntas sobre el censo.

    Args:
        dificultad_seleccionada (str): La dificultad seleccionada por el usuario ('Facil', 'Medio', 'Dificil').
        i (int): El número de la pregunta.

    Returns:
        tuple: Una tupla que contiene la respuesta correcta y la información de la pregunta.

    """
    data = pd.read_csv(CENSO)
    data = data.drop(1)
    atributos = ['Total de población', 'Varones Total de población', 'Mujeres Total de población']
    # obetener una fila random
    fila_random = data.sample().iloc[0]
    # Mezcla aleatoriamente el orden de los atributos
    random.shuffle(atributos)
    # Desempaqueta la lista de atributos en variables individuales
    atributos.append('Jurisdicción')
    question_design(fila_random,atributos,i,'Censo')

    respuesta_correcta = fila_random[atributos[-1]]
    word_displayed = respuesta_correcta.split()
    ayudas(dificultad_seleccionada,word_displayed)
    answer_tuple = (respuesta_correcta, (fila_random, atributos))
    return  answer_tuple

    

def mostrar_pregunta_ar(dificultad_seleccionada,i):
    """
    Muestra una pregunta sobre aeropuertos en la interfaz de Streamlit basada en la dificultad seleccionada.

    Parameters:
    ----------
    dificultad_seleccionada : str
        Nivel de dificultad seleccionado por el usuario ('Facil', 'Medio', 'Dificil').
    i : int
        Número de la pregunta para mostrar en el encabezado.

    Returns:
    -------
    tuple
        Una tupla que contiene la respuesta correcta y un tuple adicional con la fila de datos y los atributos utilizados para la pregunta.

    Notes:
    -----
    - La función carga los datos de los aeropuertos, selecciona una fila aleatoria y mezcla los atributos antes de mostrarlos.
    - Utiliza la función `question_design` para mostrar la pregunta en la interfaz.
    - La respuesta correcta se obtiene y se procesa para ser comparada y mostrada correctamente.
    - Se llama a la función 'ayudas' para proporcionar pistas basadas en la dificultad seleccionada.
    """
    data = pd.read_csv(AR_DATA)
    atributos = ['elevation_name','municipality','region_name','name']
    
    # Obtiene una fila aleatoria del DataFrame
    fila_random = data.sample().iloc[0]
    # Mezcla aleatoriamente la lista de atributos
    random.shuffle(atributos)

    # Muestra la pregunta utilizando la función `question_design`
    question_design(fila_random,atributos,i,'Aeropuertos')
    # Obtiene la respuesta correcta (siempre se encuentra al final de la lista de atributos)
    respuesta_correcta = fila_random[atributos[-1]]
   
    # Si la respuesta correcta es numérica, la convierte a cadena para la comparación
    if isinstance(respuesta_correcta, (int, float)):
        respuesta_correcta = str(respuesta_correcta)
    # Si la respuesta correcta no es numérica, la convierte a mayúsculas sin caracteres especiales
    else:
        respuesta_correcta = unidecode(respuesta_correcta).upper()

    word_displayed = respuesta_correcta.split()
    ayudas(dificultad_seleccionada,word_displayed)


    # Crea una tupla con la respuesta correcta y la información de la pregunta
    answer_tuple = (respuesta_correcta, (fila_random, atributos))
    return  answer_tuple



def mostrar_pregunta_conectividad(dificultad_seleccionada,i): 
    """
    Muestra una pregunta sobre conectividad a internet en localidades específicas y proporciona ayudas basadas en la dificultad seleccionada.

    Parameters
    ----------
    dificultad_seleccionada : str
        La dificultad seleccionada para la pregunta ('Facil', 'Medio', 'Dificil').
    i : int
        El número de la pregunta en la secuencia actual.

    Returns
    -------
    tuple
        Una tupla que contiene la respuesta correcta y un conjunto de información sobre la pregunta (fila de datos aleatoria y lista de atributos).

    Notes
    -----
    - La función carga un conjunto de datos de conectividad, filtra localidades con conectividad, y selecciona una fila aleatoria.
    - Los atributos de la pregunta incluyen 'Provincia', 'Partido', 'Localidad', y tipos de conexión presentes.
    - La pregunta se muestra utilizando la función `question_design`.
    - Se proporciona una ayuda basada en la dificultad seleccionada, y la respuesta correcta se procesa para eliminar caracteres especiales.
    """
    data = pd.read_csv(CONECTIVIDAD_DATA)
    # Identificar las columnas de conectividad (columnas 5 a 13)
    conexiones = data.columns[4:13]

    # Filtra el conjunto de datos para incluir solo localidades con conectividad
    data_conectividad = data[data['posee_conectividad'] == 'SI']      
    # Función para obtener tipos de conexión       

    atributos = ['Provincia','Partido','Localidad']
    # Obtiene una fila aleatoria del DataFrame 
    fila_random = data_conectividad.sample().iloc[0]

    # Obtiene los tipos de conexión presentes en la localidad aleatoria
    tipos_conexion = [col for col in conexiones if fila_random[col] == 'SI']
    random.shuffle(atributos)
    # Inserta la lista de tipos de conexión en la lista de atributos
    atributos.insert(2,tipos_conexion)

    # Muestra la pregunta utilizando la función `question_design`
    question_design(fila_random,atributos,i,'Conectividad a internet')
    
    respuesta_correcta= unidecode(fila_random[atributos[-1]]).upper()
    word_displayed = respuesta_correcta.split(' ')

    ayudas(dificultad_seleccionada,word_displayed)
    

    # Crea una tupla con la respuesta correcta y la información de la pregunta
    answer_tuple = (respuesta_correcta, (fila_random, atributos))
    
    return answer_tuple

def ayudas(dificultad_seleccionada,word_displayed):
    """
    Proporciona pistas basadas en la dificultad seleccionada para ayudar al usuario a responder la pregunta.

    Parameters
    ----------
    dificultad_seleccionada : str
        La dificultad seleccionada para la pregunta ('Facil', 'Medio', 'Dificil').
    word_displayed : list of str
        Lista de palabras que componen la respuesta correcta.

    Notes
    -----
    - En dificultad 'Facil', se proporcionan dos pistas: la cantidad de palabras y la primera letra de la primera palabra (o la palabra completa si hay más de una palabra).
    - En dificultad 'Medio', se proporciona una pista: la cantidad de palabras en la respuesta.
    - En dificultad 'Dificil', no se proporcionan pistas.
    - La función utiliza `streamlit` para mostrar las pistas en la interfaz de usuario.
    """
    if dificultad_seleccionada == 'Facil':
        st.write(f' :blue-background[*Vamos tranqui... Tienes dos pistas*]')
        st.write(f' :blue-background[*cantidad de palabras: {len(word_displayed)}*]')
        if len(word_displayed) == 1:
            st.write(f' :blue-background[*cominza por...{word_displayed[0][0]}*]')
        else:
            st.write(f' :blue-background[*comienza por... {word_displayed[0]}*]')
        
    elif dificultad_seleccionada == 'Medio':
        st.write(f' :blue-background[*Una ayudita... Tiene {len(word_displayed)} palabras*]')
    else:
        st.write(' :blue-background[*¡Me siento con suerte! Sin pistas*]')

def pregunta(tematica,dificultad_seleccionada,i):
    """
    Muestra una pregunta basada en la temática y dificultad seleccionadas, y devuelve una tupla con la respuesta correcta y la información de la pregunta.

    Parameters
    ----------
    tematica : str
        La temática de la pregunta ('Lagos', 'Aeropuertos', 'Conectividad a internet').
    dificultad_seleccionada : str
        La dificultad seleccionada para la pregunta ('Facil', 'Medio', 'Dificil').
    i : int
        El número de la pregunta en la secuencia.

    Returns
    -------
    tuple
        Una tupla que contiene la respuesta correcta y la información de la pregunta en el formato (respuesta_correcta, (fila_random, atributos)).

    Notes
    -----
    - La función llama a una función específica de muestra de preguntas en función de la temática seleccionada.
    - Para 'Lagos', llama a `mostrar_pregunta_lagos`.
    - Para 'Aeropuertos', llama a `mostrar_pregunta_ar`.
    - Para 'Conectividad a internet', llama a `mostrar_pregunta_conectividad`.
    """
    if(tematica == 'Lagos'):
        return mostrar_pregunta_lagos(dificultad_seleccionada,i)
    elif(tematica == 'Aeropuertos'):
        return mostrar_pregunta_ar(dificultad_seleccionada,i)
    elif(tematica == 'Conectividad a internet'):
        return mostrar_pregunta_conectividad(dificultad_seleccionada,i)
    elif(tematica == 'Censo'):
        return mostrar_pregunta_censo(dificultad_seleccionada,i)
