
import csv
import pathlib 

SUPERFICIE = 2
COORDENADAS = 5


original_file = pathlib.Path('.','data','lagos_arg.csv')
modified_file = pathlib.Path('.','data_modify','lagos_arg.csv')

# Función para convertir GMS a GD
def turn_to_gd(coordinates_gms):
    """
    Convierte coordenadas de Grados, Minutos y Segundos (GMS) a Grados Decimales (GD).
    
    Args:
        coordinates_gms (str): Coordenadas en formato GMS, e.g., '34°35'22"S'.
    
    Returns:
        float: Coordenadas en formato GD.
    """
    components = coordinates_gms.replace('°', ' ').replace("'", ' ').replace('"', ' ').split()

    degrees = float(components[0])
    minutes = float(components[1]) if len(components) > 1 else 0
    #se extraen los segundos excluyendo la dirección 'S' y 'O' para convertirlo en flotante
    seconds = float(components[2]) if len(components) > 2 else 0 
    direction = components[3] if len(components) > 3 else ''
    
    gd = degrees + (minutes / 60) + (seconds / 3600)
    if direction in ['S', 'O']:
        gd *= -1  # Convertir a negativo para el hemisferio sur y oeste
    return gd


# Lista para almacenar los datos procesados
processed_data = []

# Leer el archivo CSV original
with original_file.open('r', encoding='utf-8') as orig:
    """
    Lee el archivo CSV original y procesa cada línea para convertir las coordenadas GMS a GD
    y determinar el tamaño del lago basado en su superficie.
    """
    reader = csv.reader(orig)
    header = next(reader)  # Leer la primera fila como cabecera
    header[COORDENADAS] = 'Coordenadas (GMS)'
    header.extend(['Latitud_GD', 'Longitud_GD', 'Sup Tamaño']) # Añadir los nuevos campos a la cabecera
    header.extend(['Sup Tamaño'])  # Añadir los nuevos campos a la cabecera
    for line in reader:
        surface = float(line[SUPERFICIE]) 
        # Determinar el tamaño del lago según los criterios
        if surface <= 17:
            tamaño = 'chico'
        elif 17 < surface <= 59:
            tamaño = 'medio'
        else:
            tamaño = 'grande'

        coordinates_gms = line[COORDENADAS] 
         # Convertir coordenadas de GMS a GD y reemplazar en la línea actual
        latitud_gd = turn_to_gd(coordinates_gms.split()[0])
        longitud_gd = turn_to_gd(coordinates_gms.split()[1])

        line.insert(COORDENADAS + 1, '{:.6f}'.format(latitud_gd))  # Insertar latitud GD
        line.insert(COORDENADAS + 2, '{:.6f}'.format(longitud_gd))

        # Agregar los datos procesados a la lista
        line.append(tamaño)
        processed_data.append(line)

# escribir los datos procesados en el archivo nuevo
with open(modified_file, 'w', newline='', encoding='utf-8') as new_file:
    """
    Escribe los datos procesados en un nuevo archivo CSV.
    """
    writer = csv.writer(new_file)
    writer.writerow(header)  # escribe la cabecera
    writer.writerows(processed_data)  # escribe los datos procesados
