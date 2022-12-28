class Gramatica:
    def __init__(self, nombre  = None, no_terminales  = None, terminales  = None, no_terminal_inicial  = None) -> None:
        self.nombre = nombre
        self.no_terminales = no_terminales
        self.terminales = terminales
        self.no_terminal_inicial = no_terminal_inicial
        self.producciones = []