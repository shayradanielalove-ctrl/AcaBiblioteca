
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

import customtkinter as ctk
from PIL import Image

from modelos.prestamo import Prestamo
from utils import estilos


RUTA_LOGO = (
    Path(__file__).resolve().parent.parent
    / "recursos"
    / "logo.png"
)


class VistaPrestamo(ctk.CTkFrame):

    COLUMNAS = [
        ("IdPrestamo", "ID", 60),
        ("Usuario", "Usuario", 150),
        ("ISBN", "ISBN", 120),
        ("Libro", "Libro", 170),
        ("FechaPrestamo", "Fecha préstamo", 110),
        ("FechaDevolucion", "Fecha devolución", 110),
        ("Estado", "Estado", 100),
    ]

    def __init__(
        self,
        master,
        controlador_prestamos=None,
        controlador_usuarios=None,
        controlador_libros=None
    ):
        super().__init__(
            master,
            fg_color=estilos.COLOR_FONDO,
            corner_radius=0
        )

        self.controlador_prestamos = controlador_prestamos
        self.controlador_usuarios = controlador_usuarios
        self.controlador_libros = controlador_libros

        self.campos = {}

        self._usuarios = {}
        self._libros = {}

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._crear_encabezado()
        self._crear_panel_izquierdo()
        self._crear_tabla()

        if self.controlador_prestamos is not None:
            self.refrescar()

    # =====================================================
    # ENCABEZADO
    # =====================================================

    def _crear_encabezado(self):

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
            text="Gestión de Préstamos",
            font=estilos.FUENTE_TITULO,
            text_color=estilos.COLOR_TEXTO
        ).pack(side="left", pady=5)

    # =====================================================
    # PANEL IZQUIERDO
    # =====================================================

    def _crear_panel_izquierdo(self):

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

        # Búsqueda

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
            text="ID Préstamo:",
            font=estilos.FUENTE_SUBTITULO,
            text_color=estilos.COLOR_TEXTO
        ).pack(side="left", padx=(10, 5), pady=10)

        self.entrada_buscar = self._nueva_caja(
            barra,
            ancho=90
        )

        self.entrada_buscar.pack(side="left", pady=10)

        self.entrada_buscar.bind(
            "<Return>",
            lambda evento: self._al_buscar()
        )

        self._nuevo_boton(
            barra,
            "Buscar",
            estilos.COLOR_BOTON_BUSCAR_HOVER,
            estilos.COLOR_BOTON_BUSCAR_HOVER,
            self._al_buscar
        ).pack(side="left", padx=8, pady=10)

        # Formulario

        formulario = ctk.CTkFrame(
            panel,
            fg_color="transparent"
        )

        formulario.pack(padx=20, pady=5)

        filas = [
            ("id_prestamo", "ID Préstamo:", "caja"),
            ("usuario", "Usuario:", "lista"),
            ("libro", "Libro:", "lista"),
            ("fecha_prestamo", "Fecha préstamo:", "caja"),
            ("fecha_devolucion", "Fecha devolución:", "caja"),
            ("estado", "Estado:", "lista"),
        ]

        for numero, (clave, texto, tipo) in enumerate(filas):

            ctk.CTkLabel(
                formulario,
                text=texto,
                font=estilos.FUENTE_ETIQUETA,
                text_color=estilos.COLOR_TEXTO
            ).grid(
                row=numero,
                column=0,
                sticky="e",
                padx=(0, 12),
                pady=7
            )

            if tipo == "caja":

                widget = self._nueva_caja(formulario)

                if clave in (
                    "id_prestamo",
                    "fecha_prestamo",
                    "fecha_devolucion"
                ):
                    widget.configure(state="readonly")

            else:

                widget = self._nueva_lista(formulario)

                if clave == "estado":
                    widget.configure(
                        values=list(Prestamo.ESTADOS)
                    )

            widget.grid(
                row=numero,
                column=1,
                pady=7
            )

            self.campos[clave] = widget

        # Botones

        botones = ctk.CTkFrame(
            panel,
            fg_color="transparent"
        )

        botones.pack(pady=(20, 15))

        self._nuevo_boton(
            botones,
            "Registrar",
            estilos.COLOR_BOTON_PRINCIPAL,
            estilos.COLOR_BOTON_PRINCIPAL_HOVER,
            self._al_guardar
        ).grid(row=0, column=0, padx=5)

        self._nuevo_boton(
            botones,
            "Devolver",
            estilos.COLOR_BOTON_PELIGRO,
            estilos.COLOR_BOTON_PELIGRO_HOVER,
            self._al_devolver
        ).grid(row=0, column=1, padx=5)

        self._nuevo_boton(
            botones,
            "Limpiar",
            estilos.COLOR_BOTON_SECUNDARIO,
            estilos.COLOR_BOTON_SECUNDARIO_HOVER,
            self.limpiar
        ).grid(row=0, column=2, padx=5)

    # =====================================================
    # TABLA
    # =====================================================

    def _crear_tabla(self):

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
            "Prestamos.Treeview",
            background=estilos.COLOR_TABLA_FONDO,
            fieldbackground=estilos.COLOR_TABLA_FONDO,
            foreground=estilos.COLOR_TEXTO,
            font=estilos.FUENTE_TABLA,
            rowheight=30,
            borderwidth=0
        )

        estilo.configure(
            "Prestamos.Treeview.Heading",
            background=estilos.COLOR_TABLA_ENCABEZADO,
            foreground=estilos.COLOR_TEXTO,
            font=estilos.FUENTE_TABLA_ENCABEZADO,
            relief="flat"
        )

        estilo.map(
            "Prestamos.Treeview",
            background=[
                ("selected", estilos.COLOR_TABLA_SELECCION)
            ]
        )

        claves = [
            clave for clave, _, _ in self.COLUMNAS
        ]

        self.tabla = ttk.Treeview(
            contenedor,
            columns=claves,
            show="headings",
            style="Prestamos.Treeview",
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
                minwidth=50,
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
            command=self.tabla.yview
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
    # WIDGETS
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
            dropdown_hover_color=estilos.COLOR_TABLA_SELECCION
        )

        lista.set("")

        return lista

    def _nuevo_boton(
        self,
        padre,
        texto,
        color,
        color_hover,
        accion
    ):

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
            command=accion
        )

    # =====================================================
    # CONEXIÓN CON CONTROLADORES
    # =====================================================

    def conectar(
        self,
        controlador_prestamos,
        controlador_usuarios,
        controlador_libros
    ):

        self.controlador_prestamos = controlador_prestamos
        self.controlador_usuarios = controlador_usuarios
        self.controlador_libros = controlador_libros

        self.refrescar()

    def _hay_controladores(self):

        if (
            self.controlador_prestamos is None
            or self.controlador_usuarios is None
            or self.controlador_libros is None
        ):
            self.mostrar_error(
                "La vista no tiene todos los controladores conectados."
            )
            return False

        return True

    # =====================================================
    # CARGAR DATOS
    # =====================================================

    def refrescar(self):

        if not self._hay_controladores_silencioso():
            return

        try:

            usuarios = self.controlador_usuarios.obtener_todo()
            libros = self.controlador_libros.obtener_todo()
            prestamos = self.controlador_prestamos.obtener_todo()

            self.cargar_listas(usuarios, libros)

            nombres_usuarios = {
                usuario.id_usuario: usuario.nombre
                for usuario in usuarios
            }

            titulos_libros = {
                libro.isbn: libro.titulo
                for libro in libros
            }

            filas = []

            for prestamo in prestamos:

                fila = prestamo.a_diccionario()

                fila["Usuario"] = nombres_usuarios.get(
                    prestamo.id_usuario,
                    "Usuario desconocido"
                )

                fila["Libro"] = titulos_libros.get(
                    prestamo.isbn,
                    "Libro desconocido"
                )

                filas.append(fila)

            filas.sort(
                key=lambda fila: fila["IdPrestamo"] or 0,
                reverse=True
            )

            self.cargar_tabla(filas)

        except Exception as error:

            self.mostrar_error(
                f"No se pudieron cargar los préstamos:\n{error}"
            )

    def _hay_controladores_silencioso(self):

        return all((
            self.controlador_prestamos,
            self.controlador_usuarios,
            self.controlador_libros
        ))

    def cargar_listas(self, usuarios, libros):

        self._usuarios = {
            f"{usuario.id_usuario} - {usuario.nombre} {usuario.apellido}":
            usuario.id_usuario
            for usuario in usuarios
        }

        self._libros = {
            f"{libro.isbn} - {libro.titulo}": libro.isbn
            for libro in libros
            if libro.existencias > 0
        }

        self.campos["usuario"].configure(
            values=list(self._usuarios.keys())
        )

        self.campos["libro"].configure(
            values=list(self._libros.keys())
        )

    def cargar_tabla(self, prestamos):

        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        for numero, prestamo in enumerate(prestamos):

            valores = [
                prestamo.get(clave, "")
                for clave, _, _ in self.COLUMNAS
            ]

            tono = "par" if numero % 2 == 0 else "impar"

            self.tabla.insert(
                "",
                tk.END,
                iid=str(prestamo["IdPrestamo"]),
                values=valores,
                tags=(tono,)
            )

    # =====================================================
    # FORMULARIO
    # =====================================================

    def obtener_datos(self):

        return {
            "id_usuario": self._usuarios.get(
                self.campos["usuario"].get()
            ),
            "isbn": self._libros.get(
                self.campos["libro"].get()
            )
        }

    def llenar_formulario(self, prestamo):

        self.limpiar()

        self._escribir(
            self.campos["id_prestamo"],
            prestamo.get("IdPrestamo", "")
        )

        self._escribir(
            self.campos["fecha_prestamo"],
            prestamo.get("FechaPrestamo", "")
        )

        self._escribir(
            self.campos["fecha_devolucion"],
            prestamo.get("FechaDevolucion", "")
        )

        self.campos["estado"].set(
            prestamo.get("Estado", "")
        )

        self.campos["usuario"].set(
            self._buscar_opcion(
                self._usuarios,
                prestamo.get("IdUsuarios")
            )
        )

        self.campos["libro"].set(
            self._buscar_opcion(
                self._libros,
                prestamo.get("ISBN")
            )
        )

    def limpiar(self):

        for widget in self.campos.values():

            if isinstance(widget, ctk.CTkComboBox):
                widget.set("")

            else:
                widget.configure(state="normal")
                widget.delete(0, tk.END)

                if widget in (
                    self.campos["id_prestamo"],
                    self.campos["fecha_prestamo"],
                    self.campos["fecha_devolucion"]
                ):
                    widget.configure(state="readonly")

        self.entrada_buscar.delete(0, tk.END)

        seleccion = self.tabla.selection()

        if seleccion:
            self.tabla.selection_remove(seleccion)

    # =====================================================
    # EVENTOS
    # =====================================================

    def _al_guardar(self):

        if not self._hay_controladores():
            return

        try:

            datos = self.obtener_datos()

            prestamo = Prestamo(
                id_usuario=datos["id_usuario"],
                isbn=datos["isbn"]
            )

        except ValueError as error:

            self.mostrar_error(str(error))
            return

        resultado = self._llamar(
            self.controlador_prestamos.guardar,
            prestamo
        )

        if resultado:

            self.refrescar()
            self.limpiar()

            self.mostrar_mensaje(
                "Préstamo registrado correctamente."
            )

        elif resultado is False:

            self.mostrar_error(
                "No se pudo registrar el préstamo. "
                "Comprueba las existencias y los datos."
            )

    def _al_devolver(self):

        if not self._hay_controladores():
            return

        codigo = self.campos["id_prestamo"].get().strip()

        if not codigo:
            self.mostrar_error(
                "Selecciona un préstamo de la tabla."
            )
            return

        try:
            codigo = int(codigo)
        except ValueError:
            self.mostrar_error("El ID del préstamo no es válido.")
            return

        if self.campos["estado"].get() == Prestamo.DEVUELTO:
            self.mostrar_error("Este préstamo ya fue devuelto.")
            return

        if not self.confirmar(
            f"¿Registrar la devolución del préstamo {codigo}?"
        ):
            return

        resultado = self._llamar(
            self.controlador_prestamos.devolver,
            codigo
        )

        if resultado:

            self.refrescar()
            self.limpiar()

            self.mostrar_mensaje(
                "Libro devuelto correctamente."
            )

        elif resultado is False:

            self.mostrar_error(
                "No se pudo registrar la devolución."
            )

    def _al_buscar(self):

        if not self._hay_controladores():
            return

        codigo = self.entrada_buscar.get().strip()

        if not codigo:
            self.mostrar_error("Escribe un ID de préstamo.")
            return

        try:
            codigo = int(codigo)
        except ValueError:
            self.mostrar_error("El ID debe ser un número entero.")
            return

        prestamo = self._llamar(
            self.controlador_prestamos.obtener_uno,
            codigo
        )

        if prestamo is None:
            self.mostrar_error(
                f"No existe el préstamo {codigo}."
            )
            return

        self.llenar_formulario(
            prestamo.a_diccionario()
        )

    def _al_seleccionar_fila(self, evento):

        seleccion = self.tabla.selection()

        if not seleccion:
            return

        valores = self.tabla.item(
            seleccion[0],
            "values"
        )

        prestamo = {
            clave: valores[i]
            for i, (clave, _, _) in enumerate(self.COLUMNAS)
        }

        prestamo["IdPrestamo"] = seleccion[0]

        self.llenar_formulario(prestamo)

    # =====================================================
    # AYUDANTES
    # =====================================================

    def _llamar(self, funcion, *argumentos):

        try:
            return funcion(*argumentos)

        except Exception as error:

            self.mostrar_error(
                f"Ocurrió un error:\n{error}"
            )

            return None

    def mostrar_mensaje(self, texto):

        messagebox.showinfo("Biblioteca", texto)

    def mostrar_error(self, texto):

        messagebox.showerror("Error", texto)

    def confirmar(self, texto):

        return messagebox.askyesno(
            "Confirmar",
            texto
        )

    @staticmethod
    def _escribir(caja, valor):

        caja.configure(state="normal")
        caja.delete(0, tk.END)
        caja.insert(
            0,
            "" if valor is None else str(valor)
        )
        caja.configure(state="readonly")

    @staticmethod
    def _buscar_opcion(diccionario, id_buscado):

        for texto, identificador in diccionario.items():

            if str(identificador) == str(id_buscado):
                return texto

        return ""


# =====================================================
# PRUEBA INDEPENDIENTE
# =====================================================

if __name__ == "__main__":

    from datos.gestor_sql import GestorSQL
    from servicios.prestamo_service import PrestamoService
    from servicios.service import Service

    from controladores.controlador_prestamo import ControladorPrestamos
    from controladores.controladores import (
        ControladorLibros,
        ControladorUsuarios
    )

    ctk.set_appearance_mode("light")

    ventana = ctk.CTk()
    ventana.title("Tech Aca - Gestión de Préstamos")
    ventana.geometry("1450x700")
    ventana.configure(fg_color=estilos.COLOR_FONDO)

    gestor = GestorSQL()

    servicio = Service(gestor)
    servicio_prestamo = PrestamoService(gestor)

    controlador_prestamos = ControladorPrestamos(
        servicio_prestamo
    )

    controlador_usuarios = ControladorUsuarios(
        servicio
    )

    controlador_libros = ControladorLibros(
        servicio
    )

    vista = VistaPrestamo(self.frame_centro,
        self.controlador_prestamos,
        self.controlador_usuarios,
        self.controlador_libros)

    vista.pack(fill="both", expand=True)

    vista.conectar(
        controlador_prestamos,
        controlador_usuarios,
        controlador_libros
    )

    def cerrar():
        gestor.cerrar()
        ventana.destroy()

    ventana.protocol("WM_DELETE_WINDOW", cerrar)

    ventana.mainloop()
