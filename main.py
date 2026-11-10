import customtkinter as ctk

from datos.gestor_sql import GestorSQL

from servicios.service import Service
from servicios.prestamo_service import PrestamoService

from controladores.controladores import (
    ControladorLibros,
    ControladorAutores,
    ControladorEditoriales,
    ControladorUsuarios
)

from controladores.controlador_prestamo import ControladorPrestamos

from vistas.vista_main import FrmPrincipal


def main():

    ctk.set_appearance_mode("light")

    # ==============================
    # GESTOR DE BASE DE DATOS
    # ==============================

    gestor = GestorSQL()

    # ==============================
    # SERVICIOS
    # ==============================

    servicio = Service(gestor)

    servicio_prestamos = PrestamoService(gestor)

    # ==============================
    # CONTROLADORES
    # ==============================

    controlador_libros = ControladorLibros(servicio)

    controlador_autores = ControladorAutores(servicio)

    controlador_editoriales = ControladorEditoriales(servicio)

    controlador_usuarios = ControladorUsuarios(servicio)

    controlador_prestamos = ControladorPrestamos(servicio_prestamos)

    # ==============================
    # VENTANA PRINCIPAL
    # ==============================

    app = FrmPrincipal(
        controlador_libros=controlador_libros,
        controlador_autores=controlador_autores,
        controlador_editoriales=controlador_editoriales,
        controlador_usuarios=controlador_usuarios,
        controlador_prestamos=controlador_prestamos
    )

    # Cerrar correctamente la conexión
    def cerrar_aplicacion():
        gestor.cerrar()
        app.destroy()

    app.protocol("WM_DELETE_WINDOW", cerrar_aplicacion)

    app.mainloop()


if __name__ == "__main__":
    main()
