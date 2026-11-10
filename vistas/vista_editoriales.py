import tkinter as tk
from tkinter import ttk, messagebox

from pathlib import Path

import customtkinter as ctk
from PIL import Image

from modelos.editorial import Editorial
from utils import estilos


# Ruta del logo: carpeta recursos/ en la raíz del proyecto
RUTA_LOGO = Path(__file__).resolve().parent.parent / "recursos" / "logo.png"


class VistaEditoriales(ctk.CTkFrame):
    """
    Pantalla de Gestión de Editoriales.

    Utiliza ControladorEditoriales:
      - guardar
      - eliminar
      - obtener_uno
      - obtener_todo
    """

    COLUMNAS = [
        ("IdEditorial", "ID", 90),
        ("Nombre", "Nombre de la editorial", 250),
    ]

    def __init__(self, master, controlador_editoriales=None):
        super().__init__(master, fg_color=estilos.COLOR_FONDO, corner_radius=0)

        self.controlador_editoriales = controlador_editoriales
        self.campos = {}

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._crear_encabezado()
        self._crear_panel_izquierdo()
        self._crear_tabla()

        if self.controlador_editoriales is not None:
            self.refrescar()

    # =====================================================
    # CONSTRUCCIÓN DE LA PANTALLA
    # =====================================================

    def _crear_encabezado(self):
        """Franja superior con el logo y el título."""

        encabezado = ctk.CTkFrame(
            self,
            fg_color=estilos.COLOR_FONDO,
            corner_radius=0
        )

        encabezado.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=(10, 5)
        )

        if RUTA_LOGO.exists():
            imagen = Image.open(RUTA_LOGO)
            alto = 90
            ancho = round(imagen.width * alto / imagen.height)

            self._logo = ctk.CTkImage(
                light_image=imagen,
                size=(ancho, alto)
            )

            ctk.CTkLabel(
                encabezado,
                image=self._logo,
                text=""
            ).pack(side="left", padx=(20, 15))

        ctk.CTkLabel(
            encabezado,
            text="Gestión de Editoriales",
            font=estilos.FUENTE_TITULO,
            text_color=estilos.COLOR_TEXTO,
        ).pack(side="left", pady=5)

    def _crear_panel_izquierdo(self):
        """Barra de búsqueda, formulario y botones."""

        panel = ctk.CTkFrame(
            self,
            fg_color=estilos.COLOR_PANEL,
            corner_radius=estilos.RADIO_BORDE
        )

        panel.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=(20, 10),
            pady=(0, 20)
        )

        # ---------- Barra de búsqueda ----------

        barra = ctk.CTkFrame(
            panel,
            fg_color=estilos.COLOR_BARRA,
            corner_radius=estilos.RADIO_BORDE
        )

        barra.pack(fill="x", padx=15, pady=(15, 20))

        ctk.CTkLabel(
            barra,
            text="ID Editorial",
            font=estilos.FUENTE_SUBTITULO,
            text_color=estilos.COLOR_TEXTO
        ).pack(side="left", padx=(15, 8), pady=10)

        self.entrada_buscar = self._nueva_caja(barra, ancho=100)
        self.entrada_buscar.pack(side="left", pady=10)

        self.entrada_buscar.bind(
            "<Return>",
            lambda evento: self._al_buscar()
        )

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

        formulario = ctk.CTkFrame(
            panel,
            fg_color="transparent"
        )

        formulario.pack(padx=20, pady=5)

        filas = [
            ("nombre", "Nombre:"),
        ]

        for numero_fila, (clave, texto) in enumerate(filas):

            ctk.CTkLabel(
                formulario,
                text=texto,
                font=estilos.FUENTE_ETIQUETA,
                text_color=estilos.COLOR_TEXTO
            ).grid(
                row=numero_fila,
                column=0,
                sticky="e",
                padx=(0, 12),
                pady=6
            )

            widget = self._nueva_caja(formulario)
            widget.grid(row=numero_fila, column=1, pady=6)

            self.campos[clave] = widget

        # ---------- Botones ----------

        botones = ctk.CTkFrame(
            panel,
            fg_color="transparent"
        )

        botones.pack(pady=(20, 15))

        self._nuevo_boton(
            botones,
            "Guardar",
            estilos.COLOR_BOTON_PRINCIPAL,
            estilos.COLOR_BOTON_PRINCIPAL_HOVER,
            self._al_guardar,
        ).grid(row=0, column=0, padx=4)

        self._nuevo_boton(
            botones,
            "Eliminar",
            estilos.COLOR_BOTON_PELIGRO,
            estilos.COLOR_BOTON_PELIGRO_HOVER,
            self._al_eliminar,
        ).grid(row=0, column=1, padx=4)

        self._nuevo_boton(
            botones,
            "Limpiar",
            estilos.COLOR_BOTON_SECUNDARIO,
            estilos.COLOR_BOTON_SECUNDARIO_HOVER,
            self.limpiar,
        ).grid(row=1, column=0, padx=4, pady=6)

    def _crear_tabla(self):
        """Tabla Treeview con las editoriales registradas."""

        contenedor = ctk.CTkFrame(
            self,
            fg_color=estilos.COLOR_PANEL,
            corner_radius=estilos.RADIO_BORDE
        )

        contenedor.grid(
            row=1,
            column=1,
            sticky="nsew",
            padx=(10, 20),
            pady=(0, 20)
        )

        estilo = ttk.Style()
        estilo.theme_use("clam")

        estilo.configure(
            "Editoriales.Treeview",
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

        estilo.layout(
            "Editoriales.Treeview",
            [("Treeview.treearea", {"sticky": "nswe"})]
        )

        estilo.configure(
            "Editoriales.Treeview.Heading",
            background=estilos.COLOR_TABLA_ENCABEZADO,
            foreground=estilos.COLOR_TEXTO,
            font=estilos.FUENTE_TABLA_ENCABEZADO,
            relief="flat",
            bordercolor=estilos.COLOR_TABLA_ENCABEZADO,
            lightcolor=estilos.COLOR_TABLA_ENCABEZADO,
            darkcolor=estilos.COLOR_TABLA_ENCABEZADO,
        )

        estilo.map(
            "Editoriales.Treeview",
            background=[("selected", estilos.COLOR_TABLA_SELECCION)],
            foreground=[("selected", estilos.COLOR_TEXTO)],
        )

        estilo.map(
            "Editoriales.Treeview.Heading",
            background=[
                ("active", estilos.COLOR_BOTON_SECUNDARIO_HOVER)
            ]
        )

        claves = [clave for clave, _, _ in self.COLUMNAS]

        self.tabla = ttk.Treeview(
            contenedor,
            columns=claves,
            show="headings",
            style="Editoriales.Treeview",
            selectmode="browse"
        )

        for clave, encabezado, ancho in self.COLUMNAS:
            self.tabla.heading(clave, text=encabezado)
            self.tabla.column(
                clave,
                width=ancho,
                minwidth=40,
                anchor="center",
                stretch=True
            )

        # Filas de dos tonos

        self.tabla.tag_configure(
            "par",
            background=estilos.COLOR_TABLA_FONDO
        )

        self.tabla.tag_configure(
            "impar",
            background=estilos.COLOR_PANEL
        )

        barra_scroll = ctk.CTkScrollbar(
            contenedor,
            command=self.tabla.yview,
            button_color=estilos.COLOR_CAMPO,
            button_hover_color=estilos.COLOR_BOTON_SECUNDARIO_HOVER,
        )

        self.tabla.configure(
            yscrollcommand=barra_scroll.set
        )

        barra_scroll.pack(
            side="right",
            fill="y",
            padx=(0, 8),
            pady=12
        )

        self.tabla.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(12, 0),
            pady=12
        )

        self.tabla.bind(
            "<<TreeviewSelect>>",
            self._al_seleccionar_fila
        )

    # =====================================================
    # FÁBRICAS DE COMPONENTES
    # =====================================================

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

    def _nuevo_boton(self, padre, texto, color, color_hover, accion):

        return ctk.CTkButton(
            padre,
            text=texto,
            width=85,
            height=36,
            corner_radius=estilos.RADIO_BORDE,
            font=estilos.FUENTE_BOTON,
            fg_color=color,
            hover_color=color_hover,
            text_color=estilos.COLOR_TEXTO_BOTON,
            command=accion,
        )

    # =====================================================
    # CONEXIÓN CON EL CONTROLADOR
    # =====================================================

    def conectar(self, controlador_editoriales):
        """Conecta el controlador y carga las editoriales."""

        self.controlador_editoriales = controlador_editoriales
        self.refrescar()

    def refrescar(self):
        """Vuelve a leer las editoriales desde la base de datos."""

        editoriales = self._llamar(
            self.controlador_editoriales.obtener_todo
        ) or []

        self.cargar_tabla(editoriales)

    # =====================================================
    # MÉTODOS PARA MOSTRAR DATOS
    # =====================================================

    def cargar_tabla(self, editoriales):
        """Muestra las editoriales en la tabla."""

        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        for numero, editorial in enumerate(editoriales):

            datos = editorial.a_diccionario()

            valores = [
                datos.get(clave, "")
                for clave, _, _ in self.COLUMNAS
            ]

            tono = "par" if numero % 2 == 0 else "impar"

            self.tabla.insert(
                "",
                tk.END,
                iid=str(datos["IdEditorial"]),
                values=valores,
                tags=(tono,)
            )

    def obtener_datos(self):
        """Devuelve los datos del formulario."""

        return {
            "Nombre": self.campos["nombre"].get().strip()
        }

    def llenar_formulario(self, editorial):
        """Pone los datos de una editorial en el formulario."""

        self._vaciar_campos()

        self._escribir(
            self.campos["nombre"],
            editorial.get("Nombre", "")
        )

    def limpiar(self):
        """Vacía el formulario y quita la selección de la tabla."""

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
    # EVENTOS
    # =====================================================

    def _al_guardar(self):
        """Registra una editorial nueva."""

        if not self._hay_controlador():
            return

        try:
            editorial = Editorial.desde_formulario(
                self.obtener_datos()
            )

        except ValueError as error:
            self.mostrar_error(str(error))
            return

        guardado = self._llamar(
            self.controlador_editoriales.guardar,
            editorial
        )

        if guardado is True:
            self.refrescar()
            self.limpiar()
            self.mostrar_mensaje("Editorial guardada correctamente.")

        elif guardado is False:
            self.mostrar_error(
                "No se pudo guardar la editorial. "
                "Revisa los datos e inténtalo de nuevo."
            )

    def _al_eliminar(self):
        """Elimina la editorial seleccionada."""

        if not self._hay_controlador():
            return

        seleccion = self.tabla.selection()

        if not seleccion:
            self.mostrar_error(
                "Selecciona una editorial de la tabla."
            )
            return

        id_editorial = seleccion[0]

        if self._llamar(
            self.controlador_editoriales.obtener_uno,
            "IdEditorial",
            id_editorial
        ) is None:

            self.mostrar_error(
                f"No existe una editorial con ID {id_editorial}."
            )
            return

        if not self.confirmar(
            f"¿Eliminar la editorial con ID {id_editorial}?"
        ):
            return

        resultado = self._llamar(
            self.controlador_editoriales.eliminar,
            id_editorial
        )

        if resultado:
            self.refrescar()
            self.limpiar()
            self.mostrar_mensaje("Editorial eliminada correctamente.")

        else:
            self.mostrar_error(
                "No se pudo eliminar la editorial. "
                "Puede que tenga libros asociados."
            )

    def _al_buscar(self):
        """Busca una editorial por su ID."""

        if not self._hay_controlador():
            return

        texto = self.entrada_buscar.get().strip()

        if not texto:
            self.mostrar_error(
                "Escribe el ID de una editorial para buscar."
            )
            return

        try:
            codigo = int(texto)

            if codigo <= 0:
                raise ValueError

        except ValueError:
            self.mostrar_error(
                "El ID debe ser un número entero positivo."
            )
            return

        editorial = self._llamar(
            self.controlador_editoriales.obtener_uno,
            "IdEditorial",
            codigo
        )

        if editorial is None:
            self.mostrar_error(
                f"No existe una editorial con ID {codigo}."
            )
            return

        self.llenar_formulario(editorial.a_diccionario())

        if self.tabla.exists(str(codigo)):
            self.tabla.selection_set(str(codigo))
            self.tabla.see(str(codigo))

    def _al_seleccionar_fila(self, evento):
        """Carga en el formulario la editorial seleccionada."""

        seleccion = self.tabla.selection()

        if not seleccion:
            return

        valores = self.tabla.item(
            seleccion[0],
            "values"
        )

        editorial = {
            clave: valores[i]
            for i, (clave, _, _) in enumerate(self.COLUMNAS)
        }

        editorial["IdEditorial"] = seleccion[0]

        self.llenar_formulario(editorial)

    # =====================================================
    # AYUDANTES INTERNOS
    # =====================================================

    def _llamar(self, funcion, *argumentos):
        """
        Llama a un método del controlador.
        Si ocurre un error, muestra un mensaje y devuelve None.
        """

        try:
            return funcion(*argumentos)

        except Exception as error:
            self.mostrar_error(
                f"Ocurrió un error con la base de datos:\n{error}"
            )
            return None

    def _vaciar_campos(self):
        for widget in self.campos.values():
            widget.delete(0, tk.END)

    def _hay_controlador(self):

        if self.controlador_editoriales is None:
            self.mostrar_error(
                "La vista no tiene controlador conectado."
            )
            return False

        return True

    @staticmethod
    def _escribir(caja, valor):
        caja.delete(0, tk.END)
        caja.insert(
            0,
            "" if valor is None else str(valor)
        )


# =====================================================
# PRUEBA: abrir solo esta ventana
# Desde la raíz del proyecto:
# py -m vistas.vista_editoriales
# =====================================================

if __name__ == "__main__":
    from datos.conexion import RUTA_BD

    ctk.set_appearance_mode("light")

    ventana = ctk.CTk()
    ventana.title("Tech Aca - Gestión de Editoriales")
    ventana.geometry("1000x640")
    ventana.configure(fg_color=estilos.COLOR_FONDO)

    vista = VistaEditoriales(ventana)
    vista.pack(fill="both", expand=True)

    if RUTA_BD.exists():
        from controladores.controladores import ControladorEditoriales
        from datos.gestor_sql import GestorSQL
        from servicios.service import Service

        servicio = Service(GestorSQL())

        vista.conectar(
            ControladorEditoriales(servicio)
        )

    else:
        print(
            f"Aviso: no existe {RUTA_BD}. "
            "Crea la base desde database/schema_y_datos.sql."
        )

    ventana.mainloop()
