
class Automata:
    def __init__(self, nombre  = None, alfabeto  = None, simbolosP  = None, estados  = None, estado_inicial = None, estado_aceptacion = None) -> None:
        self.nombre = nombre
        self.alfabeto = alfabeto
        self.simbolosP = simbolosP
        self.estados = estados
        self.estado_inicial = estado_inicial
        self.estado_aceptacion = estado_aceptacion
        self.transiciones = []