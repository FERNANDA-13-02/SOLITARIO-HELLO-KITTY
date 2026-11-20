"""Registro persistente de mejores puntuaciones mediante BST propio."""

import json
import os

try:
    from .arbol_bst import ArbolBST
except ImportError:
    from arbol_bst import ArbolBST


class RegistroPuntuaciones:
    """Carga, guarda y consulta puntuaciones mediante un Árbol BST."""

    def __init__(self, archivo="puntuaciones.json"):
        """Recibe la ruta de persistencia; el almacenamiento auxiliar usa JSON."""
        self.archivo = archivo
        self.arbol = ArbolBST()
        self.cargar()

    def cargar(self):
        """Carga registros válidos desde JSON. Complejidad O(n log n) en promedio."""
        if not os.path.exists(self.archivo):
            return
        with open(self.archivo, "r", encoding="utf-8") as archivo:
            registros = json.load(archivo)
        for registro in registros:
            self.arbol.insertar(registro["puntaje"], registro)

    def registrar(self, puntaje, fecha, resultado):
        """Inserta una puntuación y la guarda inmediatamente."""
        registro = {"puntaje": puntaje, "fecha": fecha, "resultado": resultado}
        self.arbol.insertar(puntaje, registro)
        self.guardar()

    def guardar(self):
        """Escribe el recorrido inorden como lista JSON auxiliar."""
        registros = []
        for clave, pila in self.arbol.inorden():
            registros.extend(pila.recorrer())
        with open(self.archivo, "w", encoding="utf-8") as archivo:
            json.dump(registros, archivo, ensure_ascii=False, indent=2)

    def mejores(self, limite=10):
        """Devuelve las mejores puntuaciones de mayor a menor."""
        descendente = []
        for clave, pila in self.arbol.inorden():
            descendente.append((clave, pila))
        descendente.reverse()
        resultados = []
        for clave, pila in descendente:
            for registro in pila.recorrer():
                resultados.append(registro)
                if len(resultados) >= limite:
                    return resultados
        return resultados
