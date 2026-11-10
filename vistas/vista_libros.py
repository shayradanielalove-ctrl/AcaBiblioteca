import tkinter as tk
from tkinter import ttk, messagebox

from pathlib import Path

import customtkinter as ctk
from PIL import Image

from modelos.libro import Libro
from utils import estilos

# Ruta del logo: carpeta recursos/ en la raíz del proyecto
RUTA_LOGO = Path(__file__).resolve().parent.parent / "recursos" / "logo.png"


class VistaLibros(ctk.CTkFrame):
    """
    Pantalla de Gestión de Libros (formulario a la izquierda, tabla a la derecha).

    Usa los controladores del grupo (controladores/controladores.py):
      - ControladorLibros: guardar, actualizar, eliminar, obtener_uno, obtener_todo
      - ControladorAutores y ControladorEditoriales: obtener_todo (para las listas)
    """

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

    def __init__(self, master, controlador_libros=None, controlador_autores=None, controlador_editoriales=None):
        super().__init__(master, fg_color=estilos.COLOR_FONDO, corner_radius=0)
        self.controlador_libros = controlador_libros
        self.controlador_autores = controlador_autores
        self.controlador_editoriales = controlador_editoriales

        # Diccionarios para traducir el texto de las listas a su Id
        # Ejemplo: {"1 - Gabriel García Márquez": 1}
        self._autores = {}
        self._editoriales = {}

        self.campos = {}  # Aquí se guardan las cajas del formulario
        self.id_actual = None  # ISBN del libro que se está editando

        # La columna 1 (la tabla) crece si se agranda la ventana
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._crear_encabezado()
        self._crear_panel_izquierdo()
        self._crear_tabla()

        # Si ya llegaron los controladores, se cargan los datos de la base
        if self.controlador_libros is not None:
            self.refrescar()

    # =====================================================
    # CONSTRUCCIÓN DE LA PANTALLA
    # =====================================================

    def _crear_encabezado(self):
        """Franja superior con el logo de Tech Aca y el título 'Gestión de Libros'."""
        encabezado = ctk.CTkFrame(self, fg_color=estilos.COLOR_FONDO, corner_radius=0)
        encabezado.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(10, 5))

        # El logo está en recursos/logo.png (con fondo transparente).
        # Si no se encuentra, la pantalla se abre igual, solo sin logo.
        if RUTA_LOGO.exists():
            imagen = Image.open(RUTA_LOGO)
            alto = 90
            ancho = round(imagen.width * alto / imagen.height)
            self._logo = ctk.CTkImage(light_image=imagen, size=(ancho, alto))
            ctk.CTkLabel(encabezado, image=self._logo, text="").pack(side="left", padx=(20, 15))

        ctk.CTkLabel(
            encabezado,
            text="Gestión de Libros",
            font=estilos.FUENTE_TITULO,
            text_color=estilos.COLOR_TEXTO,
        ).pack(side="left", pady=5)

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
        ).grid(row=0, column=0, padx=5, pady=5)

        self._nuevo_boton(
            botones, "Actualizar", estilos.COLOR_BOTON_PRINCIPAL,
            estilos.COLOR_BOTON_PRINCIPAL_HOVER, self._al_actualizar,
        ).grid(row=0, column=1, padx=5, pady=5)

        self._nuevo_boton(
            botones, "Eliminar", estilos.COLOR_BOTON_PELIGRO,
            estilos.COLOR_BOTON_PELIGRO_HOVER, self._al_eliminar,
        ).grid(row=1, column=0, padx=5, pady=5)

        self._nuevo_boton(
            botones, "Limpiar", estilos.COLOR_BOTON_SECUNDARIO,
            estilos.COLOR_BOTON_SECUNDARIO_HOVER, self.limpiar,
        ).grid(row=1, column=1, padx=5, pady=5)

    def _crear_tabla(self):
        """Tabla (Treeview) con los libros registrados."""
        contenedor = ctk.CTkFrame(self, fg_color=estilos.COLOR_PANEL, corner_radius=estilos.RADIO_BORDE)
        contenedor.grid(row=1, column=1, sticky="nsew", padx=(10, 20), pady=(0, 20))

        estilo = ttk.Style()
        estilo.theme_use("clam")
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
            state="readonly",
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
    # CONEXIÓN CON LOS CONTROLADORES
    # =====================================================

    def conectar(self, controlador_libros, controlador_autores, controlador_editoriales):
        """Conecta los controladores después de crear la vista y carga los datos."""
        self.controlador_libros = controlador_libros
        self.controlador_autores = controlador_autores
        self.controlador_editoriales = controlador_editoriales
        self.refrescar()

    def refrescar(self):
        """Vuelve a leer autores, editoriales y libros desde la base y los muestra."""
        autores = self._llamar(self.controlador_autores.obtener_todo) or []
        editoriales = self._llamar(self.controlador_editoriales.obtener_todo) or []
        libros = self._llamar(self.controlador_libros.obtener_todo) or []

        opciones_autores = [autor.a_opcion() for autor in autores]
        opciones_editoriales = [editorial.a_opcion() for editorial in editoriales]
        self.cargar_listas(opciones_autores, opciones_editoriales)

        nombre_autor = dict(opciones_autores)
        nombre_editorial = dict(opciones_editoriales)
        filas = []
        for libro in sorted(libros, key=lambda l: l.titulo.lower()):
            fila = libro.a_diccionario()
            fila["Autor"] = fila["Autor"] or nombre_autor.get(libro.id_autor, "")
            fila["Editorial"] = fila["Editorial"] or nombre_editorial.get(libro.id_editorial, "")
            filas.append(fila)
        self.cargar_tabla(filas)

    # =====================================================
    # MÉTODOS PARA MOSTRAR DATOS
    # =====================================================

    def cargar_listas(self, autores, editoriales):
        """Llena las listas desplegables con tuplas (id, nombre)."""
        self._autores = {f"{id_} - {nombre}": id_ for id_, nombre in autores}
        self._editoriales = {f"{id_} - {nombre}": id_ for id_, nombre in editoriales}
        self.campos["autor"].configure(values=list(self._autores.keys()))
        self.campos["editorial"].configure(values=list(self._editoriales.keys()))

    def cargar_tabla(self, libros):
        """Muestra los libros en la tabla."""
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        for numero, libro in enumerate(libros):
            valores = [libro.get(clave, "") for clave, _, _ in self.COLUMNAS]
            tono = "par" if numero % 2 == 0 else "impar"
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
        """Pone los datos de un libro en el formulario."""
        self._vaciar_campos()

        self.id_actual = libro.get("ISBN")

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
        """Deja el formulario vacío y quita la selección de la tabla."""
        self._vaciar_campos()
        self.id_actual = None
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
    # EVENTOS
    # =====================================================

    def _al_guardar(self):
        if not self._hay_controlador():
            return

        # No se permite guardar si ya hay un libro seleccionado.
        if self.id_actual is not None:
            self.mostrar_error("Hay un libro seleccionado. Usa Actualizar o Limpiar antes de registrar otro.")
            return

        try:
            libro = Libro.desde_formulario(self.obtener_datos())
        except ValueError as error:
            self.mostrar_error(str(error))
            return

        # Guardar solo registra libros nuevos.
        existente = self._llamar(self.controlador_libros.obtener_uno, "ISBN", libro.isbn)
        if existente is not None:
            self.mostrar_error(f"Ya existe un libro con ISBN {libro.isbn}. Usa Actualizar si deseas modificarlo.")
            return

        guardado = self._llamar(self.controlador_libros.guardar, libro)

        if guardado is True:
            self.refrescar()
            self.limpiar()
            self.mostrar_mensaje("Libro guardado correctamente.")
        elif guardado is False:
            self.mostrar_error("No se pudo guardar el libro. Revisa los datos e inténtalo de nuevo.")

    def _al_actualizar(self):
        if not self._hay_controlador():
            return

        if self.id_actual is None:
            self.mostrar_error("Selecciona un libro de la tabla o búscalo por ISBN antes de actualizar.")
            return

        try:
            libro = Libro.desde_formulario(self.obtener_datos())
        except ValueError as error:
            self.mostrar_error(str(error))
            return

        if not self.confirmar(f"¿Actualizar los datos del libro con ISBN {self.id_actual}?"):
            return

        resultado = self._llamar(
            self.controlador_libros.actualizar,
            libro,
            self.id_actual,
        )

        if resultado is True:
            self.refrescar()
            self.limpiar()
            self.mostrar_mensaje("Libro actualizado correctamente.")
        elif resultado is False:
            self.mostrar_error("No se pudo actualizar el libro.")

    def _al_eliminar(self):
        if not self._hay_controlador():
            return

        isbn = self.campos["isbn"].get().strip().replace("-", "")
        if not isbn:
            self.mostrar_error("Selecciona un libro de la tabla o escribe su ISBN.")
            return

        if self._llamar(self.controlador_libros.obtener_uno, "ISBN", isbn) is None:
            self.mostrar_error(f"No existe un libro con ISBN {isbn}.")
            return

        if not self.confirmar(f"¿Eliminar el libro con ISBN {isbn}?"):
            return

        if self._llamar(self.controlador_libros.eliminar, isbn):
            self.refrescar()
            self.limpiar()
            self.mostrar_mensaje("Libro eliminado.")
        else:
            self.mostrar_error("No se pudo eliminar el libro. Puede que tenga préstamos registrados.")

    def _al_buscar(self):
        if not self._hay_controlador():
            return

        isbn = self.entrada_buscar.get().strip().replace("-", "")
        if not isbn:
            self.mostrar_error("Escribe un ISBN para buscar.")
            return

        libro = self._llamar(self.controlador_libros.obtener_uno, "ISBN", isbn)
        if libro is None:
            self.mostrar_error(f"No existe un libro con ISBN {isbn}.")
            return

        self.llenar_formulario(libro.a_diccionario())

    def _al_seleccionar_fila(self, evento):
        seleccion = self.tabla.selection()
        if not seleccion:
            return

        valores = self.tabla.item(seleccion[0], "values")
        libro = {clave: valores[i] for i, (clave, _, _) in enumerate(self.COLUMNAS)}
        libro["ISBN"] = seleccion[0]
        self.llenar_formulario(libro)

    # ---------- Ayudantes internos ----------

    def _llamar(self, funcion, *argumentos):
        """
        Llama a un método del controlador. Si ocurre un error inesperado
        (por ejemplo, la base de datos no responde), muestra un mensaje
        en vez de cerrar el programa, y devuelve None.
        """
        try:
            return funcion(*argumentos)
        except Exception as error:
            self.mostrar_error(f"Ocurrió un error con la base de datos:\n{error}")
            return None

    def _vaciar_campos(self):
        for widget in self.campos.values():
            if isinstance(widget, ctk.CTkComboBox):
                widget.set("")
            else:
                widget.delete(0, tk.END)

    def _hay_controlador(self):
        if self.controlador_libros is None:
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
# PRUEBA: abrir solo esta ventana, conectada a la base de datos real
# (desde la raíz del proyecto: py -m vistas.vista_libros)
# =====================================================
if __name__ == "__main__":
    from datos.conexion import RUTA_BD

    ctk.set_appearance_mode("light")
    ventana = ctk.CTk()
    ventana.title("Tech Aca - Gestión de Libros")
    ventana.geometry("1320x640")
    ventana.configure(fg_color=estilos.COLOR_FONDO)

    vista = VistaLibros(ventana)
    vista.pack(fill="both", expand=True)

    if RUTA_BD.exists():
        from controladores.controladores import ControladorAutores, ControladorEditoriales, ControladorLibros
        from datos.gestor_sql import GestorSQL
        from servicios.service import Service

        servicio = Service(GestorSQL())
        vista.conectar(
            ControladorLibros(servicio),
            ControladorAutores(servicio),
            ControladorEditoriales(servicio),
        )
    else:
        print(f"Aviso: no existe {RUTA_BD}. Crea la base desde database/schema_y_datos.sql.")

    ventana.mainloop()
