"""Cola enlazada implementada desde cero con nodos."""


class NodoCola:
    """Nodo de cola con dato y referencia al siguiente."""

    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None


class Cola:
    """Cola FIFO con referencias al primero y al último."""

    def __init__(self):
        """Crea una cola vacía."""
        self.primero = None
        self.ultimo = None
        self._tamano = 0

    def encolar(self, elemento):
        """Inserta al final. Complejidad: O(1)."""
        nuevo = NodoCola(elemento)
        if self.ultimo is None:
            self.primero = nuevo
            self.ultimo = nuevo
        else:
            self.ultimo.siguiente = nuevo
            self.ultimo = nuevo
        self._tamano += 1

    def desencolar(self):
        """Retira el frente; devuelve None si está vacía. Complejidad: O(1)."""
        if self.esta_vacia():
            return None
        dato = self.primero.dato
        self.primero = self.primero.siguiente
        if self.primero is None:
            self.ultimo = None
        self._tamano -= 1
        return dato

    def ver_frente(self):
        """Devuelve el frente sin retirarlo. Complejidad: O(1)."""
        return None if self.esta_vacia() else self.primero.dato

    def esta_vacia(self):
        """Indica si la cola no tiene elementos. Complejidad: O(1)."""
        return self.primero is None

    def tamano(self):
        """Devuelve el tamaño almacenado. Complejidad: O(1)."""
        return self._tamano
