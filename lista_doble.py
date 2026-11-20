"""Lista doblemente enlazada implementada desde cero."""


class NodoDoble:
    """Nodo con referencias anterior y siguiente."""

    def __init__(self, dato):
        self.dato = dato
        self.anterior = None
        self.siguiente = None


class ListaDoblementeEnlazada:
    """Lista navegable en ambos sentidos usada por las siete columnas."""

    def __init__(self):
        """Crea una lista vacía."""
        self.cabeza = None
        self.cola = None
        self._tamano = 0

    def insertar_inicio(self, elemento):
        """Inserta al inicio. Complejidad: O(1)."""
        nuevo = NodoDoble(elemento)
        nuevo.siguiente = self.cabeza
        if self.cabeza is not None:
            self.cabeza.anterior = nuevo
        else:
            self.cola = nuevo
        self.cabeza = nuevo
        self._tamano += 1

    def insertar_final(self, elemento):
        """Inserta al final. Complejidad: O(1)."""
        nuevo = NodoDoble(elemento)
        nuevo.anterior = self.cola
        if self.cola is not None:
            self.cola.siguiente = nuevo
        else:
            self.cabeza = nuevo
        self.cola = nuevo
        self._tamano += 1

    def insertar_posicion(self, posicion, elemento):
        """Inserta en una posición válida. Complejidad: O(n)."""
        if posicion < 0 or posicion > self._tamano:
            raise IndexError("Posición fuera de rango")
        if posicion == 0:
            self.insertar_inicio(elemento)
        elif posicion == self._tamano:
            self.insertar_final(elemento)
        else:
            actual = self.cabeza
            for _ in range(posicion):
                actual = actual.siguiente
            nuevo = NodoDoble(elemento)
            nuevo.anterior = actual.anterior
            nuevo.siguiente = actual
            actual.anterior.siguiente = nuevo
            actual.anterior = nuevo
            self._tamano += 1

    def eliminar(self, elemento):
        """Elimina la primera coincidencia y conserva ambos enlaces. Complejidad: O(n)."""
        actual = self.cabeza
        while actual is not None:
            if actual.dato == elemento:
                if actual.anterior is not None:
                    actual.anterior.siguiente = actual.siguiente
                else:
                    self.cabeza = actual.siguiente
                if actual.siguiente is not None:
                    actual.siguiente.anterior = actual.anterior
                else:
                    self.cola = actual.anterior
                actual.anterior = None
                actual.siguiente = None
                self._tamano -= 1
                return True
            actual = actual.siguiente
        return False

    def buscar(self, elemento):
        """Devuelve el nodo coincidente o None. Complejidad: O(n)."""
        actual = self.cabeza
        while actual is not None:
            if actual.dato == elemento:
                return actual
            actual = actual.siguiente
        return None

    def recorrer_adelante(self):
        """Recorre desde cabeza hasta cola. Complejidad: O(n)."""
        resultado = []
        actual = self.cabeza
        while actual is not None:
            resultado.append(actual.dato)
            actual = actual.siguiente
        return resultado

    def recorrer_atras(self):
        """Recorre desde cola hasta cabeza. Complejidad: O(n)."""
        resultado = []
        actual = self.cola
        while actual is not None:
            resultado.append(actual.dato)
            actual = actual.anterior
        return resultado

    def esta_vacia(self):
        """Indica si la lista está vacía. Complejidad: O(1)."""
        return self.cabeza is None

    def tamano(self):
        """Devuelve el número de nodos. Complejidad: O(1)."""
        return self._tamano
