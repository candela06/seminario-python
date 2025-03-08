import pathlib
import csv


"""
2. En el dataset de Conectividad (B), se realizará un reemplazo en las celdas que contengan el carácter '-' con la palabra 'NO'
"""

path_conectividad = pathlib.Path('..','data','Conectividad_Internet.csv')
connectivity_path_modified = pathlib.Path('..','data_modify','Conectividad_Internet.csv')



"""
replace_dash es una función lambda con una variable 'row', row va a recibir una fila de celdas de 'Conectividad_Internet.csv'. La segunda función lambda toma una celda de fila que tiene 'row' y reemplaza con 'cell.replace' '--' por 'NO'. Map aplica esta función a cada celda de la fila, generando con list() una lista modificada a base de la fila original que contenía 'row'

La función all_fields_empty() recibe una fila y devueve true si todos los elementos son '--'
"""

def all_fields_empty(row):
    return all(cell == '--' for cell in row[4:13])

replace_dash = lambda row: list(map(lambda cell: cell.replace('--', 'NO'), row))




with open(path_conectividad, 'r',encoding='utf-8',newline='') as connectivity_file:
    connectivity_reader = csv.reader(connectivity_file) # iterador de lectura para las filas del archivo original
    connectivity_header = next(connectivity_reader)     # me traigo la primera fila que es el header
    connectivity_header.append('posee_conectividad')    # agrego al header la nueva columna. 


    with open(connectivity_path_modified,'w',encoding='utf-8',newline='') as new_connectivity_file:
        connectivity_writer = csv.writer(new_connectivity_file)   # iterador de escritura para el nuevo archivo  
        connectivity_writer.writerow(connectivity_header)   #escribo el header nuevo

        for row in connectivity_reader:
            if all_fields_empty(row):
                row.append('NO')
            else: row.append('SI')
            connectivity_writer.writerow(replace_dash(row))   
"""
el bucle for itera en cada fila del archivo original, pregunta si todos los campos son '--' con all_fields_empty() y agrega SI o NO. Finalmente escribe la nueva fila llamando a replace_dash para que reemplace '--' por 'NO'

"""