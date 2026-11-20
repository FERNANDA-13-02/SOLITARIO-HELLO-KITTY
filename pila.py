"""Pila enlazada implementada desde cero con nodos."""


class NodoPila:
    """Nodo de pila. Contiene dato y referencia al nodo siguiente."""

    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None


class Pila:
    """Pila LIFO construida con referencias; no usa list, deque ni Stack."""

    def __init__(self):
        """Crea una pila vacía."""
        self.tope = None
        self._tamano = 0

    def apilar(self, elemento):
        """Recibe un elemento y lo inserta en el tope. Complejidad: O(1)."""
        nuevo = NodoPila(elemento)
        nuevo.siguiente = self.tope
        self.tope = nuevo
        self._tamano += 1

    def desapilar(self):
        """Retira y devuelve el tope, o None si está vacía. Complejidad: O(1)."""
        if self.esta_vacia():
            return None
        dato = self.tope.dato
        self.tope = self.tope.siguiente
        self._tamano -= 1
        return dato

    def ver_tope(self):
        """Devuelve el elemento superior sin retirarlo. Complejidad: O(1)."""
        return None if self.esta_vacia() else self.tope.dato

    def esta_vacia(self):
        """Indica si no contiene elementos. Complejidad: O(1)."""
        return self.tope is None

    def tamano(self):
        """Devuelve la cantidad de elementos. Complejidad: O(1)."""
        return self._tamano

    def recorrer(self):
        """Recorre desde el tope para pruebas y depuración. Complejidad: O(n)."""
        resultado = []
        actual = self.tope
        while actual is not None:
            resultado.append(actual.dato)
            actual = actual.siguiente
        return resultado
