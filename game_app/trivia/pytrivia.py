from unidecode import unidecode

class Jugador():
    """
    Clase que representa a un jugador en el juego.

    Attributes
    ----------
    tematica : str
        La temática del juego.
    usuario : str
        El nombre de usuario del jugador.
    fecha : str
        La fecha de la partida.
    dificultad : str
        La dificultad seleccionada para la partida.
    user_correct_answer : list
        Lista de respuestas correctas del usuario.
    puntos : int
        Puntos acumulados por el jugador.

    Methods
    -------
    get_usuario()
        Devuelve el nombre de usuario del jugador.
    get_tematica()
        Devuelve la temática del juego.
    get_dificultad()
        Devuelve la dificultad seleccionada para la partida.
    get_puntos()
        Devuelve los puntos acumulados por el jugador.
    set_puntos(new_puntos)
        Establece los puntos acumulados por el jugador.
    get_user_correct_answer()
        Devuelve la lista de respuestas correctas del usuario.
    set_user_correct_answer(new_user_correct_answer)
        Establece la lista de respuestas correctas del usuario.
    to_dict()
        Devuelve un diccionario con los datos del jugador.
    calcular_puntos(user_answers_list, correct_answers_list)
        Calcula los puntos obtenidos por el jugador basado en sus respuestas y la dificultad seleccionada.
    """
    
    def __init__(self, tematica, usuario, fecha, dificultad, puntos):
        """
        Inicializa la clase Jugador con los atributos proporcionados.

        Parameters
        ----------
        tematica : str
            La temática del juego.
        usuario : str
            El nombre de usuario del jugador.
        fecha : str
            La fecha de la partida.
        dificultad : str
            La dificultad seleccionada para la partida.
        puntos : int
            Puntos acumulados por el jugador.
        """
        self.tematica = tematica
        self.usuario = usuario
        self.fecha = fecha
        self.dificultad = dificultad
        self.user_correct_answer = []
        self.puntos = puntos

    def get_usuario(self):
        """Devuelve el nombre de usuario del jugador."""
        return self.usuario 
     
    def get_tematica(self):
        """Devuelve la temática del juego."""
        return self.tematica
    
    def get_dificultad(self):
        """Devuelve la dificultad seleccionada para la partida."""
        return self.dificultad
    
    def get_puntos(self):
        """Devuelve los puntos acumulados por el jugador."""
        return self.puntos
    
    def set_puntos(self, new_puntos):
        """Establece los puntos acumulados por el jugador."""
        self.puntos = new_puntos
        
    def get_user_correct_answer(self):
        """Devuelve la lista de respuestas correctas del usuario."""
        return self.user_correct_answer
    
    def set_user_correct_answer(self,new_user_correct_answer):
        """Establece la lista de respuestas correctas del usuario."""
        self.user_correct_answer = new_user_correct_answer

    def to_dict(self):
        """Devuelve un diccionario con los datos del jugador."""
        return {
            'username': self.usuario,
            'fecha': self.fecha,
            'tematica': self.tematica,
            'dificultad': self.dificultad,
            'puntos': self.puntos
        }

    def calcular_puntos(self, user_answers_list,correct_answers_list):
        """
        Calcula los puntos obtenidos por el jugador basado en sus respuestas y la dificultad seleccionada.

        Parameters
        ----------
        user_answers_list : list
            Lista de respuestas proporcionadas por el usuario.
        correct_answers_list : list
            Lista de respuestas correctas.

        Returns
        -------
        int
            Puntos acumulados después de comparar las respuestas del usuario con las correctas.
        
        Notes
        -----
        - La función compara las respuestas del usuario con las correctas, incrementando el puntaje por cada respuesta correcta.
        - Si las respuestas son numéricas, se comparan directamente.
        - Si las respuestas no son numéricas, se convierten a mayúsculas y se eliminan los caracteres especiales para la comparación.
        - El puntaje se incrementa adicionalmente basado en la dificultad seleccionada ('Medio' o 'Dificil').
        """
        puntos = 0
        aux_list = []
        # Itera sobre las respuestas del usuario y las respuestas correctas simultáneamente
        for user_answer, correct_answer in zip(user_answers_list, correct_answers_list):
            # Verifica si las respuestas son números (int o float)
            if isinstance(user_answer, (int, float)) and isinstance(correct_answer, (int, float)):
                if user_answer == correct_answer:
                    puntos += 1
                    aux_list.append[user_answer]
            # Si las respuestas no son números, las convierte a mayúsculas y elimina espacios
            else:
                if unidecode(str(user_answer).strip().upper()) == unidecode(str(correct_answer).strip().upper()):
                    puntos += 1
                    aux_list.append(user_answer)
        # Aplica bonificación por dificultad
        if self.dificultad == "Medio":
            puntos = puntos * 1.5 # Aumenta el puntaje en un 50% para dificultad media
        elif self.dificultad == "Dificil": # Duplica el puntaje para dificultad difícil
            puntos = puntos * 2

        self.set_user_correct_answer(aux_list)

        return puntos    
