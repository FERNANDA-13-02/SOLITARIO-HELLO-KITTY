"""Punto de entrada del Solitario Klondike."""

import tkinter as tk

try:
    from .interfaz import InterfazSolitario
except ImportError:
    from interfaz import InterfazSolitario


def main():
    """Crea la ventana raíz y inicia el bucle gráfico."""
    raiz = tk.Tk()
    InterfazSolitario(raiz)
    raiz.mainloop()


if __name__ == "__main__":
    main()
