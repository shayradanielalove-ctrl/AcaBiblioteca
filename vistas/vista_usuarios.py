import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

import customtkinter as ctk
from PIL import Image

from modelos.usuario import Usuario
from utils import estilos

# Ruta del logo: carpeta recursos/ en la raíz del proyecto
RUTA_LOGO = Path(__file__).resolve().parent.parent / "recursos" / "logo.png"


class VistaUsuarios(ctk.CTkFrame):
    """
    Pantalla de Gestión de Usuarios (formulario a la izquierda, tabla a la derecha).
    Tiene el mismo diseño que la pantalla de Libros.

    Usa ControladorUsuarios (controladores/controladores.py):
    guardar, actualizar, eliminar, obtener_uno, obtener_todo.
    """

    # Columnas de la tabla: (clave del diccionario, texto del encabezado, ancho)
    COLUMNAS = [
        ("IdUsuario", "Id", 45),
        ("Nombre", "Nombre", 120),
        ("Apellido", "Apellido", 130),
        ("Documento", "Documento", 115),
        ("Telefono", "Teléfono", 110),
        ("Correo", "Correo", 190),
    ]

    def __init__(self, master, controlador_usuarios=None):
        super().__init__(master, fg_color=estilos.COLOR_FONDO, corner_radius=0)
        self.controlador_usuarios = controlador_usuarios

        # Id del usuario que se está editando. None = el formulario es para uno nuevo.
        # El Id no se escribe a mano: lo pone SQLite (AUTOINCREMENT).
        self._id_actual = None

        self.campos = {}  # Aquí se guardan las cajas del formulario

        # La columna 1 (la tabla) crece si se agranda la ventana
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._crear_encabezado()
        self._crear_panel_izquierdo()
        self._crear_tabla()

        if self.controlador_usuarios is not None:
            self.refrescar()

    # =====================================================
    # CONSTRUCCIÓN DE LA PANTALLA
    # =====================================================

    def _crear_encabezado(self):
        """Franja superior con el logo de Tech Aca y el título 'Gestión de Usuarios'."""
        encabezado = ctk.CTkFrame(self, fg_color=estilos.COLOR_FONDO, corner_radius=0)
        encabezado.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(10, 5))

        if RUTA_LOGO.exists():
            imagen = Image.open(RUTA_LOGO)
            alto = 90
            ancho = round(imagen.width * alto / imagen.height)  # se mantiene la proporción
            self._logo = ctk.CTkImage(light_image=imagen, size=(ancho, alto))
            ctk.CTkLabel(encabezado, image=self._logo, text="").pack(side="left", padx=(20, 15))

        ctk.CTkLabel(
            encabezado,
            text="Gestión de Usuarios",
            font=estilos.FUENTE_TITULO,
            text_color=estilos.COLOR_TEXTO,
        ).pack(side="left", pady=5)

    def _crear_panel_izquierdo(self):
        """Barra de búsqueda + formulario + botones."""
        panel = ctk.CTkFrame(self, fg_color=estilos.COLOR_PANEL, corner_radius=estilos.RADIO_BORDE)
        panel.grid(row=1, column=0, sticky="nsew", padx=(20, 10), pady=(0, 20))

        # ---------- Barra de búsqueda (por documento) ----------
        barra = ctk.CTkFrame(panel, fg_color=estilos.COLOR_BARRA, corner_radius=estilos.RADIO_BORDE)
        barra.pack(fill="x", padx=15, pady=(15, 20))

        ctk.CTkLabel(
            barra, text="Documento", font=estilos.FUENTE_SUBTITULO, text_color=estilos.COLOR_TEXTO
        ).pack(side="left", padx=(15, 8), pady=10)

        self.entrada_buscar = self._nueva_caja(barra, ancho=130)
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
            ("nombre", "Nombre:"),
            ("apellido", "Apellido:"),
            ("documento", "Documento:"),
            ("telefono", "Teléfono:"),
            ("correo", "Correo:"),
        ]

        for numero_fila, (clave, texto) in enumerate(filas):
            ctk.CTkLabel(
                formulario, text=texto, font=estilos.FUENTE_ETIQUETA, text_color=estilos.COLOR_TEXTO
            ).grid(row=numero_fila, column=0, sticky="e", padx=(0, 12), pady=6)

            caja = self._nueva_caja(formulario)
            caja.grid(row=numero_fila, column=1, pady=6)
            self.campos[clave] = caja

        # Texto pequeño que dice si se está creando un usuario o editando uno
        self.etiqueta_modo = ctk.CTkLabel(
            panel, text="", font=estilos.FUENTE_ETIQUETA, text_color=estilos.COLOR_TEXTO_SECUNDARIO
        )
        self.etiqueta_modo.pack(pady=(10, 0))
        self._mostrar_modo()

        # ---------- Botones ----------
        botones = ctk.CTkFrame(panel, fg_color="transparent")
        botones.pack(pady=(15, 15))

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
        """Tabla (Treeview) con los usuarios registrados."""
        contenedor = ctk.CTkFrame(self, fg_color=estilos.COLOR_PANEL, corner_radius=estilos.RADIO_BORDE)
        contenedor.grid(row=1, column=1, sticky="nsew", padx=(10, 20), pady=(0, 20))

        # Mismo estilo de tabla que la pantalla de Libros
        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure(
            "Usuarios.Treeview",
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
        estilo.layout("Usuarios.Treeview", [("Treeview.treearea", {"sticky": "nswe"})])
        estilo.configure(
            "Usuarios.Treeview.Heading",
            background=estilos.COLOR_TABLA_ENCABEZADO,
            foreground=estilos.COLOR_TEXTO,
            font=estilos.FUENTE_TABLA_ENCABEZADO,
            relief="flat",
            bordercolor=estilos.COLOR_TABLA_ENCABEZADO,
            lightcolor=estilos.COLOR_TABLA_ENCABEZADO,
            darkcolor=estilos.COLOR_TABLA_ENCABEZADO,
        )
        estilo.map(
            "Usuarios.Treeview",
            background=[("selected", estilos.COLOR_TABLA_SELECCION)],
            foreground=[("selected", estilos.COLOR_TEXTO)],
        )
        estilo.map("Usuarios.Treeview.Heading", background=[("active", estilos.COLOR_BOTON_SECUNDARIO_HOVER)])

        claves = [clave for clave, _, _ in self.COLUMNAS]
        self.tabla = ttk.Treeview(
            contenedor, columns=claves, show="headings", style="Usuarios.Treeview", selectmode="browse"
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
    # CONEXIÓN CON EL CONTROLADOR
    # =====================================================

    def conectar(self, controlador_usuarios):
        """Conecta el controlador después de crear la vista y carga los datos."""
        self.controlador_usuarios = controlador_usuarios
        self.refrescar()

    def refrescar(self):
        """Vuelve a leer los usuarios desde la base y los muestra en la tabla."""
        usuarios = self._llamar(self.controlador_usuarios.obtener_todo) or []
        usuarios = sorted(usuarios, key=lambda u: (u.apellido.lower(), u.nombre.lower()))
        self.cargar_tabla([usuario.a_diccionario() for usuario in usuarios])

    # =====================================================
    # MÉTODOS PARA MOSTRAR DATOS
    # =====================================================

    def cargar_tabla(self, usuarios):
        """Muestra los usuarios en la tabla. usuarios es una lista de diccionarios."""
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        for numero, usuario in enumerate(usuarios):
            valores = [usuario.get(clave, "") for clave, _, _ in self.COLUMNAS]
            tono = "par" if numero % 2 == 0 else "impar"
            # iid = Id del usuario, así cada fila se reconoce por su Id
            self.tabla.insert("", tk.END, iid=str(usuario["IdUsuario"]), values=valores, tags=(tono,))

    def llenar_formulario(self, usuario):
        """Pone los datos de un usuario (diccionario) en el formulario y recuerda su Id."""
        self._vaciar_campos()
        self._escribir(self.campos["nombre"], usuario.get("Nombre"))
        self._escribir(self.campos["apellido"], usuario.get("Apellido"))
        self._escribir(self.campos["documento"], usuario.get("Documento"))
        self._escribir(self.campos["telefono"], usuario.get("Telefono"))
        self._escribir(self.campos["correo"], usuario.get("Correo"))
        self._id_actual = int(usuario["IdUsuario"]) if usuario.get("IdUsuario") else None
        self._mostrar_modo()

    def limpiar(self):
        """Deja el formulario vacío, listo para registrar un usuario nuevo."""
        self._vaciar_campos()
        self._id_actual = None
        self._mostrar_modo()
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
        if not self._hay_controlador():
            return

        # 1) El modelo Usuario valida los datos (obligatorios, solo números, correo...)
        try:
            usuario = Usuario(
                nombre=self.campos["nombre"].get(),
                apellido=self.campos["apellido"].get(),
                documento=self.campos["documento"].get(),
                telefono=self.campos["telefono"].get(),
                correo=self.campos["correo"].get(),
                id_usuario=self._id_actual,
            )
        except ValueError as error:
            self.mostrar_error(str(error))
            return

        # 2) Dos usuarios no pueden tener el mismo documento
        #    (la base no lo impide, así que se revisa aquí)
        otro = self._llamar(self.controlador_usuarios.obtener_uno, "Documento", usuario.documento)
        if otro is not None and otro.id_usuario != self._id_actual:
            self.mostrar_error(f"Ya existe un usuario con el documento {usuario.documento}: {otro.nombre_completo}.")
            return

        # 3) Si hay un usuario seleccionado se ACTUALIZA; si no, se REGISTRA uno nuevo
        if self._id_actual is not None:
            if not self.confirmar(f"¿Actualizar los datos de {usuario.nombre_completo}?"):
                return
            guardado = self._llamar(self.controlador_usuarios.actualizar, usuario, self._id_actual)
        else:
            guardado = self._llamar(self.controlador_usuarios.guardar, usuario)

        if guardado:
            self.refrescar()
            self.limpiar()
            self.mostrar_mensaje("Usuario guardado correctamente.")
        elif guardado is False:
            self.mostrar_error("No se pudo guardar el usuario. Revisa los datos e inténtalo de nuevo.")

    def _al_eliminar(self):
        if not self._hay_controlador():
            return
        if self._id_actual is None:
            self.mostrar_error("Selecciona un usuario de la tabla o búscalo por su documento.")
            return

        nombre = f"{self.campos['nombre'].get()} {self.campos['apellido'].get()}".strip()
        if not self.confirmar(f"¿Eliminar al usuario {nombre}?"):
            return

        if self._llamar(self.controlador_usuarios.eliminar, self._id_actual):
            self.refrescar()
            self.limpiar()
            self.mostrar_mensaje("Usuario eliminado.")
        else:
            # Lo más común: el usuario tiene préstamos y la clave foránea no deja borrarlo
            self.mostrar_error("No se pudo eliminar el usuario. Puede que tenga préstamos registrados.")

    def _al_buscar(self):
        if not self._hay_controlador():
            return
        documento = self.entrada_buscar.get().strip()
        if not documento:
            self.mostrar_error("Escribe un documento para buscar.")
            return
        usuario = self._llamar(self.controlador_usuarios.obtener_uno, "Documento", documento)
        if usuario is None:
            self.mostrar_error(f"No existe un usuario con el documento {documento}.")
            return

        datos = usuario.a_diccionario()
        self.llenar_formulario(datos)
        # También se marca su fila en la tabla
        fila = str(datos["IdUsuario"])
        if self.tabla.exists(fila):
            self.tabla.selection_set(fila)
            self.tabla.see(fila)

    def _al_seleccionar_fila(self, evento):
        seleccion = self.tabla.selection()
        if not seleccion:
            return
        valores = self.tabla.item(seleccion[0], "values")
        usuario = {clave: valores[i] for i, (clave, _, _) in enumerate(self.COLUMNAS)}
        self.llenar_formulario(usuario)

    # ---------- Ayudantes internos ----------

    def _mostrar_modo(self):
        if self._id_actual is None:
            self.etiqueta_modo.configure(text="Nuevo usuario")
        else:
            self.etiqueta_modo.configure(text=f"Editando el usuario #{self._id_actual}")

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
        for caja in self.campos.values():
            caja.delete(0, tk.END)

    def _hay_controlador(self):
        if self.controlador_usuarios is None:
            self.mostrar_error("La vista no tiene controlador conectado.")
            return False
        return True

    @staticmethod
    def _escribir(caja, valor):
        caja.delete(0, tk.END)
        caja.insert(0, "" if valor is None else str(valor))


# =====================================================
# PRUEBA: abrir solo esta ventana, conectada a la base de datos real
# (desde la raíz del proyecto: py -m vistas.vista_usuarios)
# =====================================================
if __name__ == "__main__":
    from datos.conexion import RUTA_BD

    ctk.set_appearance_mode("light")
    ventana = ctk.CTk()
    ventana.title("Tech Aca - Gestión de Usuarios")
    ventana.geometry("1320x640")
    ventana.configure(fg_color=estilos.COLOR_FONDO)

    vista = VistaUsuarios(ventana)
    vista.pack(fill="both", expand=True)

    if RUTA_BD.exists():
        # Misma conexión entre capas que usa main.py: gestor -> servicio -> controlador
        from controladores.controladores import ControladorUsuarios
        from datos.gestor_sql import GestorSQL
        from servicios.service import Service

        vista.conectar(ControladorUsuarios(Service(GestorSQL())))
    else:
        print(f"Aviso: no existe {RUTA_BD}. Crea la base desde database/schema_y_datos.sql.")

    ventana.mainloop()
