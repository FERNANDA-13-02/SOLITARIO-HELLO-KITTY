"""Interfaz gráfica Tkinter del juego Solitario Klondike."""

import os
import tkinter as tk
from tkinter import messagebox

try:
    from .juego import JuegoSolitario
    from .puntuaciones import RegistroPuntuaciones
except ImportError:
    from juego import JuegoSolitario
    from puntuaciones import RegistroPuntuaciones


class InterfazSolitario:
    """Construye ventanas y traduce clics a operaciones de la lógica."""

    COLORES = {
        "fondo": "#fff4f8",
        "fondo_central": "#ffdce9",
        "panel": "#d93668",
        "panel_oscuro": "#a91f4d",
        "rosa": "#ef6fa6",
        "rosa_claro": "#ffe4ef",
        "rojo": "#d91f54",
        "blanco": "#fffafc",
        "texto": "#74233f",
        "boca_abajo": "#ef91b7",
        "boca_abajo_oscuro": "#cf527f",
        "verde": "#8dc7a2",
        "sombra": "#d7a1b5",
    }

    def __init__(self, root):
        """Recibe la ventana Tk raíz y crea el menú principal."""
        self.root = root
        self.root.title("Hello Kitty - Solitario Klondike")
        self.root.geometry("1120x760")
        self.root.minsize(900, 680)
        self.root.configure(bg=self.COLORES["fondo"])
        ruta_fondo = os.path.join(os.path.dirname(__file__), "hello_kitty_fondo.png")
        self.imagen_fondo = tk.PhotoImage(file=ruta_fondo)
        ruta_menu = os.path.join(os.path.dirname(__file__), "hello_kitty_menu.png")
        self.imagen_menu = tk.PhotoImage(file=ruta_menu).subsample(2, 2)
        self.juego = JuegoSolitario(cartas_por_robo=1)
        self.puntuaciones = RegistroPuntuaciones()
        self.seleccion = None
        self.botones_columnas = []
        self.botones_fundacion = []
        self.mostrar_menu()

    def limpiar(self):
        """Elimina widgets actuales para cambiar de pantalla."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def mostrar_menu(self):
        """Muestra el menú principal con las opciones requeridas."""
        self.limpiar()
        fondo = tk.Frame(self.root, bg=self.COLORES["fondo"])
        fondo.pack(fill="both", expand=True)
        self._poner_imagen_fondo(fondo)

        tk.Frame(fondo, bg="#efb8cc", height=8).pack(fill="x")
        encabezado = tk.Frame(fondo, bg=self.COLORES["panel"], height=92)
        encabezado.pack(fill="x")
        tk.Label(encabezado, text="♡  HELLO KITTY  ♡",
                 font=("Segoe UI", 25, "bold"), fg="white",
                 bg=self.COLORES["panel"]).place(relx=0.5, rely=0.48,
                                                   anchor="center")

        marco = tk.Canvas(
            fondo, width=338, height=395, highlightthickness=3,
            highlightbackground="#f2b0ca", bd=0)
        marco.place(relx=0.79, rely=0.57, anchor="center")
        marco.create_image(0, 0, image=self.imagen_menu, anchor="nw")
        marco.create_text(
            169, 34, text="SOLITARIO", font=("Segoe UI", 23, "bold"),
            fill=self.COLORES["panel"])
        marco.create_text(
            169, 65, text="KLONDIKE", font=("Segoe UI", 14, "bold"),
            fill=self.COLORES["texto"])
        opciones = (
            ("Nueva partida", self.iniciar_partida),
            ("Instrucciones", self.mostrar_instrucciones),
            ("Consultar puntuaciones", self.mostrar_puntuaciones),
            ("Salir", self.root.destroy),
        )
        for indice, (texto, accion) in enumerate(opciones):
            boton = self._boton(marco, texto, accion)
            boton.configure(font=("Segoe UI", 9, "bold"), width=25,
                            padx=4, pady=2)
            marco.create_window(
                169, 110 + indice * 40, window=boton, width=260, height=32)

    def _poner_imagen_fondo(self, contenedor):
        """Coloca el fondo bajo los controles del contenedor."""
        fondo = tk.Label(
            contenedor, image=self.imagen_fondo, anchor="nw",
            bg=self.COLORES["fondo"], bd=0)
        fondo.place(x=0, y=0, relwidth=1, relheight=1)
        fondo.lower()

    def _boton(self, padre, texto, accion, ancho=140):
        """Crea un botón rosa consistente con el tema."""
        return tk.Button(
            padre, text=texto, command=accion, width=22,
            font=("Segoe UI", 11, "bold"), fg="white",
            bg=self.COLORES["rosa"], activebackground=self.COLORES["rojo"],
            activeforeground="white", relief="flat", cursor="hand2",
            bd=0, padx=12, pady=8)

    def _dibujar_gatita(self, lienzo, cx, cy):
        """Dibuja una gatita decorativa original con orejas y lazo rosa."""
        lienzo.create_polygon(cx - 42, cy - 38, cx - 55, cy - 82,
                              cx - 16, cy - 55, fill="white",
                              outline="#dba4b7", width=2)
        lienzo.create_polygon(cx + 42, cy - 38, cx + 55, cy - 82,
                              cx + 16, cy - 55, fill="white",
                              outline="#dba4b7", width=2)
        lienzo.create_oval(cx - 66, cy - 58, cx + 66, cy + 74,
                           fill="white", outline="#dba4b7", width=3)
        lienzo.create_oval(cx - 33, cy - 15, cx - 27, cy - 5, fill="#40232d")
        lienzo.create_oval(cx + 27, cy - 15, cx + 33, cy - 5, fill="#40232d")
        lienzo.create_oval(cx - 5, cy - 2, cx + 5, cy + 6, fill="#f4a0b7")
        lienzo.create_line(cx - 57, cy + 5, cx - 25, cy + 1,
                           fill="#dba4b7", width=2)
        lienzo.create_line(cx - 57, cy + 23, cx - 25, cy + 13,
                           fill="#dba4b7", width=2)
        lienzo.create_line(cx + 57, cy + 5, cx + 25, cy + 1,
                           fill="#dba4b7", width=2)
        lienzo.create_line(cx + 57, cy + 23, cx + 25, cy + 13,
                           fill="#dba4b7", width=2)
        lienzo.create_oval(cx - 5, cy - 82, cx + 5, cy - 72,
                           fill=self.COLORES["rojo"], outline="")
        lienzo.create_oval(cx - 36, cy - 86, cx - 4, cy - 54,
                           fill=self.COLORES["rojo"], outline="#a91f4d")
        lienzo.create_oval(cx + 4, cy - 86, cx + 36, cy - 54,
                           fill=self.COLORES["rojo"], outline="#a91f4d")

    def iniciar_partida(self):
        """Crea una partida nueva y dibuja el tablero."""
        self.juego.nueva_partida()
        self.seleccion = None
        self._puntaje_registrado = False
        self.crear_tablero()

    def crear_tablero(self):
        """Construye mazo, descarte, fundaciones, columnas y controles."""
        self.limpiar()
        barra = tk.Frame(self.root, bg=self.COLORES["panel"], height=62)
        barra.pack(fill="x")
        tk.Label(barra, text="♡", font=("Segoe UI", 22, "bold"),
                 fg="white", bg=self.COLORES["panel"]).pack(side="left", padx=(14, 6))
        tk.Label(barra, text="SOLITARIO KITTY",
                 font=("Segoe UI", 16, "bold"), fg="white",
                 bg=self.COLORES["panel"]).pack(side="left", padx=(0, 18))

        controles = (
            ("Robar", self.robar),
            ("Deshacer", self.deshacer),
            ("Nueva", self.iniciar_partida),
            ("Abandonar", self.abandonar),
        )
        for texto, accion in controles:
            tk.Button(barra, text=texto, command=accion,
                      font=("Segoe UI", 9, "bold"), fg=self.COLORES["texto"],
                      bg=self.COLORES["rosa_claro"], activebackground="white",
                      relief="flat", padx=8, pady=5).pack(side="left", padx=3, pady=14)
        tk.Button(barra, text="Menú", command=self.mostrar_menu,
                  font=("Segoe UI", 9, "bold"), fg="white",
                  bg=self.COLORES["panel_oscuro"], activebackground=self.COLORES["rojo"],
                  relief="flat", padx=9, pady=5).pack(side="right", padx=(3, 12), pady=14)
        tk.Button(barra, text="Ayuda", command=self.mostrar_instrucciones,
                  font=("Segoe UI", 9, "bold"), fg="white",
                  bg=self.COLORES["panel_oscuro"], activebackground=self.COLORES["rojo"],
                  relief="flat", padx=9, pady=5).pack(side="right", padx=3, pady=14)

        superior = tk.Frame(self.root, bg=self.COLORES["fondo_central"])
        superior.pack(fill="x", padx=18, pady=(12, 8))
        self._poner_imagen_fondo(superior)
        tk.Label(superior, text="MAZO", bg=self.COLORES["fondo_central"],
                 fg=self.COLORES["texto"], font=("Segoe UI", 9, "bold")).grid(row=0, column=0)
        self.boton_mazo = tk.Button(
            superior, text="♡", width=7, height=4, command=self.robar,
            font=("Segoe UI", 16, "bold"), fg="white",
            bg=self.COLORES["boca_abajo"], activebackground=self.COLORES["boca_abajo_oscuro"],
            relief="ridge", bd=4)
        self.boton_mazo.grid(row=1, column=0, padx=8)

        tk.Label(superior, text="DESCARTE", bg=self.COLORES["fondo_central"],
                 fg=self.COLORES["texto"], font=("Segoe UI", 9, "bold")).grid(row=0, column=1)
        self.boton_descarte = tk.Button(
            superior, text="Vacío", width=7, height=4,
            command=self.seleccionar_descarte, font=("Segoe UI", 11, "bold"),
            bg=self.COLORES["blanco"], fg=self.COLORES["texto"], relief="ridge", bd=4)
        self.boton_descarte.grid(row=1, column=1, padx=8)

        tk.Label(superior, text="FUNDACIONES", bg=self.COLORES["fondo_central"],
                 fg=self.COLORES["texto"], font=("Segoe UI", 9, "bold")).grid(
            row=0, column=3, columnspan=4)
        self.botones_fundacion = []
        for indice in range(4):
            boton = tk.Button(
                superior, text="♡", width=7, height=4,
                command=lambda i=indice: self.seleccionar_fundacion(i),
                font=("Segoe UI", 11, "bold"), fg=self.COLORES["panel"],
                bg=self.COLORES["rosa_claro"], relief="ridge", bd=4)
            boton.grid(row=1, column=3 + indice, padx=8)
            self.botones_fundacion.append(boton)

        tablero = tk.Frame(self.root, bg=self.COLORES["fondo_central"])
        tablero.pack(fill="both", expand=True, padx=18, pady=(4, 8))
        self._poner_imagen_fondo(tablero)
        for indice in range(7):
            tk.Label(tablero, text=f"COLUMNA {indice + 1}",
                     bg=self.COLORES["fondo_central"], fg=self.COLORES["texto"],
                     font=("Segoe UI", 8, "bold")).grid(row=0, column=indice)

        self.botones_columnas = []
        for indice in range(7):
            marco = tk.Frame(tablero, bg=self.COLORES["fondo_central"], width=145)
            marco.grid(row=1, column=indice, padx=3, sticky="n")
            self.botones_columnas.append(marco)

        self.etiqueta_estado = tk.Label(self.root, text="", anchor="w",
                                        font=("Segoe UI", 10, "bold"),
                                        fg=self.COLORES["texto"], bg=self.COLORES["rosa_claro"])
        self.etiqueta_estado.pack(fill="x", side="bottom")
        self.actualizar_tablero()

    def robar(self):
        """Ejecuta el robo por el botón del mazo."""
        self.juego.robar()
        self.seleccion = None
        self.actualizar_tablero()

    def deshacer(self):
        """Restaura la última instantánea del historial propio."""
        self.juego.restaurar_estado()
        self.seleccion = None
        self.actualizar_tablero()

    def seleccionar_descarte(self):
        """Selecciona la carta superior del descarte."""
        if self.juego.descarte.esta_vacia():
            self.juego.mensaje = "El descarte está vacío"
        else:
            self.seleccion = ("descarte", None)
            self.juego.mensaje = "Carta del descarte seleccionada"
        self.actualizar_tablero()

    def seleccionar_fundacion(self, indice):
        """Intenta mover la selección a una fundación."""
        if self.seleccion is None:
            self.juego.mensaje = "Selecciona una carta primero"
        elif self.seleccion[0] == "descarte":
            self.juego.mover_descarte_a_fundacion(indice)
        elif self.seleccion[0] == "columna":
            self.juego.mover_columna_a_fundacion(self.seleccion[1], indice)
        self.seleccion = None
        self.actualizar_tablero()

    def seleccionar_carta_columna(self, columna, indice_carta):
        """Selecciona una carta o usa la selección para mover al destino."""
        cartas = self.juego.columnas[columna].recorrer_adelante()
        if indice_carta >= len(cartas):
            self.seleccionar_destino_columna(columna)
            return
        carta = cartas[indice_carta]
        if self.seleccion is None:
            if carta.boca_arriba:
                self.seleccion = ("columna", columna, indice_carta)
                self.juego.mensaje = f"Carta seleccionada: {carta.nombre()}"
            else:
                self.juego.mensaje = "No puedes seleccionar cartas boca abajo"
        elif self.seleccion[0] == "descarte":
            self.juego.mover_descarte_a_columna(columna)
            self.seleccion = None
        elif self.seleccion[0] == "columna":
            origen = self.seleccion[1]
            if origen == columna:
                self.seleccion = ("columna", columna, indice_carta)
            else:
                self.juego.mover_grupo_columna(origen, columna, self.seleccion[2])
                self.seleccion = None
        self.actualizar_tablero()

    def seleccionar_destino_columna(self, columna):
        """Usa el destino vacío de una columna o un destino sin carta superior."""
        if self.seleccion is None:
            self.juego.mensaje = "Selecciona una carta primero"
        elif self.seleccion[0] == "descarte":
            self.juego.mover_descarte_a_columna(columna)
        elif self.seleccion[0] == "columna":
            origen = self.seleccion[1]
            if origen != columna:
                self.juego.mover_grupo_columna(
                    origen, columna, self.seleccion[2])
        self.seleccion = None
        self.actualizar_tablero()

    def actualizar_tablero(self):
        """Redibuja todas las cartas y los indicadores de estado."""
        mazo_texto = "♡" if not self.juego.mazo.esta_vacia() else "Vacío"
        self.boton_mazo.configure(text=mazo_texto)

        if self.juego.descarte.esta_vacia():
            descarte_texto = "Vacío"
        else:
            descarte_texto = self.juego.descarte.ver_tope().nombre()
        self.boton_descarte.configure(text=descarte_texto)

        for indice, fundacion in enumerate(self.juego.fundaciones):
            texto = "♡" if fundacion.esta_vacia() else fundacion.ver_tope().nombre()
            self.botones_fundacion[indice].configure(text=texto)

        for columna_indice, marco in enumerate(self.botones_columnas):
            for widget in marco.winfo_children():
                widget.destroy()
            cartas = self.juego.columnas[columna_indice].recorrer_adelante()
            if not cartas:
                tk.Button(
                    marco, text="VACÍA\n♡", width=10, height=3,
                    font=("Segoe UI", 9, "bold"),
                    fg=self.COLORES["texto"], bg=self.COLORES["rosa_claro"],
                    relief="ridge", bd=3,
                    command=lambda c=columna_indice:
                        self.seleccionar_destino_columna(c)).pack(pady=2)
            for carta_indice, carta in enumerate(cartas):
                if carta.boca_arriba:
                    color = "#fffdfd"
                    fg = self.COLORES["rojo"] if carta.es_roja() else "#30262a"
                    texto = carta.nombre()
                else:
                    color = self.COLORES["boca_abajo"]
                    fg = "white"
                    texto = "♥\n♡"
                relieve = "raised"
                if (self.seleccion is not None
                        and self.seleccion[0] == "columna"
                        and self.seleccion[1] == columna_indice
                        and self.seleccion[2] <= carta_indice
                        and carta.boca_arriba):
                    relieve = "solid"
                boton = tk.Button(
                    marco, text=texto, width=9, height=2,
                    font=("Segoe UI", 11, "bold"),
                    bg=color, fg=fg, relief=relieve,
                    activebackground=self.COLORES["rosa_claro"],
                    bd=4 if relieve == "solid" else 2,
                    cursor="hand2",
                    command=lambda c=columna_indice, i=carta_indice:
                        self.seleccionar_carta_columna(c, i))
                boton.pack(pady=1)

        puntuacion = self.juego.puntuacion
        movimientos = self.juego.movimientos
        estado = f"{self.juego.mensaje}  |  Movimientos: {movimientos}  |  Puntuación: {puntuacion}"
        self.etiqueta_estado.configure(text=estado)
        if self.juego.estado == "victoria":
            self.completar_puntuacion()

    def completar_puntuacion(self):
        """Registra una victoria una sola vez al detectar el estado."""
        if getattr(self, "_puntaje_registrado", False):
            return
        self._puntaje_registrado = True
        from datetime import datetime
        self.puntuaciones.registrar(
            self.juego.puntuacion,
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            "victoria")
        messagebox.showinfo("Victoria", self.juego.mensaje)

    def abandonar(self):
        """Confirma el abandono y permite ver las puntuaciones."""
        if messagebox.askyesno("Abandonar", "¿Deseas abandonar la partida?"):
            self.juego.abandonar()
            self.actualizar_tablero()
            messagebox.showinfo("Partida finalizada", "Partida abandonada")

    def mostrar_instrucciones(self):
        """Muestra reglas completas en una ventana modal."""
        texto = (
            "• Se reparten 28 cartas en 7 columnas (1 a 7 cartas).\n"
            "• Las últimas cartas empiezan boca arriba.\n"
            "• En columnas: descendente y alternando rojo/negro.\n"
            "• Solo Reyes o grupos con Rey pueden ir a columnas vacías.\n"
            "• Fundaciones: As a Rey, mismo palo.\n"
            "• El mazo roba una carta por vez y se recicla desde el descarte.\n"
            "• Selecciona una carta y luego una columna o fundación.\n"
            "• Para mover un grupo, selecciona su primera carta visible.\n"
            "• Deshacer restaura el movimiento inmediatamente anterior.\n"
            "• Ganas al reunir las 52 cartas en las cuatro fundaciones."
        )
        self._mostrar_modal("Instrucciones", texto, 620, 470)

    def mostrar_puntuaciones(self):
        """Consulta el BST y muestra las mejores puntuaciones."""
        mejores = self.puntuaciones.mejores()
        if not mejores:
            texto = "No hay puntuaciones registradas."
        else:
            texto = "\n".join(
                f"{i}. {r['puntaje']} puntos - {r['fecha']} - {r['resultado']}"
                for i, r in enumerate(mejores, 1))
        self._mostrar_modal("Puntuaciones", texto, 520, 420)

    def _mostrar_modal(self, titulo, contenido, ancho, alto):
        """Muestra una ventana temática para instrucciones y puntuaciones."""
        ventana = tk.Toplevel(self.root)
        ventana.title(titulo)
        ventana.geometry(f"{ancho}x{alto}")
        ventana.configure(bg=self.COLORES["fondo"])
        ventana.transient(self.root)
        ventana.grab_set()

        encabezado = tk.Frame(ventana, bg=self.COLORES["panel"], height=70)
        encabezado.pack(fill="x")
        tk.Label(encabezado, text=f"♡  {titulo.upper()}",
                 font=("Segoe UI", 18, "bold"), fg="white",
                 bg=self.COLORES["panel"]).pack(pady=18)

        marco = tk.Frame(ventana, bg=self.COLORES["blanco"],
                         highlightthickness=3,
                         highlightbackground="#efb2ca")
        marco.pack(fill="both", expand=True, padx=24, pady=22)
        tk.Label(marco, text=contenido, justify="left", anchor="nw",
                 font=("Segoe UI", 11), fg=self.COLORES["texto"],
                 bg=self.COLORES["blanco"], padx=24, pady=18).pack(
                     fill="both", expand=True)
        self._boton(marco, "Cerrar", ventana.destroy, ancho=180).pack(pady=(0, 14))
