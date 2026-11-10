"""
Clase base Persona.

Autor y Usuario tienen en común el nombre y el apellido, así que los dos
HEREDAN de Persona en vez de repetir ese código (herencia).
"""

from modelos import validaciones


class Persona:
    def __init__(self, nombre, apellido):
        # Al asignar self.nombre se llama al "setter" de abajo, que valida el dato
        self.nombre = nombre
        self.apellido = apellido

    # ---------- Propiedades (encapsulamiento) ----------
    # El dato real se guarda en self._nombre (con guion bajo = "privado").
    # Desde fuera se usa persona.nombre, y al cambiarlo siempre pasa por la validación.

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._nombre = validaciones.texto_obligatorio(valor, "Nombre", maximo=60)

    @property
    def apellido(self):
        return self._apellido

    @apellido.setter
    def apellido(self, valor):
        self._apellido = validaciones.texto_obligatorio(valor, "Apellido", maximo=60)

    @property
    def nombre_completo(self):
        """Propiedad calculada: no se guarda, se arma con nombre + apellido."""
        return f"{self.nombre} {self.apellido}"

    def a_diccionario(self):
        """Cada clase hija lo redefine con sus propios campos (polimorfismo)."""
        return {"Nombre": self.nombre, "Apellido": self.apellido}

    def __str__(self):
        return self.nombre_completo
