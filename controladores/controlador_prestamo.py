
from servicios.prestamo_service import PrestamoService


class ControladorPrestamos:

    def __init__(self, servicio):
        self.servicio = servicio

    def guardar(self, prestamo):
        return self.servicio.guardar_prestamo(prestamo)

    def devolver(self, codigo):
        return self.servicio.devolucion(codigo)

    def obtener_todo(self):
        return self.servicio.listar_todo()

    def obtener_uno(self, codigo):
        return self.servicio.listar_uno(codigo)
