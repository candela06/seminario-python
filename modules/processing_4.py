# 1- Para el dataset de Población del censo 2022 (D)(c2022_tp_c_resumen_adaptado.csv) reemplazar los valores "///" y "-" por cero (0) en los campos que corresponda.

# 2- Además agregar un nuevo campo que tenga el porcentaje de población en situación de calle. Tener en cuenta el total general (NO tener en cuenta los totales por sexo registrado al nacer).
import pathlib
import csv
path = pathlib.Path('data','c2022_tp_c_resumen_adaptado.csv')
with open(path, 'r') as file:
    """
    Toma el archivo CSV existente que contiene datos sobre población y personas en situación de calle.
    Calcula el porcentaje de personas en situación de calle respecto a la población total y añade esta información
    como una nueva columna al archivo CSV original.
    
    """
    lines = list(csv.reader(file))
    headers = lines[0]
    headers.append('Porcentaje de población en situación de calle')
    modified_lines = [list(map(lambda item: '0' if item in ["///", "-"] else item, line)) for line in lines]
    data_lines = modified_lines[1:]
    calculate_percentage = lambda line: f"{round((int(line[4]) / int(line[1])) * 100, 3)}%"   
    for line in data_lines:
        line.append(calculate_percentage(line))
with open('data_modify/c2022_tp_c_resumen_adaptado.csv', 'w', newline='') as modified_file:
    """
    Escribe encabezados y líneas de datos modificadas del archivo.
    """
    writer = csv.writer(modified_file)
    writer.writerow(headers)
    writer.writerows(modified_lines[1:])
