"""Modelo Autor: representa una fila de la tabla Autores. Hereda de Persona."""

from modelos import validaciones
from modelos.persona import Persona


class Autor(Persona):
    def __init__(self, nombre, apellido, id_autor=None):
        super().__init__(nombre, apellido)  # Persona se encarga de nombre y apellido
        self.id_autor = id_autor

    @property
    def id_autor(self):
        return self._id_autor

    @id_autor.setter
    def id_autor(self, valor):
        # None = autor nuevo; SQLite le asigna el Id al insertarlo
        self._id_autor = validaciones.id_opcional(valor, "IdAutor")

    @classmethod
    def desde_fila(cls, fila):
        return cls(
            nombre=validaciones.columna(fila, "Nombre"),
            apellido=validaciones.columna(fila, "Apellido"),
            id_autor=validaciones.columna(fila, "IdAutor"),
        )

    def a_diccionario(self):
        # Se aprovecha lo que ya hace Persona y se le agrega el Id
        datos = super().a_diccionario()
        datos["IdAutor"] = self.id_autor
        return datos

    def a_opcion(self):
        """Tupla (id, nombre) que espera VistaLibros.cargar_listas()."""
        return (self.id_autor, self.nombre_completo)
