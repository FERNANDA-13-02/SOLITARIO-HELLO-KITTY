"""Representa una carta del Solitario Klondike."""


class Carta:
    """Datos y estado visible de una carta.

    Recibe: palo, valor y si está boca arriba.
    Devuelve: objetos Carta comparables por identidad lógico-palo-valor.
    """

    PALOS = ("corazones", "diamantes", "treboles", "picas")
    ROJOS = ("corazones", "diamantes")
    NEGROS = ("treboles", "picas")

    def __init__(self, palo, valor, boca_arriba=False):
        """Inicializa una carta sin colecciones externas como almacenamiento."""
        self.palo = palo
        self.valor = valor
        self.boca_arriba = boca_arriba

    def es_roja(self):
        """Devuelve True si el palo es rojo."""
        return self.palo in self.ROJOS

    def mismo_palo(self, otra):
        """Devuelve True si ambas cartas pertenecen al mismo palo."""
        return isinstance(otra, Carta) and self.palo == otra.palo

    def puede_ir_sobre(self, otra):
        """Indica si esta carta puede colocarse sobre otra carta en una columna."""
        if not isinstance(otra, Carta):
            return False
        return self.valor == otra.valor - 1 and self.es_roja() != otra.es_roja()

    def clave(self):
        """Devuelve una clave única estable formada por palo y valor."""
        return f"{self.palo}-{self.valor}"

    def nombre(self):
        """Devuelve el nombre visible de la carta."""
        nombres = {11: "J", 12: "Q", 13: "K", 1: "A"}
        valor = nombres.get(self.valor, str(self.valor))
        simbolos = {"corazones": "♥", "diamantes": "♦", "treboles": "♣", "picas": "♠"}
        return f"{valor}{simbolos[self.palo]}"

    def __eq__(self, otra):
        """Compara cartas por su palo y valor."""
        return isinstance(otra, Carta) and self.palo == otra.palo and self.valor == otra.valor

    def __hash__(self):
        """Permite usar la carta como clave auxiliar sin reemplazar estructuras evaluadas."""
        return hash((self.palo, self.valor))

    def __str__(self):
        """Devuelve el texto visible de la carta."""
        return self.nombre() if self.boca_arriba else "[  ]"
