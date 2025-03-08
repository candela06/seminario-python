import pathlib
import csv

def read_csv_file(file_path):
    """Lee un archivo CSV y devuelve un objeto lector CSV y el archivo abierto."""
    file = file_path.open(mode='r', encoding='utf-8')
    reader = csv.reader(file)
    header = next(reader)  # Leer la primera fila que contiene los encabezados
    return reader, file

def process_airports(original_airports, modified_airports, ar_data):
    """
    Procesa los datos de los aeropuertos y escribe un nuevo archivo CSV con datos modificados.

    Parameters:
        original_airports (pathlib.Path): Ruta al archivo CSV original de aeropuertos.
        modified_airports (pathlib.Path): Ruta al archivo CSV modificado de aeropuertos.
        ar_data (csv.reader): Objeto lector CSV que contiene datos de provincias en Argentina.
    """
    # Indices de las columnas en los archivos CSV
    elevation_ft_index = 6
    municipality_index = 13
    city_index = 0
    admin_name_index = 5

    # Crear un diccionario para mapear ciudades a nombres de provincias
    city_to_province = {row[city_index]: row[admin_name_index] for row in ar_data}

    # Procesar los aeropuertos
    with original_airports.open(mode='r', encoding='utf-8') as original_file, \
         modified_airports.open(mode='w', encoding='utf-8', newline ='') as modified_file:
        
        reader = csv.reader(original_file)
        writer = csv.writer(modified_file)

        # Leer el encabezado y escribirlo en el nuevo archivo
        header = next(reader)
        header.extend(['elevation_name', 'prov_name'])
        writer.writerow(header)

        # Procesar cada fila
        for row in reader:
            # Procesar los datos de elevación
            try:
                elevation_ft = int(row[elevation_ft_index])
            except ValueError:
                elevation_ft = 0

            if elevation_ft <= 131:
                elevation_name = 'baja'
            elif elevation_ft <= 903:
                elevation_name = 'media'
            else:
                elevation_name = 'alta'

            # Obtener el nombre de la provincia correspondiente a la ciudad
            city_name = row[municipality_index]
            province_name = city_to_province.get(city_name, '')

            # Agregar los datos procesados a la fila
            row.extend([elevation_name, province_name])

            # Escribir la fila en el nuevo archivo
            writer.writerow(row)

# Definir rutas de archivos
original_airports_file = pathlib.Path('./data/ar-airports.csv')
modified_airports_file = pathlib.Path('./data_modify/ar-airports.csv')
ar_data_file = pathlib.Path('./data/ar.csv')

# Leer datos de ar.csv
ar_data_reader, file = read_csv_file(ar_data_file)

# Procesar aeropuertos
process_airports(original_airports_file, modified_airports_file, ar_data_reader)

file.close()
