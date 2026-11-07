import tkinter as tk
from tkinter import ttk, messagebox

import customtkinter as ctk

from utils import estilos


class VistaLibros(ctk.CTkFrame):
    """Pantalla de Gestión de Libros (formulario a la izquierda, tabla a la derecha)."""

    # Columnas de la tabla: (clave del diccionario, texto del encabezado, ancho)
    COLUMNAS = [
        ("ISBN", "ISBN", 115),
        ("Titulo", "Título", 165),
        ("Autor", "Autor", 145),
        ("Editorial", "Editorial", 120),
        ("Categoria", "Categoría", 95),
        ("Anio", "Año", 50),
        ("Existencias", "Existencias", 100),
    ]

    def __init__(self, master, controlador=None):
        super().__init__(master, fg_color=estilos.COLOR_FONDO, corner_radius=0)
        self.controlador = controlador

        # Diccionarios para traducir el texto de las listas a su Id
        # Ejemplo: {"1 - Gabriel García Márquez": 1}
        self._autores = {}
        self._editoriales = {}

        self.campos = {}  # Aquí se guardan las cajas del formulario

        # La columna 1 (la tabla) crece si se agranda la ventana
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._crear_encabezado()
        self._crear_panel_izquierdo()
        self._crear_tabla()

    # =====================================================
    # CONSTRUCCIÓN DE LA PANTALLA
    # =====================================================

    def _crear_encabezado(self):
        """Franja superior con el título 'Gestión de Libros'."""
        encabezado = ctk.CTkFrame(self, fg_color=estilos.COLOR_FONDO, corner_radius=0)
        encabezado.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(10, 5))

        ctk.CTkLabel(
            encabezado,
            text="Gestión de Libros",
            font=estilos.FUENTE_TITULO,
            text_color=estilos.COLOR_TEXTO,
        ).pack(pady=5)

    def _crear_panel_izquierdo(self):
        """Barra de búsqueda + formulario + botones."""
        panel = ctk.CTkFrame(self, fg_color=estilos.COLOR_PANEL, corner_radius=estilos.RADIO_BORDE)
        panel.grid(row=1, column=0, sticky="nsew", padx=(20, 10), pady=(0, 20))

        # ---------- Barra de búsqueda ----------
        barra = ctk.CTkFrame(panel, fg_color=estilos.COLOR_BARRA, corner_radius=estilos.RADIO_BORDE)
        barra.pack(fill="x", padx=15, pady=(15, 20))

        ctk.CTkLabel(
            barra, text="ISBN", font=estilos.FUENTE_SUBTITULO, text_color=estilos.COLOR_TEXTO
        ).pack(side="left", padx=(15, 8), pady=10)

        self.entrada_buscar = self._nueva_caja(barra, ancho=170)
        self.entrada_buscar.pack(side="left", pady=10)
        # Presionar Enter en la caja también busca
        self.entrada_buscar.bind("<Return>", lambda evento: self._al_buscar())

        ctk.CTkButton(
            barra,
            text="Buscar",
            width=80,
            height=estilos.ALTO_CAMPO,
            corner_radius=estilos.RADIO_BORDE,
            font=estilos.FUENTE_BOTON,
            fg_color=estilos.COLOR_BOTON_BUSCAR,
            hover_color=estilos.COLOR_BOTON_BUSCAR_HOVER,
            text_color=estilos.COLOR_TEXTO,
            command=self._al_buscar,
        ).pack(side="left", padx=10, pady=10)

        # ---------- Formulario ----------
        formulario = ctk.CTkFrame(panel, fg_color="transparent")
        formulario.pack(padx=20, pady=5)

        filas = [
            ("isbn", "ISBN:", "caja"),
            ("titulo", "Título:", "caja"),
            ("autor", "Autor:", "lista"),
            ("editorial", "Editorial:", "lista"),
            ("categoria", "Categoría:", "caja"),
            ("anio", "Año:", "caja"),
            ("existencias", "Existencias:", "caja"),
        ]

        for numero_fila, (clave, texto, tipo) in enumerate(filas):
            ctk.CTkLabel(
                formulario, text=texto, font=estilos.FUENTE_ETIQUETA, text_color=estilos.COLOR_TEXTO
            ).grid(row=numero_fila, column=0, sticky="e", padx=(0, 12), pady=6)

            if tipo == "caja":
                widget = self._nueva_caja(formulario)
            else:
                widget = self._nueva_lista(formulario)

            widget.grid(row=numero_fila, column=1, pady=6)
            self.campos[clave] = widget

        # ---------- Botones ----------
        botones = ctk.CTkFrame(panel, fg_color="transparent")
        botones.pack(pady=(20, 15))

        self._nuevo_boton(
            botones, "Guardar", estilos.COLOR_BOTON_PRINCIPAL,
            estilos.COLOR_BOTON_PRINCIPAL_HOVER, self._al_guardar,
        ).grid(row=0, column=0, padx=5)

        self._nuevo_boton(
            botones, "Eliminar", estilos.COLOR_BOTON_PELIGRO,
            estilos.COLOR_BOTON_PELIGRO_HOVER, self._al_eliminar,
        ).grid(row=0, column=1, padx=5)

        self._nuevo_boton(
            botones, "Limpiar", estilos.COLOR_BOTON_SECUNDARIO,
            estilos.COLOR_BOTON_SECUNDARIO_HOVER, self.limpiar,
        ).grid(row=0, column=2, padx=5)

    def _crear_tabla(self):
        """Tabla (Treeview) con los libros registrados."""
        contenedor = ctk.CTkFrame(self, fg_color=estilos.COLOR_PANEL, corner_radius=estilos.RADIO_BORDE)
        contenedor.grid(row=1, column=1, sticky="nsew", padx=(10, 20), pady=(0, 20))

        # CustomTkinter no trae tabla, así que se usa el Treeview de tkinter
        # y se le cambian los colores con un "Style".
        estilo = ttk.Style()
        estilo.theme_use("clam")  # Este tema sí permite cambiar el color de los encabezados
        estilo.configure(
            "Libros.Treeview",
            background=estilos.COLOR_TABLA_FONDO,
            fieldbackground=estilos.COLOR_TABLA_FONDO,
            foreground=estilos.COLOR_TEXTO,
            font=estilos.FUENTE_TABLA,
            rowheight=30,
            borderwidth=0,
            bordercolor=estilos.COLOR_PANEL,
            lightcolor=estilos.COLOR_PANEL,
            darkcolor=estilos.COLOR_PANEL,
        )
        # Quita el marco gris que el tema "clam" le pone a la tabla
        estilo.layout("Libros.Treeview", [("Treeview.treearea", {"sticky": "nswe"})])
        estilo.configure(
            "Libros.Treeview.Heading",
            background=estilos.COLOR_TABLA_ENCABEZADO,
            foreground=estilos.COLOR_TEXTO,
            font=estilos.FUENTE_TABLA_ENCABEZADO,
            relief="flat",
            bordercolor=estilos.COLOR_TABLA_ENCABEZADO,
            lightcolor=estilos.COLOR_TABLA_ENCABEZADO,
            darkcolor=estilos.COLOR_TABLA_ENCABEZADO,
        )
        estilo.map(
            "Libros.Treeview",
            background=[("selected", estilos.COLOR_TABLA_SELECCION)],
            foreground=[("selected", estilos.COLOR_TEXTO)],
        )
        estilo.map("Libros.Treeview.Heading", background=[("active", estilos.COLOR_BOTON_SECUNDARIO_HOVER)])

        claves = [clave for clave, _, _ in self.COLUMNAS]
        self.tabla = ttk.Treeview(
            contenedor, columns=claves, show="headings", style="Libros.Treeview", selectmode="browse"
        )
        for clave, encabezado, ancho in self.COLUMNAS:
            self.tabla.heading(clave, text=encabezado)
            self.tabla.column(clave, width=ancho, minwidth=40, anchor="center", stretch=True)

        # Filas de dos tonos (tipo cebra) para que se lea más fácil
        self.tabla.tag_configure("par", background=estilos.COLOR_TABLA_FONDO)
        self.tabla.tag_configure("impar", background=estilos.COLOR_PANEL)

        barra_scroll = ctk.CTkScrollbar(
            contenedor,
            command=self.tabla.yview,
            button_color=estilos.COLOR_CAMPO,
            button_hover_color=estilos.COLOR_BOTON_SECUNDARIO_HOVER,
        )
        self.tabla.configure(yscrollcommand=barra_scroll.set)

        barra_scroll.pack(side="right", fill="y", padx=(0, 8), pady=12)
        self.tabla.pack(side="left", fill="both", expand=True, padx=(12, 0), pady=12)

        # Al hacer clic en una fila, sus datos pasan al formulario
        self.tabla.bind("<<TreeviewSelect>>", self._al_seleccionar_fila)

    # ---------- Pequeñas "fábricas" para no repetir código ----------

    def _nueva_caja(self, padre, ancho=estilos.ANCHO_CAMPO):
        return ctk.CTkEntry(
            padre,
            width=ancho,
            height=estilos.ALTO_CAMPO,
            corner_radius=estilos.RADIO_BORDE,
            font=estilos.FUENTE_CAMPO,
            fg_color=estilos.COLOR_CAMPO,
            border_color=estilos.COLOR_CAMPO_BORDE,
            text_color=estilos.COLOR_CAMPO_TEXTO,
        )

    def _nueva_lista(self, padre):
        lista = ctk.CTkComboBox(
            padre,
            values=[],
            state="readonly",  # El usuario escoge, no escribe
            width=estilos.ANCHO_CAMPO,
            height=estilos.ALTO_CAMPO,
            corner_radius=estilos.RADIO_BORDE,
            font=estilos.FUENTE_CAMPO,
            dropdown_font=estilos.FUENTE_CAMPO,
            fg_color=estilos.COLOR_CAMPO,
            border_color=estilos.COLOR_CAMPO_BORDE,
            button_color=estilos.COLOR_CAMPO,
            button_hover_color=estilos.COLOR_BOTON_SECUNDARIO_HOVER,
            text_color=estilos.COLOR_CAMPO_TEXTO,
            dropdown_fg_color=estilos.COLOR_PANEL,
            dropdown_text_color=estilos.COLOR_TEXTO,
            dropdown_hover_color=estilos.COLOR_TABLA_SELECCION,
        )
        lista.set("")
        return lista

    def _nuevo_boton(self, padre, texto, color, color_hover, accion):
        return ctk.CTkButton(
            padre,
            text=texto,
            width=100,
            height=36,
            corner_radius=estilos.RADIO_BORDE,
            font=estilos.FUENTE_BOTON,
            fg_color=color,
            hover_color=color_hover,
            text_color=estilos.COLOR_TEXTO_BOTON,
            command=accion,
        )

    # =====================================================
    # MÉTODOS QUE USA EL CONTROLADOR
    # =====================================================

    def set_controlador(self, controlador):
        self.controlador = controlador

    def cargar_listas(self, autores, editoriales):
        """
        Llena las listas desplegables.
        autores y editoriales son listas de tuplas (id, nombre).
        Ejemplo: [(1, "Gabriel García Márquez"), (2, "Julio Cortázar")]
        """
        self._autores = {f"{id_} - {nombre}": id_ for id_, nombre in autores}
        self._editoriales = {f"{id_} - {nombre}": id_ for id_, nombre in editoriales}
        self.campos["autor"].configure(values=list(self._autores.keys()))
        self.campos["editorial"].configure(values=list(self._editoriales.keys()))

    def cargar_tabla(self, libros):
        """
        Muestra los libros en la tabla.
        libros es una lista de diccionarios con las claves de COLUMNAS.
        """
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        for numero, libro in enumerate(libros):
            valores = [libro.get(clave, "") for clave, _, _ in self.COLUMNAS]
            tono = "par" if numero % 2 == 0 else "impar"
            # iid=ISBN: así la fila se identifica por su ISBN (texto), no por un número
            self.tabla.insert("", tk.END, iid=str(libro["ISBN"]), values=valores, tags=(tono,))

    def obtener_datos(self):
        """Devuelve lo que hay en el formulario como un diccionario."""
        return {
            "ISBN": self.campos["isbn"].get().strip(),
            "Titulo": self.campos["titulo"].get().strip(),
            "IdAutor": self._autores.get(self.campos["autor"].get()),
            "IdEditorial": self._editoriales.get(self.campos["editorial"].get()),
            "Categoria": self.campos["categoria"].get().strip(),
            "Anio": self.campos["anio"].get().strip(),
            "Existencias": self.campos["existencias"].get().strip(),
        }

    def llenar_formulario(self, libro):
        """Pone los datos de un libro en el formulario (por ejemplo al buscar)."""
        self._vaciar_campos()
        self._escribir(self.campos["isbn"], libro.get("ISBN", ""))
        self._escribir(self.campos["titulo"], libro.get("Titulo", ""))
        self._escribir(self.campos["categoria"], libro.get("Categoria", ""))
        self._escribir(self.campos["anio"], libro.get("Anio", ""))
        self._escribir(self.campos["existencias"], libro.get("Existencias", ""))
        self.campos["autor"].set(self._buscar_texto(self._autores, libro.get("IdAutor"), libro.get("Autor")))
        self.campos["editorial"].set(
            self._buscar_texto(self._editoriales, libro.get("IdEditorial"), libro.get("Editorial"))
        )

    def limpiar(self):
        """Deja el formulario vacío y quita la selección de la tabla (botón Limpiar)."""
        self._vaciar_campos()
        self.entrada_buscar.delete(0, tk.END)
        if self.tabla.selection():
            self.tabla.selection_remove(self.tabla.selection())

    def mostrar_mensaje(self, texto):
        messagebox.showinfo("Biblioteca", texto)

    def mostrar_error(self, texto):
        messagebox.showerror("Error", texto)

    def confirmar(self, texto):
        return messagebox.askyesno("Confirmar", texto)

    # =====================================================
    # EVENTOS (lo que pasa al presionar botones)
    # =====================================================

    def _al_guardar(self):
        if self._hay_controlador():
            self.controlador.guardar_libro(self.obtener_datos())

    def _al_eliminar(self):
        isbn = self.campos["isbn"].get().strip()
        if not isbn:
            self.mostrar_error("Selecciona un libro de la tabla o escribe su ISBN.")
            return
        if self._hay_controlador() and self.confirmar(f"¿Eliminar el libro con ISBN {isbn}?"):
            self.controlador.eliminar_libro(isbn)

    def _al_buscar(self):
        isbn = self.entrada_buscar.get().strip()
        if not isbn:
            self.mostrar_error("Escribe un ISBN para buscar.")
            return
        if self._hay_controlador():
            self.controlador.buscar_libro(isbn)

    def _al_seleccionar_fila(self, evento):
        seleccion = self.tabla.selection()
        if not seleccion:
            return
        valores = self.tabla.item(seleccion[0], "values")
        libro = {clave: valores[i] for i, (clave, _, _) in enumerate(self.COLUMNAS)}
        libro["ISBN"] = seleccion[0]  # El iid guarda el ISBN como texto exacto
        self.llenar_formulario(libro)

    # ---------- Ayudantes internos ----------

    def _vaciar_campos(self):
        for widget in self.campos.values():
            if isinstance(widget, ctk.CTkComboBox):
                widget.set("")
            else:
                widget.delete(0, tk.END)

    def _hay_controlador(self):
        if self.controlador is None:
            self.mostrar_error("La vista no tiene controlador conectado.")
            return False
        return True

    @staticmethod
    def _escribir(caja, valor):
        caja.delete(0, tk.END)
        caja.insert(0, "" if valor is None else str(valor))

    @staticmethod
    def _buscar_texto(diccionario, id_buscado, nombre=None):
        """Encuentra el texto de la lista a partir del id o del nombre."""
        for texto, id_ in diccionario.items():
            if id_buscado is not None and str(id_) == str(id_buscado):
                return texto
            if nombre and texto.endswith(f" - {nombre}"):
                return texto
        return ""


# =====================================================
# PRUEBA: ejecutar este archivo solo, con datos de ejemplo
# =====================================================
if __name__ == "__main__":

    from datos.conexion import RUTA_BD, conexion

    def leer_base_de_datos():
        """
        Lee autores, editoriales y libros de AcaBiblioteca.db (SOLO lectura).
        Si el archivo .db no existe, devuelve listas vacías: no se crea uno vacío.
        """
        if not RUTA_BD.exists():
            print(f"Aviso: no existe {RUTA_BD}. La tabla se muestra vacía.")
            return [], [], []
        with conexion() as conn:
            autores = [(f["IdAutor"], f["NombreCompleto"]) for f in conn.execute(
                "SELECT IdAutor, Nombre || ' ' || Apellido AS NombreCompleto FROM Autores ORDER BY IdAutor")]
            editoriales = [(f["Ideditorial"], f["Nombre"]) for f in conn.execute(
                "SELECT Ideditorial, Nombre FROM Editoriales ORDER BY Ideditorial")]
            # Los alias (AS ...) dejan las columnas con los nombres que usa la vista
            libros = [dict(f) for f in conn.execute(
                """SELECT l.ISBN, l.Titulo, l.IdAutor, l.IdEditorial, l.Categoria,
                          IFNULL(l."Año", '') AS Anio, l.Existencias,
                          a.Nombre || ' ' || a.Apellido AS Autor, e.Nombre AS Editorial
                   FROM Libros l
                   JOIN Autores a ON a.IdAutor = l.IdAutor
                   JOIN Editoriales e ON e.Ideditorial = l.IdEditorial
                   ORDER BY l.Titulo""")]
        return autores, editoriales, libros

    class ControladorDePrueba:
        """
        Controlador de prueba: muestra lo que hay en la base de datos.
        Guardar y Eliminar solo cambian la lista en memoria (NO escriben en la BD);
        eso lo hará el controlador real del módulo de Libros.
        """

        def __init__(self, vista):
            self.vista = vista
            self.autores, self.editoriales, self.libros = leer_base_de_datos()
            self.vista.cargar_listas(self.autores, self.editoriales)
            self.refrescar()

        def refrescar(self):
            nombres_autor = dict(self.autores)
            nombres_editorial = dict(self.editoriales)
            filas = []
            for libro in self.libros:
                fila = dict(libro)
                fila["Autor"] = nombres_autor.get(libro["IdAutor"], "")
                fila["Editorial"] = nombres_editorial.get(libro["IdEditorial"], "")
                filas.append(fila)
            self.vista.cargar_tabla(filas)

        def guardar_libro(self, datos):
            if not datos["ISBN"] or not datos["Titulo"] or datos["IdAutor"] is None or datos["IdEditorial"] is None:
                self.vista.mostrar_error("ISBN, título, autor y editorial son obligatorios.")
                return
            self.libros = [l for l in self.libros if l["ISBN"] != datos["ISBN"]]
            self.libros.append(datos)
            self.refrescar()
            self.vista.limpiar()
            self.vista.mostrar_mensaje("Libro guardado (solo en memoria, es una prueba).")

        def eliminar_libro(self, isbn):
            self.libros = [l for l in self.libros if l["ISBN"] != isbn]
            self.refrescar()
            self.vista.limpiar()

        def buscar_libro(self, isbn):
            for libro in self.libros:
                if libro["ISBN"] == isbn:
                    self.vista.llenar_formulario(libro)
                    return
            self.vista.mostrar_error(f"No existe un libro con ISBN {isbn}.")

    ctk.set_appearance_mode("light")
    ventana = ctk.CTk()
    ventana.title("Tech Aca - Gestión de Libros")
    ventana.geometry("1320x640")
    ventana.configure(fg_color=estilos.COLOR_FONDO)

    vista = VistaLibros(ventana)
    vista.pack(fill="both", expand=True)
    vista.set_controlador(ControladorDePrueba(vista))

    ventana.mainloop()