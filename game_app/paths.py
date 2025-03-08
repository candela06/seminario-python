#paths juego
from pathlib import Path

GAME_APP= Path(__file__).resolve().parent
#GAME_DIR= ROOTDIR / 'game_app'
PAGES_DIR= GAME_APP / 'pages'
FORM_PATH= PAGES_DIR / '04_📝_Formulario.py'
GAME_PATH= PAGES_DIR / '03_🎮_Juego.py'
RANKING_PATH= PAGES_DIR / 'Ranking.py'
STATISTICS_PATH= PAGES_DIR / '05_📊_Estadisticas.py'

PARTIDAS_DATA = GAME_APP / 'user_data' / 'partidas.csv'
USUARIOS_DATA = GAME_APP / 'user_data' / 'user_data.json'