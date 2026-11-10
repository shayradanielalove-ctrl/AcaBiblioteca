import tkinter as tk
from tkinter import ttk, messagebox

from pathlib import Path

import customtkinter as ctk
from PIL import Image

from modelos.autor import Autor
from utils import estilos


# Ruta del logo
RUTA_LOGO = Path(__file__).resolve().parent.parent / "recursos" / "logo.png"


class VistaAutores(ctk.CTkFrame):
    """
    Pantalla de Gestión de Autores.

    Usa ControladorAutores:
      - guardar
      - actualizar
      - eliminar
      - obtener_uno
      - obtener_todo
    """

    COLUMNAS = [
        ("IdAutor", "ID", 80),
        ("Nombre", "Nombre", 180),
        ("Apellido", "Apellido", 180),
    ]

    def __init__(self, master, controlador_autores=None):
        super().__init__(
            master,
            fg_color=estilos.COLOR_FONDO,
            corner_radius=0
        )

        self.controlador_autores = controlador_autores
        self.id_actual = None
        self.campos = {}

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._crear_encabezado()
        self._crear_panel_izquierdo()
        self._crear_tabla()

        if self.controlador_autores is not None:
            self.refrescar()

    # =====================================================
    # CONSTRUCCIÓN DE LA PANTALLA
    # =====================================================

    def _crear_encabezado(self):
        """Encabezado con logo y título."""

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
            text="Gestión de Autores",
            font=estilos.FUENTE_TITULO,
            text_color=estilos.COLOR_TEXTO
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

        barra.pack(
            fill="x",
            padx=15,
            pady=(15, 20)
        )

        ctk.CTkLabel(
            barra,
            text="ID Autor",
            font=estilos.FUENTE_SUBTITULO,
            text_color=estilos.COLOR_TEXTO
        ).pack(
            side="left",
            padx=(15, 8),
            pady=10
        )

        self.entrada_buscar = self._nueva_caja(
            barra,
            ancho=100
        )

        self.entrada_buscar.pack(
            side="left",
            pady=10
        )

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
            command=self._al_buscar
        ).pack(
            side="left",
            padx=10,
            pady=10
        )

        # ---------- Formulario ----------

        formulario = ctk.CTkFrame(
            panel,
            fg_color="transparent"
        )

        formulario.pack(
            padx=20,
            pady=5
        )

        filas = [
            ("nombre", "Nombre:"),
            ("apellido", "Apellido:"),
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
                pady=10
            )

            widget = self._nueva_caja(formulario)

            widget.grid(
                row=numero_fila,
                column=1,
                pady=10
            )

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
            self._al_guardar
        ).grid(row=0, column=0, padx=4)

        self._nuevo_boton(
            botones,
            "Actualizar",
            estilos.COLOR_BOTON_PRINCIPAL,
            estilos.COLOR_BOTON_PRINCIPAL_HOVER,
            self._al_actualizar
        ).grid(row=0, column=1, padx=4)

        self._nuevo_boton(
            botones,
            "Eliminar",
            estilos.COLOR_BOTON_PELIGRO,
            estilos.COLOR_BOTON_PELIGRO_HOVER,
            self._al_eliminar
        ).grid(row=1, column=0, padx=4, pady=6)

        self._nuevo_boton(
            botones,
            "Limpiar",
            estilos.COLOR_BOTON_SECUNDARIO,
            estilos.COLOR_BOTON_SECUNDARIO_HOVER,
            self.limpiar
        ).grid(row=1, column=1, padx=4, pady=6)

    def _crear_tabla(self):
        """Tabla Treeview con los autores registrados."""

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
            "Autores.Treeview",
            background=estilos.COLOR_TABLA_FONDO,
            fieldbackground=estilos.COLOR_TABLA_FONDO,
            foreground=estilos.COLOR_TEXTO,
            font=estilos.FUENTE_TABLA,
            rowheight=30,
            borderwidth=0,
            bordercolor=estilos.COLOR_PANEL,
            lightcolor=estilos.COLOR_PANEL,
            darkcolor=estilos.COLOR_PANEL
        )

        estilo.layout(
            "Autores.Treeview",
            [("Treeview.treearea", {"sticky": "nswe"})]
        )

        estilo.configure(
            "Autores.Treeview.Heading",
            background=estilos.COLOR_TABLA_ENCABEZADO,
            foreground=estilos.COLOR_TEXTO,
            font=estilos.FUENTE_TABLA_ENCABEZADO,
            relief="flat",
            bordercolor=estilos.COLOR_TABLA_ENCABEZADO,
            lightcolor=estilos.COLOR_TABLA_ENCABEZADO,
            darkcolor=estilos.COLOR_TABLA_ENCABEZADO
        )

        estilo.map(
            "Autores.Treeview",
            background=[
                ("selected", estilos.COLOR_TABLA_SELECCION)
            ],
            foreground=[
                ("selected", estilos.COLOR_TEXTO)
            ]
        )

        estilo.map(
            "Autores.Treeview.Heading",
            background=[
                ("active", estilos.COLOR_BOTON_SECUNDARIO_HOVER)
            ]
        )

        claves = [
            clave for clave, _, _ in self.COLUMNAS
        ]

        self.tabla = ttk.Treeview(
            contenedor,
            columns=claves,
            show="headings",
            style="Autores.Treeview",
            selectmode="browse"
        )

        for clave, encabezado, ancho in self.COLUMNAS:

            self.tabla.heading(
                clave,
                text=encabezado
            )

            self.tabla.column(
                clave,
                width=ancho,
                minwidth=40,
                anchor="center",
                stretch=True
            )

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
            button_hover_color=estilos.COLOR_BOTON_SECUNDARIO_HOVER
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
    # FÁBRICAS DE WIDGETS
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
            text_color=estilos.COLOR_CAMPO_TEXTO
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
            command=accion
        )

    # =====================================================
    # CONEXIÓN CON EL CONTROLADOR
    # =====================================================

    def conectar(self, controlador_autores):
        """Conecta el controlador y carga los autores."""

        self.controlador_autores = controlador_autores
        self.refrescar()

    def refrescar(self):
        """Obtiene los autores y actualiza la tabla."""

        autores = self._llamar(
            self.controlador_autores.obtener_todo
        ) or []

        filas = [
            autor.a_diccionario()
            for autor in autores
        ]

        self.cargar_tabla(filas)

    # =====================================================
    # MÉTODOS PARA MOSTRAR DATOS
    # =====================================================

    def cargar_tabla(self, autores):
        """Muestra los autores en el Treeview."""

        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        for numero, autor in enumerate(autores):

            valores = [
                autor.get(clave, "")
                for clave, _, _ in self.COLUMNAS
            ]

            tono = "par" if numero % 2 == 0 else "impar"

            self.tabla.insert(
                "",
                tk.END,
                iid=str(autor["IdAutor"]),
                values=valores,
                tags=(tono,)
            )

    def obtener_datos(self):
        """Obtiene los datos del formulario."""

        return {
            "nombre": self.campos["nombre"].get().strip(),
            "apellido": self.campos["apellido"].get().strip(),
        }

    def llenar_formulario(self, autor):
        """Coloca los datos de un autor en el formulario."""

        self._vaciar_campos()

        self.id_actual = autor.id_autor

        self._escribir(
            self.campos["nombre"],
            autor.nombre
        )

        self._escribir(
            self.campos["apellido"],
            autor.apellido
        )

    def limpiar(self):
        """Limpia el formulario y quita la selección."""

        self._vaciar_campos()

        self.id_actual = None

        self.entrada_buscar.delete(0, tk.END)

        if self.tabla.selection():
            self.tabla.selection_remove(
                self.tabla.selection()
            )

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
        """Registra un autor nuevo."""

        if not self._hay_controlador():
            return

        if self.id_actual is not None:
            self.mostrar_error(
                "Hay un autor seleccionado. "
                "Usa Actualizar o Limpiar antes de registrar otro."
            )
            return

        try:
            datos = self.obtener_datos()

            autor = Autor(
                nombre=datos["nombre"],
                apellido=datos["apellido"]
            )

        except (ValueError, TypeError) as error:
            self.mostrar_error(str(error))
            return

        guardado = self._llamar(
            self.controlador_autores.guardar,
            autor
        )

        if guardado is True:
            self.refrescar()
            self.limpiar()
            self.mostrar_mensaje("Autor registrado correctamente.")

        elif guardado is False:
            self.mostrar_error(
                "No se pudo guardar el autor. "
                "Revisa los datos e inténtalo de nuevo."
            )

    def _al_actualizar(self):
        """Actualiza el autor seleccionado."""

        if not self._hay_controlador():
            return

        if self.id_actual is None:
            self.mostrar_error(
                "Selecciona un autor de la tabla o búscalo por su ID antes de actualizar."
            )
            return

        try:
            datos = self.obtener_datos()

            autor = Autor(
                nombre=datos["nombre"],
                apellido=datos["apellido"]
            )

        except (ValueError, TypeError) as error:
            self.mostrar_error(str(error))
            return

        if not self.confirmar(
            f"¿Actualizar el autor con ID {self.id_actual}?"
        ):
            return

        resultado = self._llamar(
            self.controlador_autores.actualizar,
            autor,
            self.id_actual
        )

        if resultado is True:
            self.refrescar()
            self.limpiar()
            self.mostrar_mensaje("Autor actualizado correctamente.")

        elif resultado is False:
            self.mostrar_error(
                "No se pudo actualizar el autor."
            )

    def _al_eliminar(self):

        if not self._hay_controlador():
            return

        if self.id_actual is None:
            self.mostrar_error(
                "Selecciona un autor de la tabla o búscalo por su ID."
            )
            return

        if not self.confirmar(
            f"¿Eliminar al autor con ID {self.id_actual}?"
        ):
            return

        eliminado = self._llamar(
            self.controlador_autores.eliminar,
            self.id_actual
        )

        if eliminado:
            self.refrescar()
            self.limpiar()
            self.mostrar_mensaje("Autor eliminado correctamente.")

        elif eliminado is False:
            self.mostrar_error(
                "No se pudo eliminar el autor. Puede que tenga libros asociados."
            )

    def _al_buscar(self):

        if not self._hay_controlador():
            return

        codigo = self.entrada_buscar.get().strip()

        if not codigo:
            self.mostrar_error(
                "Escribe un ID de autor para buscar."
            )
            return

        try:
            codigo = int(codigo)

            if codigo < 1:
                raise ValueError

        except ValueError:
            self.mostrar_error(
                "El ID debe ser un número entero positivo."
            )
            return

        autor = self._llamar(
            self.controlador_autores.obtener_uno,
            "IdAutor",
            codigo
        )

        if autor is None:
            self.mostrar_error(
                f"No existe un autor con el ID {codigo}."
            )
            return

        self.llenar_formulario(autor)

        if self.tabla.exists(str(codigo)):
            self.tabla.selection_set(str(codigo))
            self.tabla.see(str(codigo))

    def _al_seleccionar_fila(self, evento):

        seleccion = self.tabla.selection()

        if not seleccion:
            return

        codigo = int(seleccion[0])

        autor = self._llamar(
            self.controlador_autores.obtener_uno,
            "IdAutor",
            codigo
        )

        if autor is not None:
            self.llenar_formulario(autor)

    # =====================================================
    # AYUDANTES INTERNOS
    # =====================================================

    def _llamar(self, funcion, *argumentos):
        """Ejecuta una operación del controlador y captura errores."""

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

        if self.controlador_autores is None:
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
# PRUEBA: abrir solamente esta ventana
# Desde la raíz: py -m vistas.vista_autores
# =====================================================

if __name__ == "__main__":

    from datos.conexion import RUTA_BD

    ctk.set_appearance_mode("light")

    ventana = ctk.CTk()
    ventana.title("Tech Aca - Gestión de Autores")
    ventana.geometry("1100x640")
    ventana.configure(fg_color=estilos.COLOR_FONDO)

    vista = VistaAutores(ventana)
    vista.pack(fill="both", expand=True)

    if RUTA_BD.exists():

        from controladores.controladores import ControladorAutores
        from datos.gestor_sql import GestorSQL
        from servicios.service import Service

        gestor = GestorSQL()
        servicio = Service(gestor)

        vista.conectar(
            ControladorAutores(servicio)
        )

        def cerrar_aplicacion():
            gestor.cerrar()
            ventana.destroy()

        ventana.protocol(
            "WM_DELETE_WINDOW",
            cerrar_aplicacion
        )

    else:
        print(
            f"Aviso: no existe {RUTA_BD}. "
            "Comprueba la ruta de la base de datos."
        )

    ventana.mainloop()
