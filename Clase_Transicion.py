class Transicion:
    def __init__(self, origen = None, entrada = None, salida = None, destino = None, inserto = None) -> None:
        self.origen = origen
        self.entrada = entrada
        self.salida = salida
        self.destino = destino
        self.inserto = inserto


        # Eorigen, caracter que entra, caracter que saco de la pila, Edestino, caracter que introduzco a la pila