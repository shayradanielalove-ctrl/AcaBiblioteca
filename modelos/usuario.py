"""Modelo Usuario: representa una fila de la tabla Usuarios. Hereda de Persona."""

from modelos import validaciones
from modelos.persona import Persona


class Usuario(Persona):
    def __init__(self, nombre, apellido, documento, telefono, correo, id_usuario=None):
        super().__init__(nombre, apellido)
        self.documento = documento
        self.telefono = telefono
        self.correo = correo
        self.id_usuario = id_usuario

    @property
    def id_usuario(self):
        return self._id_usuario

    @id_usuario.setter
    def id_usuario(self, valor):
        self._id_usuario = validaciones.id_opcional(valor, "IdUsuario")

    @property
    def documento(self):
        return self._documento

    @documento.setter
    def documento(self, valor):
        self._documento = validaciones.solo_digitos(valor, "Documento", minimo=6, maximo=15)

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        self._telefono = validaciones.solo_digitos(valor, "Teléfono", minimo=7, maximo=15)

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, valor):
        self._correo = validaciones.correo(valor)

    @classmethod
    def desde_fila(cls, fila):
        return cls(
            nombre=validaciones.columna(fila, "Nombre"),
            apellido=validaciones.columna(fila, "Apellido"),
            documento=validaciones.columna(fila, "Documento"),
            telefono=validaciones.columna(fila, "Telefono"),
            correo=validaciones.columna(fila, "Correo"),
            # En la BD la columna se llama "IdUsuarios" (en plural)
            id_usuario=validaciones.columna(fila, "IdUsuarios", "IdUsuario"),
        )

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos.update({
            "IdUsuario": self.id_usuario,
            "Documento": self.documento,
            "Telefono": self.telefono,
            "Correo": self.correo,
        })
        return datos

    def a_opcion(self):
        """Tupla (id, texto) para una lista desplegable, por ejemplo en Préstamos."""
        return (self.id_usuario, f"{self.nombre_completo} - {self.documento}")
