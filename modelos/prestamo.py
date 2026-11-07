"""Modelo Prestamo: representa una fila de la tabla Prestamos."""

from datetime import date

from modelos import validaciones


class Prestamo:
    # Constantes de clase: los únicos estados que puede tener un préstamo
    PRESTADO = "Prestado"
    DEVUELTO = "Devuelto"
    ESTADOS = (PRESTADO, DEVUELTO)

    def __init__(self, id_usuario, isbn, fecha_prestamo=None, fecha_devolucion=None,
                 estado=PRESTADO, id_prestamo=None):
        self.id_usuario = id_usuario
        self.isbn = isbn
        # Si no se da la fecha del préstamo, se usa la de hoy
        self.fecha_prestamo = fecha_prestamo or date.today()
        self.fecha_devolucion = fecha_devolucion
        self.estado = estado
        self.id_prestamo = id_prestamo

    # ---------- Propiedades con validación ----------

    @property
    def id_prestamo(self):
        return self._id_prestamo

    @id_prestamo.setter
    def id_prestamo(self, valor):
        self._id_prestamo = validaciones.id_opcional(valor, "IdPrestamo")

    @property
    def id_usuario(self):
        return self._id_usuario

    @id_usuario.setter
    def id_usuario(self, valor):
        if valor is None or str(valor).strip() == "":
            raise ValueError("Debes escoger un usuario.")
        self._id_usuario = validaciones.entero(valor, "Usuario", minimo=1)

    @property
    def isbn(self):
        return self._isbn

    @isbn.setter
    def isbn(self, valor):
        if valor is None or str(valor).strip() == "":
            raise ValueError("Debes escoger un libro.")
        self._isbn = str(valor).strip()

    @property
    def fecha_prestamo(self):
        return self._fecha_prestamo

    @fecha_prestamo.setter
    def fecha_prestamo(self, valor):
        self._fecha_prestamo = validaciones.fecha(valor, "Fecha de préstamo")

    @property
    def fecha_devolucion(self):
        return self._fecha_devolucion

    @fecha_devolucion.setter
    def fecha_devolucion(self, valor):
        nueva = validaciones.fecha(valor, "Fecha de devolución", obligatorio=False)
        if nueva is not None and nueva < self.fecha_prestamo:
            raise ValueError("La fecha de devolución no puede ser anterior a la del préstamo.")
        self._fecha_devolucion = nueva

    @property
    def estado(self):
        return self._estado

    @estado.setter
    def estado(self, valor):
        if valor not in self.ESTADOS:
            raise ValueError(f"El estado debe ser {self.PRESTADO} o {self.DEVUELTO}.")
        # Coherencia: un préstamo "Devuelto" debe tener fecha de devolución
        if valor == self.DEVUELTO and self.fecha_devolucion is None:
            raise ValueError("Un préstamo devuelto necesita fecha de devolución.")
        self._estado = valor

    @property
    def activo(self):
        """True mientras el libro no se haya devuelto."""
        return self.estado == self.PRESTADO

    # ---------- Acciones ----------

    def registrar_devolucion(self, fecha=None):
        """Marca el préstamo como devuelto (RF06). Por defecto con la fecha de hoy."""
        if not self.activo:
            raise ValueError("Este préstamo ya fue devuelto.")
        self.fecha_devolucion = fecha or date.today()
        self.estado = self.DEVUELTO

    # ---------- Conversión ----------

    @classmethod
    def desde_fila(cls, fila):
        return cls(
            id_usuario=validaciones.columna(fila, "IdUsuarios", "IdUsuario"),
            isbn=validaciones.columna(fila, "ISBN"),
            fecha_prestamo=validaciones.columna(fila, "FechaPrestamo"),
            fecha_devolucion=validaciones.columna(fila, "FechaDevolucion"),
            estado=validaciones.columna(fila, "Estado"),
            id_prestamo=validaciones.columna(fila, "IdPrestamo"),
        )

    def a_diccionario(self):
        return {
            "IdPrestamo": self.id_prestamo,
            "IdUsuario": self.id_usuario,
            "ISBN": self.isbn,
            "FechaPrestamo": self.fecha_prestamo.isoformat(),
            "FechaDevolucion": self.fecha_devolucion.isoformat() if self.fecha_devolucion else "",
            "Estado": self.estado,
        }

    def a_parametros(self):
        """Tupla para un INSERT parametrizado (fechas como texto AAAA-MM-DD)."""
        return (
            self.id_usuario,
            self.isbn,
            self.fecha_prestamo.isoformat(),
            self.fecha_devolucion.isoformat() if self.fecha_devolucion else None,
            self.estado,
        )

    def __str__(self):
        return f"Préstamo {self.id_prestamo or '(nuevo)'} - ISBN {self.isbn} - {self.estado}"
