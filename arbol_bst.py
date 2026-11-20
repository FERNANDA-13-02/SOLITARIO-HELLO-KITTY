"""Árbol binario de búsqueda implementado desde cero."""


class NodoBST:
    """Nodo con clave, dato y referencias a hijos."""

    def __init__(self, clave, dato):
        self.clave = clave
        self.dato = dato
        self.izquierdo = None
        self.derecho = None


class ArbolBST:
    """BST para puntuaciones. Las claves repetidas se conservan en una pila auxiliar."""

    def __init__(self):
        """Crea un árbol vacío."""
        self.raiz = None

    def insertar(self, clave, dato):
        """Inserta una clave; si existe, apila el dato en el nodo existente.

        Complejidad promedio O(log n), peor caso O(n).
        """
        if self.raiz is None:
            try:
                from .pila import Pila
            except ImportError:
                from pila import Pila
            pila = Pila()
            pila.apilar(dato)
            self.raiz = NodoBST(clave, pila)
            return
        actual = self.raiz
        while True:
            if clave == actual.clave:
                actual.dato.apilar(dato)
                return
            if clave < actual.clave:
                if actual.izquierdo is None:
                    try:
                        from .pila import Pila
                    except ImportError:
                        from pila import Pila
                    pila = Pila()
                    pila.apilar(dato)
                    actual.izquierdo = NodoBST(clave, pila)
                    return
                actual = actual.izquierdo
            else:
                if actual.derecho is None:
                    try:
                        from .pila import Pila
                    except ImportError:
                        from pila import Pila
                    pila = Pila()
                    pila.apilar(dato)
                    actual.derecho = NodoBST(clave, pila)
                    return
                actual = actual.derecho

    def buscar(self, clave):
        """Devuelve el dato del nodo encontrado o None. Complejidad promedio O(log n)."""
        actual = self.raiz
        while actual is not None:
            if clave == actual.clave:
                return actual.dato
            actual = actual.izquierdo if clave < actual.clave else actual.derecho
        return None

    def eliminar(self, clave):
        """Elimina una clave usando sucesor mínimo para dos hijos.

        Devuelve True si encontró la clave. Complejidad promedio O(log n), peor O(n).
        """
        encontrado = [False]

        def eliminar_nodo(nodo, clave_buscada):
            if nodo is None:
                return None
            if clave_buscada < nodo.clave:
                nodo.izquierdo = eliminar_nodo(nodo.izquierdo, clave_buscada)
            elif clave_buscada > nodo.clave:
                nodo.derecho = eliminar_nodo(nodo.derecho, clave_buscada)
            else:
                encontrado[0] = True
                if nodo.izquierdo is None:
                    return nodo.derecho
                if nodo.derecho is None:
                    return nodo.izquierdo
                sucesor = nodo.derecho
                while sucesor.izquierdo is not None:
                    sucesor = sucesor.izquierdo
                nodo.clave = sucesor.clave
                nodo.dato = sucesor.dato
                nodo.derecho = eliminar_nodo(nodo.derecho, sucesor.clave)
            return nodo

        self.raiz = eliminar_nodo(self.raiz, clave)
        return encontrado[0]

    def inorden(self):
        """Devuelve recorrido inorden ascendente. Complejidad O(n)."""
        resultado = []

        def visitar(nodo):
            if nodo is not None:
                visitar(nodo.izquierdo)
                resultado.append((nodo.clave, nodo.dato))
                visitar(nodo.derecho)

        visitar(self.raiz)
        return resultado

    def preorden(self):
        """Devuelve recorrido preorden. Complejidad O(n)."""
        resultado = []

        def visitar(nodo):
            if nodo is not None:
                resultado.append((nodo.clave, nodo.dato))
                visitar(nodo.izquierdo)
                visitar(nodo.derecho)

        visitar(self.raiz)
        return resultado

    def posorden(self):
        """Devuelve recorrido posorden. Complejidad O(n)."""
        resultado = []

        def visitar(nodo):
            if nodo is not None:
                visitar(nodo.izquierdo)
                visitar(nodo.derecho)
                resultado.append((nodo.clave, nodo.dato))

        visitar(self.raiz)
        return resultado
