# """Importo las librerias a utilizar"""
import streamlit as st
import pandas as pd
import pydeck as pdk
from pathlib import Path
import matplotlib.pyplot as plt
import sys
ROOTDIR = Path(__file__).resolve().parents[2]  # Esto va dos niveles hacia arriba, de Datos.py a grupo08
sys.path.append(str(ROOTDIR))
from path import AR_DATA, LAGOS_DATA

st.title("Conociendo Nuestros Datos 👨‍💻")

# """En estas funciones, se cargan los datos de los archivos CSV de aeropuertos y lagos."""
def cargar_aeropuertos():
    try:
        aeropuertos = pd.read_csv(AR_DATA)
    except FileNotFoundError:
        st.write('Archivo no encontrado.')
        aeropuertos = None
    return aeropuertos
def cargar_lagos():
    try:
        lagos = pd.read_csv(LAGOS_DATA)
    except FileNotFoundError:
        st.write('Archivo no encontrado.')
        lagos=None
    return lagos

# """ 
# Widget 1 Aeropuertos

# Este widget muestra un mapa interactivo de aeropuertos coloreados por elevación.
# La función utiliza PyDeck para visualizar los aeropuertos como puntos en un mapa, con colores que representan su elevación (verde para baja, amarillo para media y rojo para alta).
# También incluye un cuadro de referencia que explica los colores utilizados.
# """
def mapa_coordenadas_aeropuertos (aeropuertos):
    elevacion_colors = {
        'baja': [0, 255, 0],   # Verde para baja elevación
        'media': [255, 255, 0], # Amarillo para media elevación
        'alta': [255, 0, 0]    # Rojo para alta elevación
    }
    aeropuertos['elevation_color'] = aeropuertos['elevation_name'].map(elevacion_colors)
    st.header('🗺️ Mapa de Aeropuertos del Pais por Coordenadas')
    layer = pdk.Layer('ScatterplotLayer',data=aeropuertos,get_position='[longitude_deg, latitude_deg]',get_color='elevation_color',get_radius=5000,pickable=True) 
    view_state = pdk.ViewState(latitude=aeropuertos['latitude_deg'].mean(),longitude=aeropuertos['longitude_deg'].mean(),zoom=3,pitch=0)
    map = pdk.Deck(layers=[layer],initial_view_state=view_state,tooltip={"text": "{name}\nElevación: {elevation_name}"})
    st.markdown("""
    ### Cuadro de Referencia:
    - <span style="color:rgb(0, 255, 0);">🟢 Baja</span>
    - <span style="color:rgb(255, 255, 0);">🟡 Media</span>
    - <span style="color:rgb(255, 0, 0);">🔴 Alta</span>
    """, unsafe_allow_html=True)
    st.pydeck_chart(map)

# """
# Widget 2 Aeropuertos

# Esta widget muestra una tabla con información de los aeropuertos de una provincia seleccionada.
# Primero, definimos una función que filtra los aeropuertos por provincia.
# Luego, definimos otra función donde va a mostrarnos la información de los aeropuertos de la provincia en una tabla,
# incluyendo el nombre, latitud, longitud, región, municipio y enlace de inicio.
# Por último, la última función nos diseña la tabla deseada, con sus respectivas opciones.

# """


def mostrar_aeropuertos_por_provincia(aeropuertos, provincia_seleccionada):
    aeropuertos_provincia = aeropuertos[aeropuertos['region_name'] == provincia_seleccionada]
    return aeropuertos_provincia

def mostrar_info_aeropuertos(aeropuertos,index,contador):
    mostrar_aeropuertos = aeropuertos.iloc[index:index + contador, :]
    aeropuertos_info = mostrar_aeropuertos.loc[:, ['name', 'latitude_deg', 'longitude_deg', 'region_name', 'municipality', 'home_link']]
    aeropuertos_info.columns = ['Nombre', 'Latitud', 'Longitud', 'Nombre de la Región', 'Municipalidad', 'Enlace de Inicio']
    st.dataframe(aeropuertos_info)

def tabla_info_aeropuertos(aeropuertos):
    st.header('🛫 Información de Aeropuertos por Provincia')
    provincias = aeropuertos['region_name'].unique()
    provincia_seleccionada = st.selectbox("Selecciona una provincia:", provincias)
    aeropuertos_provincia = mostrar_aeropuertos_por_provincia(aeropuertos, provincia_seleccionada)
    contador = st.number_input("Cantidad de aeropuertos a mostrar:", min_value=1, max_value=10, value=5)
    num_aeropuertos = len(aeropuertos_provincia)
    total_paginas = num_aeropuertos // contador + (1 if num_aeropuertos % contador != 0 else 0)
    if 'pagina' not in st.session_state:
        st.session_state.pagina = 1
    pagina = st.session_state.pagina
    indice_inicio = (pagina - 1) * contador
    st.write(f"Página {pagina} de {total_paginas}")
    st.write(f"Mostrando {contador} aeropuertos de {indice_inicio + 1} a {min(indice_inicio + contador, num_aeropuertos)} de un total de {num_aeropuertos} aeropuertos.")
    mostrar_info_aeropuertos(aeropuertos_provincia, indice_inicio, contador)
    col1,col2 = st.columns([1,1])
    with col1:
        if st.button("Anterior"):
            if st.session_state.pagina > 1:
                st.session_state.pagina -= 1       
    with col2:
        if st.button("Siguiente"):
            if st.session_state.pagina < total_paginas:
                st.session_state.pagina += 1

# """"
# Widget 3 Aeropuertos

# Muestra un gráfico de barras que representa la cantidad de aeropuertos por provincia.
# Esta función  utiliza la información de los aeropuertos y calcula la cantidad de aeropuertos en cada provincia.
# Luego, crea un gráfico de barras donde el eje x representa las provincias
# y el eje y representa la cantidad de aeropuertos en cada provincia.
    
# """

def grafico_aeropuertos_por_provincia(aeropuertos):
    st.header('📊 Cantidad de Aeropuertos por Provincia')
    aeropuertos_por_provincia = aeropuertos['region_name'].value_counts()
    provincias = aeropuertos_por_provincia.index
    cantidad_aeropuertos = aeropuertos_por_provincia.values
    plt.figure(figsize=(10, 6))
    plt.bar(provincias, cantidad_aeropuertos, color='skyblue')
    plt.xlabel('Provincias')
    plt.ylabel('Cantidad de Aeropuertos')
    plt.title('Cantidad de Aeropuertos por Provincia')
    plt.xticks(rotation=45, ha='right')
    plt.yticks([0,20,40,60,80,100,120,140,160,180,200,250,300])
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    st.pyplot(plt)

# """"
# Widget 1 Lagos
# Este widget muestra un mapa interactivo de los lagos del país.
# Esta función toma el DataFrame de lagos y crea un mapa interactivo utilizando PyDeck.
# Cada lago se representa como un punto en el mapa, con su posición determinada con la latitud y longitud respectivas.

# """
def mapa_coordenadas_lagos(lagos):
    st.header('🗺️ Mapa de Lagos del Pais')
    layer = pdk.Layer('ScatterplotLayer',data=lagos,get_position='[Longitud_GD, Latitud_GD]',get_color='[200, 30, 0, 160]',get_radius=5000,pickable=True)   
    view_state = pdk.ViewState(latitude=lagos['Latitud_GD'].mean(),longitude=lagos['Longitud_GD'].mean(),zoom=3,pitch=0)
    map = pdk.Deck(layers=[layer],initial_view_state=view_state,tooltip={"text": "{Nombre}"})
    st.pydeck_chart(map)

# """"
# Widget 2 Lagos
# Este widget muestra un gráfico de torta que representa la cantidad de lagos por tamaño.
# Esta función utiliza la informacion de los lagos y calcula la cantidad de lagos en cada tamaño de superficie. 
# Luego, crea un gráfico de torta donde cada sector representa un tamaño de superficie y su tamaño relativo representa la proporción de lagos en ese tamaño.

# """
def grafico_torta_lagos(lagos):
    st.header('📈Porcentaje de Cantidad de Lagos por Tamaño')
    sizes = lagos['Sup Tamaño'].value_counts()
    labels=sizes.index
    plt.figure(figsize=(10, 6))
    pie = plt.pie(sizes, labels=labels, autopct="%0.1f %%")
    plt.style.use('dark_background')
    plt.setp(pie[1], color='white')
    plt.axis("equal")
    st.pyplot(plt)

# """
# Widget 3 Lagos

# Este widget muestra un gráfico de barras que representa la cantidad de lagos por provincia.
# Esta función usa la información de lagos y calcula la cantidad de lagos en cada provincia.
# Luego, crea un gráfico de barras donde el eje x representa las provincias y el eje y representa la cantidad de lagos en cada provincia.
# """
def grafico_lagos_por_provincia(lagos):
    st.header('📊Cantidad de Lagos por Provincia')
    lagos_por_provincia = lagos['Ubicación'].value_counts()
    provincias = lagos_por_provincia.index
    cantidad_lagos = lagos_por_provincia.values
    plt.figure(figsize=(10, 6))
    plt.bar(provincias, cantidad_lagos, color='skyblue')
    plt.xlabel('Provincias')
    plt.ylabel('Cantidad de Aeropuertos')
    plt.title('Cantidad de Aeropuertos por Provincia')
    plt.xticks(rotation=45, ha='right')
    plt.yticks([0,2,4,6,8,10,12,14,16,18,20])
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    st.pyplot(plt)

# """
# Streamlit application
# Llamo a las funciones correspondientes para mostrar los widgets en la aplicación de Streamlit.
# """
aeropuertos = cargar_aeropuertos()
lagos = cargar_lagos()
mapa_coordenadas_aeropuertos(aeropuertos)
tabla_info_aeropuertos(aeropuertos)
grafico_aeropuertos_por_provincia(aeropuertos)
mapa_coordenadas_lagos(lagos)
grafico_torta_lagos(lagos)
grafico_lagos_por_provincia(lagos)