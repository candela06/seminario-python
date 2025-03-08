### Integrantes del proyecto:

- Candela Silva
- Manuel Peñalba
- Malena Kairiyama
- Karen Kairiyama  

---
  
## Instrucciones para ejecutar las aplicaciones:
  
1. Copiar con el comando ```git clone <link>``` el enlace del poyecto.
2. Generar un entorno virtual con el comando ```python3 -m venv venv```.
3. Activar el entorno virtual, para linux: ```source venv/bin/activate```, para windows: ```source venv\Scripts\activate```.  
4. Instalar la versión de python 3.11.x desde git o de forma directa.
5. Ejecutar ```pip install -r requirements.txt``` para instalar todas las librerías. Entre ellas Jupyter notebook y StreamLit.

```bash
git clone git@github.com:candela06/seminario-python.git
python3 -m venv venv  
source venv/bin/activate  
pip install -r requirements.txt  
```

#### Datasets
En la carpeta **modules** se encuentran 4 archivos *processing* enumerados. Ejecutar cada uno de ellos desde la terminal con el comando ```python <archivo.py>``` o ```python3 <archivo.py>``` para tener acceso a las datasets modificados:
```bash
cd modules
python processing_1.py
python processing_2.py
python processing_3.py
python processing_4.py
```

#### Consultas
>**WARNING:** antes de correr los jupyter notebooks es necesario ejecutar los procesos mencionados anteriormente. 

En la terminal, desde el directorio **notebooks** ejecutar ```jupyter notebook``` para iniciar el servidor de jupyter notebook en una pestaña del navegador. No es necesario abrirlo desde la terminal si trabajamos con vscode como IDE. 
```bash
cd notebooks
jupyter notebook
```

>   Las primeras 3 consultas se encuentran en consultas_1.ipynb.

>   Las consultas 4, 5 y 6 se encuentran en consultas_2.ipynb.

>   Las 7, 8 y 9 en consultas_3.ipynb.

>   Consultas 10, 11 y 12 se encuentran en consultas_4.ipybn.

---
#### Juego PyTrivia
Luego de seguir las **Instrucciones para ejecutar las aplicaciones**(especificadas más arriba). Desde el directorio **game_app** ejecutar el comando ```streamlit run Inicio.py```.  Streamlit iniciará un servidor local y abrirá la aplicación en tu navegador web predeterminado y comenzará el juego!
```bash
cd game_app
streamlit run Inicio.py
```
