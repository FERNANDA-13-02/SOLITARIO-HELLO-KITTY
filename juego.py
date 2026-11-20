"""Lógica independiente de Tkinter del Solitario Klondike."""

import random

try:
    from .carta import Carta
    from .pila import Pila
    from .cola import Cola
    from .lista_circular import ListaCircular
    from .lista_doble import ListaDoblementeEnlazada
except ImportError:
    from carta import Carta
    from pila import Pila
    from cola import Cola
    from lista_circular import ListaCircular
    from lista_doble import ListaDoblementeEnlazada


class JuegoSolitario:
    """Coordina la partida y conserva las 52 cartas sin duplicados."""

    def __init__(self, cartas_por_robo=1, sembrar_aleatorio=None):
        """Recibe la variante de robo y opcionalmente una función semilla."""
        self.cartas_por_robo = cartas_por_robo
        self.semilla = sembrar_aleatorio
        self.mazo = Cola()
        self.reciclaje = ListaCircular()
        self.descarte = Pila()
        self.columnas = []
        self.fundaciones = []
        self.historial = Pila()
        self.movimientos = 0
        self.puntuacion = 0
        self.estado = "nueva"
        self.mensaje = "Nueva partida"

    def nueva_partida(self):
        """Baraja, reparte e inicializa todas las zonas de la partida."""
        baraja = [Carta(palo, valor)
                  for palo in Carta.PALOS
                  for valor in range(1, 14)]
        if self.semilla is not None:
            self.semilla(baraja)
        else:
            random.shuffle(baraja)

        self.mazo = Cola()
        self.reciclaje = ListaCircular()
        self.descarte = Pila()
        self.columnas = [ListaDoblementeEnlazada() for _ in range(7)]
        self.fundaciones = [Pila() for _ in range(4)]
        self.historial = Pila()
        self.movimientos = 0
        self.puntuacion = 0
        self.estado = "jugando"
        self.mensaje = "Partida iniciada"

        indice = 0
        for numero_columna in range(7):
            for posicion in range(numero_columna + 1):
                carta = baraja[indice]
                carta.boca_arriba = posicion == numero_columna
                self.columnas[numero_columna].insertar_final(carta)
                indice += 1

        for carta in baraja[indice:]:
            carta.boca_arriba = False
            self.mazo.encolar(carta)
            self.reciclaje.insertar_final(carta)

    def contar_cartas(self):
        """Cuenta todas las cartas visibles en las zonas y devuelve el total."""
        total = self.mazo.tamano()
        total += self.descarte.tamano()
        for columna in self.columnas:
            total += columna.tamano()
        for fundacion in self.fundaciones:
            total += fundacion.tamano()
        return total

    def conjunto_cartas(self):
        """Devuelve las claves existentes para comprobar duplicados."""
        claves = []
        actual = self.mazo.primero
        while actual is not None:
            claves.append(actual.dato.clave())
            actual = actual.siguiente
        claves.extend(carta.clave() for carta in self.descarte.recorrer())
        for columna in self.columnas:
            claves.extend(carta.clave() for carta in columna.recorrer_adelante())
        for fundacion in self.fundaciones:
            claves.extend(carta.clave() for carta in fundacion.recorrer())
        return claves

    def guardar_estado(self):
        """Guarda una instantánea serializada mínima antes de una acción.

        Complejidad: O(52) porque una partida nunca supera ese tamaño.
        """
        snapshot = {
            "mazo": [(c.palo, c.valor, c.boca_arriba)
                     for c in self.recorrer_cola(self.mazo)],
            "reciclaje": [(c.palo, c.valor, c.boca_arriba)
                          for c in self.reciclaje.recorrer()],
            "descarte": [(c.palo, c.valor, c.boca_arriba)
                         for c in self.descarte.recorrer()],
            "columnas": [[(c.palo, c.valor, c.boca_arriba)
                          for c in columna.recorrer_adelante()]
                         for columna in self.columnas],
            "fundaciones": [[(c.palo, c.valor, c.boca_arriba)
                             for c in fundacion.recorrer()]
                            for fundacion in self.fundaciones],
            "movimientos": self.movimientos,
            "puntuacion": self.puntuacion,
            "mensaje": self.mensaje,
        }
        self.historial.apilar(snapshot)

    @staticmethod
    def recorrer_cola(cola):
        """Recorre una Cola auxiliarmente sin modificar su frente ni su cola."""
        resultado = []
        actual = cola.primero
        while actual is not None:
            resultado.append(actual.dato)
            actual = actual.siguiente
        return resultado

    def restaurar_estado(self):
        """Deshace al último estado guardado. Devuelve True si pudo hacerlo."""
        snapshot = self.historial.desapilar()
        if snapshot is None:
            self.mensaje = "No hay movimientos para deshacer"
            return False

        def reconstruir(tupla):
            carta = Carta(tupla[0], tupla[1], tupla[2])
            return carta

        self.mazo = Cola()
        for datos in snapshot["mazo"]:
            self.mazo.encolar(reconstruir(datos))

        self.reciclaje = ListaCircular()
        for datos in snapshot["reciclaje"]:
            self.reciclaje.insertar_final(reconstruir(datos))

        self.descarte = Pila()
        for datos in reversed(snapshot["descarte"]):
            self.descarte.apilar(reconstruir(datos))

        self.columnas = [ListaDoblementeEnlazada() for _ in range(7)]
        for indice, datos_columna in enumerate(snapshot["columnas"]):
            for datos in datos_columna:
                self.columnas[indice].insertar_final(reconstruir(datos))

        self.fundaciones = [Pila() for _ in range(4)]
        for indice, datos_fundacion in enumerate(snapshot["fundaciones"]):
            for datos in datos_fundacion:
                self.fundaciones[indice].apilar(reconstruir(datos))

        self.movimientos = snapshot["movimientos"]
        self.puntuacion = snapshot["puntuacion"]
        self.mensaje = "Movimiento deshecho"
        self.estado = "jugando"
        return True

    def robar(self):
        """Roba una o tres cartas de la cola y las mueve al descarte."""
        if self.estado != "jugando":
            return False
        if self.mazo.esta_vacia():
            if self.descarte.esta_vacia():
                self.mensaje = "El mazo no tiene cartas"
                return False
            self.reciclar_mazo()
            if self.mazo.esta_vacia():
                return False

        self.guardar_estado()
        robadas = 0
        while robadas < self.cartas_por_robo and not self.mazo.esta_vacia():
            carta = self.mazo.desencolar()
            carta.boca_arriba = True
            self.descarte.apilar(carta)
            robadas += 1
        self.movimientos += 1
        self.puntuacion += 1
        self.mensaje = f"Robadas {robadas} carta(s)"
        return True

    def reciclar_mazo(self):
        """Recicla el descarte mediante la lista circular hacia la cola del mazo."""
        if self.descarte.esta_vacia():
            return
        self.reciclaje = ListaCircular()
        cartas = self.descarte.recorrer()
        for carta in reversed(cartas):
            carta.boca_arriba = False
            self.reciclaje.insertar_final(carta)
        for carta in self.reciclaje.recorrer():
            self.mazo.encolar(carta)
        while not self.descarte.esta_vacia():
            self.descarte.desapilar()
        self.mensaje = "Mazo reciclado"

    def mover_descarte_a_columna(self, indice_columna):
        """Mueve la carta superior del descarte a una columna."""
        if self.descarte.esta_vacia():
            self.mensaje = "El descarte está vacío"
            return False
        carta = self.descarte.ver_tope()
        if not self.columna_acepta(indice_columna, carta):
            self.mensaje = "Movimiento inválido al destino"
            return False
        self.guardar_estado()
        carta = self.descarte.desapilar()
        carta.boca_arriba = True
        self.columnas[indice_columna].insertar_final(carta)
        self.movimientos += 1
        self.puntuacion += 5
        self.mensaje = "Carta movida a columna"
        self.comprobar_victoria()
        return True

    def columna_acepta(self, indice_columna, carta):
        """Valida rey vacío o alternancia de color y valor descendente."""
        if indice_columna < 0 or indice_columna >= 7:
            return False
        columna = self.columnas[indice_columna]
        if columna.esta_vacia():
            return isinstance(carta, Carta) and carta.valor == 13
        ultima = columna.cola.dato
        return carta.boca_arriba and carta.puede_ir_sobre(ultima)

    def mover_grupo_columna(self, origen, destino, indice_carta):
        """Mueve una carta o grupo descubierta entre columnas."""
        if origen == destino or not (0 <= origen < 7 and 0 <= destino < 7):
            self.mensaje = "Origen o destino inválido"
            return False
        cartas = self.columnas[origen].recorrer_adelante()
        if indice_carta < 0 or indice_carta >= len(cartas):
            self.mensaje = "Carta no seleccionada"
            return False
        grupo = cartas[indice_carta:]
        if any(not carta.boca_arriba for carta in grupo):
            self.mensaje = "No puedes mover cartas boca abajo"
            return False
        if not self.secuencia_valida(grupo):
            self.mensaje = "El grupo no forma una secuencia válida"
            return False
        if not self.columna_acepta(destino, grupo[0]):
            self.mensaje = "Movimiento inválido al destino"
            return False

        self.guardar_estado()
        for carta in grupo:
            self.columnas[origen].eliminar(carta)
            self.columnas[destino].insertar_final(carta)
        self.voltear_ultima_visible(origen)
        self.movimientos += 1
        self.puntuacion += 5
        self.mensaje = "Grupo movido"
        self.comprobar_victoria()
        return True

    @staticmethod
    def secuencia_valida(grupo):
        """Comprueba que un grupo sea descendente, alternado y descubierto."""
        if not grupo:
            return False
        for indice in range(len(grupo) - 1):
            if not grupo[indice + 1].puede_ir_sobre(grupo[indice]):
                return False
        return all(carta.boca_arriba for carta in grupo)

    def voltear_ultima_visible(self, indice_columna):
        """Voltea boca arriba la última carta si quedó descubierta."""
        columna = self.columnas[indice_columna]
        if not columna.esta_vacia() and not columna.cola.dato.boca_arriba:
            columna.cola.dato.boca_arriba = True
            self.puntuacion += 5

    def mover_descarte_a_fundacion(self, indice_fundacion):
        """Mueve la carta superior del descarte a una fundación válida."""
        if self.descarte.esta_vacia():
            self.mensaje = "El descarte está vacío"
            return False
        carta = self.descarte.ver_tope()
        if not self.fundacion_acepta(indice_fundacion, carta):
            self.mensaje = "Movimiento inválido a fundación"
            return False
        self.guardar_estado()
        carta = self.descarte.desapilar()
        self.fundaciones[indice_fundacion].apilar(carta)
        self.movimientos += 1
        self.puntuacion += 10
        self.mensaje = "Carta enviada a fundación"
        self.comprobar_victoria()
        return True

    def mover_columna_a_fundacion(self, indice_columna, indice_fundacion):
        """Mueve el tope de una columna a una fundación válida."""
        if not (0 <= indice_columna < 7 and 0 <= indice_fundacion < 4):
            self.mensaje = "Origen o fundación inválida"
            return False
        columna = self.columnas[indice_columna]
        if columna.esta_vacia():
            self.mensaje = "La columna está vacía"
            return False
        carta = columna.cola.dato
        if not carta.boca_arriba or not self.fundacion_acepta(indice_fundacion, carta):
            self.mensaje = "Movimiento inválido a fundación"
            return False
        self.guardar_estado()
        columna.eliminar(carta)
        self.fundaciones[indice_fundacion].apilar(carta)
        self.voltear_ultima_visible(indice_columna)
        self.movimientos += 1
        self.puntuacion += 10
        self.mensaje = "Carta enviada a fundación"
        self.comprobar_victoria()
        return True

    def fundacion_acepta(self, indice_fundacion, carta):
        """Valida As inicial y valores ascendentes del mismo palo."""
        if not (0 <= indice_fundacion < 4):
            return False
        fundacion = self.fundaciones[indice_fundacion]
        if fundacion.esta_vacia():
            return isinstance(carta, Carta) and carta.valor == 1
        tope = fundacion.ver_tope()
        return carta.mismo_palo(tope) and carta.valor == tope.valor + 1

    def comprobar_victoria(self):
        """Comprueba si las cuatro fundaciones contienen las 52 cartas."""
        total = sum(fundacion.tamano() for fundacion in self.fundaciones)
        if total == 52:
            self.estado = "victoria"
            self.mensaje = "¡Victoria! Las 52 cartas están en las fundaciones"
            return True
        return False

    def abandonar(self):
        """Marca una partida como abandonada por decisión del usuario."""
        self.estado = "abandonada"
        self.mensaje = "Partida abandonada"
