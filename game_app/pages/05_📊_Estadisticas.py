import pathlib
import sys
import streamlit as st
from streamlit_extras.let_it_rain import rain
import json
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import locale

ROOTDIR = pathlib.Path(__file__).resolve().parents[1]  # Esto va dos niveles hacia arriba, de Datos.py a grupo08
sys.path.append(str(ROOTDIR))
from paths import PARTIDAS_DATA, USUARIOS_DATA
locale.setlocale(locale.LC_TIME, 'Spanish_Spain.1252')

def load_data(partidas_file: str, usuarios_file: str):
    """
    Carga datos JSON desde archivos y devuelve dos listas de diccionarios.

    Args:
    partidas_file (str): La ruta al archivo JSON de partidas.
    usuarios_file (str): La ruta al archivo JSON de usuarios.

    Returns:
    tuple: Una tupla de dos listas de diccionarios (partidas, usuarios).
    """
   
    partidas = pd.read_csv(partidas_file)

    with open(usuarios_file, 'r') as f:
        usuarios = json.load(f)

    return partidas, usuarios



def create_dataframes(partidas: list, usuarios: list):
    """
    Crea DataFrames de pandas a partir de listas de diccionarios.

    Args:
    partidas (list): Lista de diccionarios con datos de partidas.
    usuarios (list): Lista de diccionarios con datos de usuarios.

    Returns:
    tuple: Una tupla de dos DataFrames (df_partidas, df_usuarios).
    """
    df_partidas = pd.DataFrame(partidas)
    df_usuarios = pd.DataFrame(usuarios)
    return df_partidas, df_usuarios

def filter_jugadores(df_partidas: pd.DataFrame, df_usuarios: pd.DataFrame):
    """
    Filtra los usuarios que hayan jugado al menos una vez.

    Args:
    df_partidas (pd.DataFrame): DataFrame con datos de partidas.
    df_usuarios (pd.DataFrame): DataFrame con datos de usuarios.

    Returns:
    pd.DataFrame: DataFrame de usuarios que han jugado al menos una vez.
    """
    usuarios_jugadores = df_partidas['username'].unique()
    df_usuarios_jugadores = df_usuarios[df_usuarios['username'].isin(usuarios_jugadores)]
    return df_usuarios_jugadores




def plot_pie_chart(genero_counts: pd.Series):
    """
    Crea un gráfico de tortas a partir de una serie de pandas y lo muestra en Streamlit.

    Args:
    genero_counts (pd.Series): Serie de pandas con los conteos de género.
    """
    labels = genero_counts.index
    sizes = genero_counts.values

    # Configurar explotado para destacar el segmento más grande
    explode = [0.1 if i == genero_counts.idxmax() else 0 for i in range(len(labels))]

    # Configurar colores más vibrantes
    colors = sns.color_palette('bright')[0:len(labels)]

    # Crear figura y ejes
    fig, ax = plt.subplots(figsize=(8, 8), facecolor='black')  # Fondo negro

    # Graficar el pie chart
    wedges, texts, autotexts = ax.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                                      shadow=True, startangle=90, colors=colors)

    # Personalizar etiquetas y porcentaje automático
    for text in texts:
        text.set_color('white')  # Color de las etiquetas
        text.set_fontsize(12)

    for autotext in autotexts:
        autotext.set_color('white')  # Color del porcentaje automático
        autotext.set_fontsize(12)

    # Ajustes adicionales
    ax.axis('equal')  # Asegura que el gráfico de torta sea un círculo
    plt.title("Distribución de Género de Usuarios que Jugaron al Menos una Vez", fontsize=16, color='gray')

    # Mostrar el gráfico en Streamlit
    st.pyplot(fig)

def plot_pie_chart_media(df_partidas: pd.DataFrame):
    """
    Crea un gráfico de tortas con el porcentaje de partidas que tienen una puntuación superior a la media.

    Args:
    df_partidas (pd.DataFrame): DataFrame con datos de partidas.
    """
    media_puntuacion = df_partidas['puntos'].mean()
    superior_a_media = df_partidas[df_partidas['puntos'] > media_puntuacion].shape[0]
    total_partidas = df_partidas.shape[0]
    porcentaje_superior_a_media = (superior_a_media / total_partidas) * 100
    porcentaje_inferior_a_media = 100 - porcentaje_superior_a_media

    labels = ['Superior a la Media', 'Inferior o Igual a la Media']
    sizes = [porcentaje_superior_a_media, porcentaje_inferior_a_media]
    # Configurar colores más vibrantes
    colors = ['#66b3ff', '#99ff99']

    # Configurar explotado para destacar el primer segmento
    explode = (0.1, 0)

    # Crear figura y ejes
    fig, ax = plt.subplots(figsize=(8, 8), facecolor='black')  # Fondo negro

    # Graficar el pie chart
    wedges, texts, autotexts = ax.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                                      shadow=True, startangle=90, colors=colors)

    # Personalizar etiquetas y porcentaje automático
    for text in texts:
        text.set_color('white')  # Color de las etiquetas
        text.set_fontsize(12)

    for autotext in autotexts:
        autotext.set_color('white')  # Color del porcentaje automático
        autotext.set_fontsize(12)

    # Ajustes adicionales
    ax.axis('equal')  # Asegura que el gráfico de torta sea un círculo
    plt.title("Porcentaje de Partidas con Puntuaciones Superiores a la Media", fontsize=16, color='gray')

    # Mostrar el gráfico en Streamlit
    st.pyplot(fig)



def plot_bar_chart_dias(df_partidas: pd.DataFrame):
    """
    Crea un gráfico de barras que muestra la cantidad de partidas realizadas para cada día de la semana.

    Args:
    df_partidas (pd.DataFrame): DataFrame con datos de partidas.
    """
    df_partidas['fecha'] = pd.to_datetime(df_partidas['fecha'])
    df_partidas['dia_semana'] = df_partidas['fecha'].dt.strftime('%A')
    dias_counts = df_partidas['fecha'].dt.strftime('%A').value_counts().reindex([
    'lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo'])
    # Crear un mapeo de colores personalizado para cada día de la semana
    colors = ['#FF0000', '#FF4500', '#FFA500', '#FFFF00', '#32CD32', '#00BFFF', '#8A2BE2']

    # Configurar el fondo del gráfico directamente desde Streamlit
    st.set_option('deprecation.showPyplotGlobalUse', False)  # Evitar un warning de Streamlit
    fig, ax = plt.subplots(figsize=(16, 9))
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')  # Fondo del gráfico en negro

    # Graficar el gráfico de barras con colores personalizados
    dias_counts.plot(kind='bar', ax=ax, color=colors)
    
    # Personalizar etiquetas y título
    plt.xlabel("Día de la Semana", color='white')  # Etiqueta del eje x en blanco
    plt.ylabel("Cantidad de Partidas", color='white')  # Etiqueta del eje y en blanco
    plt.title("Cantidad de Partidas por Día de la Semana", color='white')  # Título en blanco

    # Personalizar colores de las etiquetas del eje y ticks
    ax.tick_params(axis='x', colors='white',rotation=0)  # Etiquetas del eje x en blanco
    ax.tick_params(axis='y', colors='white')  # Etiquetas del eje y en blanco

    # Configurar color del título
    ax.title.set_color('white')

    ax.grid(axis='y', linestyle='--', alpha=0.7)  # Rejillas horizontales
    # Mostrar el gráfico en Streamlit
    st.pyplot(fig)

 



# Función para calcular el promedio de puntos acumulados mensuales
def plot_bar_chart_promedio_preguntas(df_partidas: pd.DataFrame, fecha_inicio: pd.Timestamp, fecha_fin: pd.Timestamp):
    """
    Crea un gráfico de barras que muestra el promedio de preguntas acertadas mensuales dentro de un rango de fechas.

    Args:
    df_partidas (pd.DataFrame): DataFrame con datos de partidas.
    fecha_inicio (pd.Timestamp): Fecha de inicio del rango.
    fecha_fin (pd.Timestamp): Fecha de fin del rango.
    """
    df_partidas['fecha'] = pd.to_datetime(df_partidas['fecha'])
    mask = (df_partidas['fecha'] >= fecha_inicio) & (df_partidas['fecha'] <= fecha_fin)
    df_partidas_filtrado = df_partidas.loc[mask]
    # Verificar si el DataFrame filtrado está vacío
    if df_partidas_filtrado.empty:
        st.warning("No hay datos disponibles para el rango de fechas seleccionado.")
        return
    
    df_partidas_filtrado['mes'] = df_partidas_filtrado['fecha'].dt.strftime('%Y-%m')
    promedio_preguntas = df_partidas_filtrado.groupby('mes')['puntos'].mean()
   
    # Verificar si el resultado del agrupamiento está vacío
    if promedio_preguntas.empty:
        st.warning("No hay datos disponibles después del agrupamiento.")
        return
    
    # Configurar el fondo del gráfico directamente desde Streamlit
    st.set_option('deprecation.showPyplotGlobalUse', False)  # Evitar un warning de Streamlit
    fig, ax = plt.subplots(figsize=(10, 9))
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')  # Fondo del gráfico en negro
    plt.plot(promedio_preguntas.index, promedio_preguntas.values, marker='o', linestyle='--', color='b')
    for i, txt in enumerate(promedio_preguntas.values):
        ax.annotate(f'{txt:.2f}', (promedio_preguntas.index[i], promedio_preguntas.values[i]),
                    textcoords="offset points", xytext=(0,5), ha='center', color='r', fontsize=15)
    plt.xlabel("Mes", color= 'white')
    plt.ylabel("Promedio de Preguntas Acertadas", color='white')
    plt.title("Promedio de Preguntas Acertadas Mensuales", color='white')
    plt.xticks(rotation=45)  # Rotar las etiquetas del eje x si es necesario

    ax.tick_params(axis='x', colors='white')  # Etiquetas del eje x en blanco
    ax.tick_params(axis='y', colors='white')  # Etiquetas del eje y en blanco

    # Configurar color del título
    ax.title.set_color('white')
    ax.grid(axis='y', linestyle='--', alpha=0.7)  # Rejillas horizontales
    ax.grid(axis='x', linestyle='--', alpha=0.7)  # Rejillas verticales

    # Mostrar el gráfico en Streamlit
    st.pyplot(fig)



def plot_top_10_usuarios(df_partidas: pd.DataFrame, fecha_inicio: pd.Timestamp, fecha_fin: pd.Timestamp):
    """
    Muestra el Top 10 de usuarios con mayor cantidad de puntos acumulados entre un rango de fechas.

    Args:
    df_partidas (pd.DataFrame): DataFrame con datos de partidas.
    fecha_inicio (pd.Timestamp): Fecha de inicio del rango.
    fecha_fin (pd.Timestamp): Fecha de fin del rango.
    """
    # Filtrar datos por fecha
    df_partidas['fecha'] = pd.to_datetime(df_partidas['fecha'])
    mask = (df_partidas['fecha'] >= fecha_inicio) & (df_partidas['fecha'] <= fecha_fin)
    df_partidas_filtrado = df_partidas.loc[mask]

    # Verificar si no hay datos después del filtrado
    if df_partidas_filtrado.empty:
        st.warning("No hay datos disponibles para el rango de fechas seleccionado.")
        return
    
    # Agrupar por usuario y sumar los puntos acumulados
    puntos_acumulados = df_partidas_filtrado.groupby('username')['puntos'].sum().sort_values(ascending=False).head(10)

    # Verificar si no hay datos después del agrupamiento
    if puntos_acumulados.empty:
        st.warning("No hay datos disponibles después del agrupamiento.")
        return

    # Mostrar los datos en formato de tabla
    st.write("Top 10 de Usuarios con Mayor Cantidad de Puntos Acumulados")
    st.table(puntos_acumulados.reset_index().rename(columns={'puntos': 'Puntos Acumulados'}))

def ordenar_por_dificultad(df_partidas: pd.DataFrame):
    """
    Ordena el DataFrame de partidas por dificultad, ubicando primero el dataset que tiene mayor número de errores en las respuestas.

    Args:
    df_partidas (pd.DataFrame): DataFrame con datos de partidas.

    Returns:
    pd.DataFrame: DataFrame ordenado por dificultad.
    """
    errores_por_dificultad = df_partidas[df_partidas['puntos'] == 0].groupby('dificultad').size().sort_values(ascending=False)
    df_partidas['errores'] = df_partidas['dificultad'].map(errores_por_dificultad)
    df_partidas_ordenado = df_partidas.sort_values(by='errores', ascending=False).drop(columns=['errores'])
    return df_partidas_ordenado

def plot_line_chart_usuarios(df_partidas: pd.DataFrame, usuario1: str, usuario2: str):
    """
    Crea un gráfico de líneas que muestra la evolución del puntaje a lo largo del tiempo para dos usuarios seleccionados.

    Args:
    df_partidas (pd.DataFrame): DataFrame con datos de partidas.
    usuario1 (str): Nombre del primer usuario.
    usuario2 (str): Nombre del segundo usuario.
    """
    df_partidas['fecha'] = pd.to_datetime(df_partidas['fecha'])
    df_usuario1 = df_partidas[df_partidas['username'] == usuario1].set_index('fecha').resample('D').sum()
    df_usuario2 = df_partidas[df_partidas['username'] == usuario2].set_index('fecha').resample('D').sum()

    fig, ax = plt.subplots(figsize=(12,6))
    fig.patch.set_facecolor('black')  # Fondo del gráfico en negro
    ax.set_facecolor('black')  

    ax.plot(df_usuario1.index, df_usuario1['puntos'], label=usuario1, linewidth=2, marker='o', markersize=8, color='deepskyblue')
    ax.plot(df_usuario2.index, df_usuario2['puntos'], label=usuario2, linewidth=2, marker='s', markersize=8, color='orange')

    plt.xlabel("Fecha", fontsize=12, color='white')
    plt.ylabel("Puntos", fontsize=12, color='white')
    plt.title("Evolución del Puntaje a lo Largo del Tiempo", fontsize=16, color='white')
    plt.legend()

    ax.grid(True, linestyle='--', alpha=0.6)

    fig.autofmt_xdate()  # Formato automático de las fechas en el eje x

    # Personalizar los ticks del eje x y y
    ax.tick_params(axis='x', colors='white', labelsize=10)
    ax.tick_params(axis='y', colors='white', labelsize=10)

    # Personalizar la leyenda
    ax.legend(loc='upper left', fontsize=10)


    ax.legend()

    ax.grid(True, linestyle='--', alpha=0.6)

    fig.autofmt_xdate()
    
    st.pyplot(fig)

def listar_tematica_por_genero(df_partidas: pd.DataFrame, df_usuarios: pd.DataFrame):
    """
    Lista para cada género cuál es la temática en la cual demuestra mayor conocimiento.

    Args:
    df_partidas (pd.DataFrame): DataFrame con datos de partidas.
    df_usuarios (pd.DataFrame): DataFrame con datos de usuarios.
    """
    df_merged = pd.merge(df_partidas, df_usuarios, on='username')
    tematica_por_genero = df_merged[df_merged['puntos'] > 0].groupby(['gender', 'tematica']).size().reset_index(name='counts')
    max_tematica_por_genero = tematica_por_genero.loc[tematica_por_genero.groupby('gender')['counts'].idxmax()]
    max_tematica_por_genero.rename(columns={'gender': 'Género', 'counts': 'Cantidad'}, inplace=True)

    st.write("Temática con Mayor Conocimiento por Género")
    st.write(max_tematica_por_genero)

def listar_dificultad_puntaje(df_partidas: pd.DataFrame):
    """
    Lista cada dificultad de juego junto con el puntaje promedio obtenido en cada una y la cantidad de veces que fue elegida.

    Args:
    df_partidas (pd.DataFrame): DataFrame con datos de partidas.
    """
    dificultad_puntaje = df_partidas.groupby('dificultad').agg({'puntos': ['mean', 'size']}).reset_index()
    dificultad_puntaje.columns = ['dificultad', 'puntaje_promedio', 'cantidad_veces']

    st.write("Puntaje Promedio y Cantidad de Veces Elegida por Dificultad")
    st.write(dificultad_puntaje)

def listar_usuarios_racha(df_partidas: pd.DataFrame):
    """
    Lista los usuarios que registran una partida con un puntaje mayor a cero en todos los días durante los últimos 7 días.

    Args:
    df_partidas (pd.DataFrame): DataFrame con datos de partidas.
    """
    # Convertir la columna de fecha a datetime
    df_partidas['fecha'] = pd.to_datetime(df_partidas['fecha'])
    
    # Obtener el rango de los últimos 7 días
    hoy = pd.Timestamp('today').normalize()  # Obtener la fecha de hoy y normalizar a medianoche
    ultimos_7_dias = pd.date_range(end=hoy, periods=7)
    
    # Filtrar las partidas de los últimos 7 días
    df_ultimos_7_dias = df_partidas[df_partidas['fecha'].isin(ultimos_7_dias)]
    
    # Verificar que hay datos para los últimos 7 días
    if df_ultimos_7_dias.empty:
        st.write("No hay partidas registradas en los últimos 7 días.")
        return
    
    # Filtrar usuarios con puntajes mayores a cero y contar por usuario y día
    df_ultimos_7_dias = df_ultimos_7_dias[df_ultimos_7_dias['puntos'] > 0]
    usuarios_dias = df_ultimos_7_dias.groupby(['username', 'fecha']).size().reset_index(name='count')
    
    # Contar los días con partidas por usuario
    usuarios_racha = usuarios_dias.groupby('username').size()
    
    # Filtrar usuarios que tengan registros en los 7 días
    usuarios_racha = usuarios_racha[usuarios_racha >= 7]

    # Mostrar el resultado
    st.write("Usuarios en Racha (puntaje > 0 en los últimos 7 días)")
    if usuarios_racha.empty:
        st.write("No hay usuarios en racha en los últimos 7 días.")
    else:
        st.write(usuarios_racha)

def rainy():
    rain(
        emoji="⭐",
        font_size=32,
        falling_speed=2,
        animation_length="2s",
    )

def main():


    """
    Función principal para ejecutar la aplicación de Streamlit.
    Carga los datos, filtra los usuarios que han jugado, y muestra gráficos y listados.
    """
    rainy()
    st.title("👩👨 Análisis de Usuarios por Género")

    partidas, usuarios = load_data(PARTIDAS_DATA, USUARIOS_DATA)
    df_partidas, df_usuarios = create_dataframes(partidas, usuarios)
    df_usuarios_jugadores = filter_jugadores(df_partidas, df_usuarios)

    genero_counts = df_usuarios_jugadores['gender'].value_counts()
    plot_pie_chart(genero_counts)

    plot_pie_chart_media(df_partidas)

    st.header(" 📌Cantidad de Partidas por Día de la Semana")
    plot_bar_chart_dias(df_partidas)


    
    st.header("🔴Promedio de Preguntas Acertadas Mensuales")
    fecha_inicio_promedio = st.date_input("Fecha de Inicio", key="fecha_inicio_1")
    fecha_fin_promedio = st.date_input("Fecha de Fin", key="fecha_fin_1")
    if fecha_inicio_promedio <= fecha_fin_promedio:
        plot_bar_chart_promedio_preguntas(df_partidas, pd.Timestamp(fecha_inicio_promedio), pd.Timestamp(fecha_fin_promedio))
    else:
        st.error("La Fecha de Inicio debe ser anterior a la Fecha de Fin")


    st.header("🟣Top 10 de Usuarios con Mayor Cantidad de Puntos Acumulados")
    fecha_inicio_top = st.date_input("Fecha de Inicio", key="fecha_inicio_2")
    fecha_fin_top = st.date_input("Fecha de Fin", key="fecha_fin_2")
    if fecha_inicio_top <= fecha_fin_top:
        plot_top_10_usuarios(df_partidas, pd.Timestamp(fecha_inicio_top), pd.Timestamp(fecha_fin_top))
    else:
        st.error("La Fecha de Inicio debe ser anterior a la Fecha de Fin")

    st.header("🎈Partidas Ordenadas por Dificultad🎈")
    df_partidas_ordenado = ordenar_por_dificultad(df_partidas)
    st.write(df_partidas_ordenado)

    st.header("🏈Evolución de Puntaje para Dos Usuarios")
    usuario1 = st.selectbox("Selecciona el primer usuario", df_partidas['username'].unique())
    usuario2 = st.selectbox("Selecciona el segundo usuario", df_partidas['username'].unique())
    plot_line_chart_usuarios(df_partidas, usuario1, usuario2)

    st.header("🧸Temática con Mayor Conocimiento por Género")
    listar_tematica_por_genero(df_partidas, df_usuarios)

    st.header("🤩Puntaje Promedio y Cantidad de Veces Elegida por Dificultad")
    listar_dificultad_puntaje(df_partidas)

    st.header("🔥Usuarios en Racha🔥")
    listar_usuarios_racha(df_partidas)

    st.header("🎇Detalles de Usuarios🎇")
    df_usuarios_jugadores.rename(columns={'username': 'Usuario', 'full_name':'Nombre Completo','birth_date':'Fecha de Nacimiento', 'gender':'Género'}, inplace=True)
    st.write(df_usuarios_jugadores)


if __name__ == "__main__":
    main()





