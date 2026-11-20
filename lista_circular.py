"""Lista circular enlazada implementada desde cero."""


class NodoCircular:
    """Nodo circular con dato y referencia siguiente."""

    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None


class ListaCircular:
    """Lista enlazada circular sin colecciones como sustituto."""

    def __init__(self):
        """Crea una lista vacía."""
        self.cabeza = None
        self._tamano = 0

    def insertar_inicio(self, elemento):
        """Inserta al inicio y conserva el cierre circular. Complejidad: O(n)."""
        nuevo = NodoCircular(elemento)
        if self.cabeza is None:
            nuevo.siguiente = nuevo
            self.cabeza = nuevo
        else:
            cola = self.cabeza
            while cola.siguiente is not self.cabeza:
                cola = cola.siguiente
            nuevo.siguiente = self.cabeza
            cola.siguiente = nuevo
            self.cabeza = nuevo
        self._tamano += 1

    def insertar_final(self, elemento):
        """Inserta al final. Complejidad: O(n)."""
        nuevo = NodoCircular(elemento)
        if self.cabeza is None:
            nuevo.siguiente = nuevo
            self.cabeza = nuevo
        else:
            cola = self.cabeza
            while cola.siguiente is not self.cabeza:
                cola = cola.siguiente
            cola.siguiente = nuevo
            nuevo.siguiente = self.cabeza
        self._tamano += 1

    def insertar_posicion(self, posicion, elemento):
        """Inserta en índice válido. Posiciones negativas o fuera de rango son inválidas."""
        if posicion < 0 or posicion > self._tamano:
            raise IndexError("Posición fuera de rango")
        if posicion == 0:
            self.insertar_inicio(elemento)
            return
        nuevo = NodoCircular(elemento)
        actual = self.cabeza
        anterior = None
        for _ in range(posicion):
            anterior = actual
            actual = actual.siguiente
        nuevo.siguiente = actual
        anterior.siguiente = nuevo
        self._tamano += 1

    def eliminar(self, elemento):
        """Elimina la primera coincidencia y devuelve True, o False. Complejidad: O(n)."""
        if self.cabeza is None:
            return False
        actual = self.cabeza
        anterior = None
        for _ in range(self._tamano):
            if actual.dato == elemento:
                if self._tamano == 1:
                    self.cabeza = None
                else:
                    cola = self.cabeza
                    while cola.siguiente is not self.cabeza:
                        cola = cola.siguiente
                    if actual is self.cabeza:
                        self.cabeza = actual.siguiente
                    if anterior is not None:
                        anterior.siguiente = actual.siguiente
                    else:
                        cola.siguiente = actual.siguiente
                self._tamano -= 1
                return True
            anterior = actual
            actual = actual.siguiente
        return False

    def buscar(self, elemento):
        """Busca elemento y devuelve el nodo o None. Complejidad: O(n)."""
        if self.cabeza is None:
            return None
        actual = self.cabeza
        for _ in range(self._tamano):
            if actual.dato == elemento:
                return actual
            actual = actual.siguiente
        return None

    def recorrer(self):
        """Recorre una sola vuelta y nunca sigue indefinidamente. Complejidad: O(n)."""
        resultado = []
        if self.cabeza is None:
            return resultado
        actual = self.cabeza
        for _ in range(self._tamano):
            resultado.append(actual.dato)
            actual = actual.siguiente
        return resultado

    def esta_vacia(self):
        """Indica si no contiene elementos. Complejidad: O(1)."""
        return self.cabeza is None

    def tamano(self):
        """Devuelve la cantidad de elementos. Complejidad: O(1)."""
        return self._tamano
