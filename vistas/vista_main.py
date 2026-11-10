
import tkinter as tk
import customtkinter as ctk
from PIL import Image

from vistas.vista_libros import VistaLibros
from vistas.vista_autores import VistaAutores
from vistas.vista_editoriales import VistaEditoriales
from vistas.vista_usuarios import VistaUsuarios
from vistas.vista_prestamos import VistaPrestamo


ctk.set_appearance_mode("light")


class FrmPrincipal(ctk.CTk):

    def __init__(
        self,
        controlador_libros=None,
        controlador_autores=None,
        controlador_editoriales=None,
        controlador_usuarios=None,
        controlador_prestamos=None
    ):
        super().__init__()

        self.title("Aca Biblioteca")
        self.geometry("1200x700")

        # Controladores recibidos desde main.py
        self.controlador_libros = controlador_libros
        self.controlador_autores = controlador_autores
        self.controlador_editoriales = controlador_editoriales
        self.controlador_usuarios = controlador_usuarios
        self.controlador_prestamos = controlador_prestamos

        # ========================
        # PANEL IZQUIERDO
        # ========================

        self.frame_menu = ctk.CTkFrame(
            self,
            width=480,
            fg_color="#f1e8e5",
            corner_radius=0
        )

        self.frame_menu.pack(
            side="left",
            fill="both"
        )

        self.frame_menu.pack_propagate(False)

        #Frame Logo y titulo 

        self.frame_header = ctk.CTkFrame(
        self.frame_menu,
        fg_color="transparent"
        )

        self.frame_header.pack(
            fill="x",
            pady=(20,10),
            padx=10
        )

        # Logo

        self.logo_img = ctk.CTkImage(
            light_image=Image.open("utils/logo.png"),
            size=(120, 120)
        )

        self.lbl_logo = ctk.CTkLabel(
            self.frame_header,
            image=self.logo_img,
            text=""
        )

        self.lbl_logo.pack(
            pady=(15, 5),
            side="left"
        )

        # Título

        self.lbl_titulo = ctk.CTkLabel(
            self.frame_header,
            text="Biblioteca",
            font=("Georgia", 40, "bold"),
            text_color="#7F507A"
        )

        self.lbl_titulo.pack(
            pady=(25, 5),
            anchor="w"
        )

        self.lbl_subtitulo = ctk.CTkLabel(
            self.frame_header,
            text="Sistema de Gestión",
            font=("Georgia", 20),
            text_color="#7F507A"
        )

        self.lbl_subtitulo.pack(
            pady=(0, 20),
            anchor="w"
        )

        # ========================
        # BOTONES MENU
        # ========================

        btn_inicio = self._crear_boton(
            "Inicio", "utils/casa.png",
            lambda: self.cambiar_vista("Inicio")
        )

        btn_libros = self._crear_boton(
            "Libros", "utils/libros.png",
            lambda: self.cambiar_vista("Libros")
        )

        btn_autores = self._crear_boton(
            "Autores", "utils/autores.png",
            lambda: self.cambiar_vista("Autores")
        )

        btn_usuarios = self._crear_boton(
            "Usuarios", "utils/usuarios.png",
            lambda: self.cambiar_vista("Usuarios")
        )

        btn_editoriales = self._crear_boton(
            "Editoriales", "utils/editoriales.png",
            lambda: self.cambiar_vista("Editoriales")
        )

        btn_prestamos = self._crear_boton(
            "Prestamos", "utils/prestamo.png",
            lambda: self.cambiar_vista("Prestamos")
        )

        btn_salida = self._crear_boton(
            "Salida", "utils/salida.png",
            self.destroy
        )

        # ========================
        # CONTENEDOR PRINCIPAL
        # ========================

        self.frame_contenido = ctk.CTkFrame(
            self,
            fg_color="#eedad4",
            corner_radius=0
        )

        self.frame_contenido.pack(
            side="right",
            fill="both",
            expand=True
        )

        # Área central

        self.frame_centro = ctk.CTkFrame(
            self.frame_contenido,
            fg_color="#eedad4"
        )

        self.frame_centro.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.cambiar_vista("Inicio")

    # =====================================================
    # CREACIÓN DE BOTONES
    # =====================================================

    def _crear_boton(self, texto, ruta_imagen, comando):

        imagen = ctk.CTkImage(
            light_image=Image.open(ruta_imagen),
            size=(60, 60)
        )

        boton = ctk.CTkButton(
            self.frame_menu,
            text=texto,
            image=imagen,
            height=50,
            corner_radius=25,
            compound="left",
            fg_color="#eedad4",
            hover_color="#DABFC0",
            text_color="#784870",
            font=("Georgia", 22, "bold"),
            command=comando
        )

        boton.pack(
            fill="x",
            padx=20,
            pady=8
        )

        return boton

    # =====================================================
    # CAMBIAR VISTAS
    # =====================================================

    def cambiar_vista(self, opcion):

        # Eliminar la vista anterior
        for widget in self.frame_centro.winfo_children():
            widget.destroy()

        # Inicio
        if opcion == "Inicio":

            self.lbl_inicio = ctk.CTkLabel(
                self.frame_centro,
                text="Bienvenido al Sistema de Biblioteca",
                font=("Georgia", 28)
            )

            self.lbl_inicio.pack(pady=50)

        # Libros
        elif opcion == "Libros":

            vista = VistaLibros(
                self.frame_centro,
                self.controlador_libros,
                self.controlador_autores,
                self.controlador_editoriales
            )

            vista.pack(fill="both", expand=True)

        # Autores
        elif opcion == "Autores":

            vista = VistaAutores(
                self.frame_centro,
                self.controlador_autores
            )

            vista.pack(fill="both", expand=True)

        # Editoriales
        elif opcion == "Editoriales":

            vista = VistaEditoriales(
                self.frame_centro,
                self.controlador_editoriales
            )

            vista.pack(fill="both", expand=True)

        # Usuarios
        elif opcion == "Usuarios":

            vista = VistaUsuarios(
                self.frame_centro,
                self.controlador_usuarios
            )

            vista.pack(fill="both", expand=True)

        # Prestamos
        elif opcion == "Prestamos":

            vista = VistaPrestamo(
                self.frame_centro,
                self.controlador_prestamos,
                self.controlador_usuarios,
                self.controlador_libros
            )

            vista.pack(fill="both", expand=True)
