"""Modelo Editorial: representa una fila de la tabla Editoriales."""

from modelos import validaciones


class Editorial:
    def __init__(self, nombre, id_editorial=None):
        self.nombre = nombre
        self.id_editorial = id_editorial

    @property
    def id_editorial(self):
        return self._id_editorial

    @id_editorial.setter
    def id_editorial(self, valor):
        self._id_editorial = validaciones.id_opcional(valor, "IdEditorial")

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._nombre = validaciones.texto_obligatorio(valor, "Nombre de la editorial", maximo=100)

    @classmethod
    def desde_fila(cls, fila):
        return cls(
            nombre=validaciones.columna(fila, "Nombre"),
            # En la BD la columna se llama "Ideditorial" (con e minúscula)
            id_editorial=validaciones.columna(fila, "Ideditorial", "IdEditorial"),
        )
        
    @classmethod
    def desde_formulario(cls, datos):
        return cls(
            nombre=validaciones.columna(datos, "Nombre")
        )

    def a_diccionario(self):
        return {"IdEditorial": self.id_editorial, "Nombre": self.nombre}

    def a_opcion(self):
        """Tupla (id, nombre) que espera VistaLibros.cargar_listas()."""
        return (self.id_editorial, self.nombre)

    def __str__(self):
        return self.nombre
