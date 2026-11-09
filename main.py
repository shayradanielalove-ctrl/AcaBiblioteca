from datos.gestor_sql import GestorSQL

from servicios.service import Service
from servicios.prestamo_service import PrestamoService

from controladores.controladores import (ControladorLibros, ControladorAutores, ControladorEditoriales, ControladorUsuarios)
from controladores.controlador_prestamo import ControladorPrestamos

def main():
    gestor = GestorSQL()

    service = Service(gestor)
    prestamo_service = PrestamoService(gestor)

    libros = ControladorLibros(service)
    autores = ControladorAutores(service)
    editoriales = ControladorEditoriales(service)
    usuarios = ControladorUsuarios(service)

    prestamos = ControladorPrestamos(prestamo_service)