"""Modelo Libro: representa una fila de la tabla Libros (clave primaria = ISBN)."""

from datetime import date

from modelos import validaciones


class Libro:
    def __init__(self, isbn, titulo, id_autor, id_editorial, categoria, anio=None, existencias=0,
                 autor="", editorial=""):
        self.isbn = isbn
        self.titulo = titulo
        self.id_autor = id_autor
        self.id_editorial = id_editorial
        self.categoria = categoria
        self.anio = anio
        self.existencias = existencias
        # Nombres para mostrar en la tabla (vienen del JOIN con Autores y Editoriales).
        # No se guardan en la tabla Libros, por eso no se validan.
        self.autor = autor or ""
        self.editorial = editorial or ""

    # ---------- Propiedades con validación ----------

    @property
    def isbn(self):
        return self._isbn

    @isbn.setter
    def isbn(self, valor):
        texto = validaciones.texto_obligatorio(valor, "ISBN", maximo=17)
        digitos = texto.replace("-", "")  # Se permite escribirlo con guiones
        if not digitos.isdigit() or len(digitos) not in (10, 13):
            raise ValueError("El ISBN debe tener 10 o 13 dígitos.")
        self._isbn = digitos

    @property
    def titulo(self):
        return self._titulo

    @titulo.setter
    def titulo(self, valor):
        self._titulo = validaciones.texto_obligatorio(valor, "Título", maximo=150)

    @property
    def id_autor(self):
        return self._id_autor

    @id_autor.setter
    def id_autor(self, valor):
        if valor is None or str(valor).strip() == "":
            raise ValueError("Debes escoger un autor.")
        self._id_autor = validaciones.entero(valor, "Autor", minimo=1)

    @property
    def id_editorial(self):
        return self._id_editorial

    @id_editorial.setter
    def id_editorial(self, valor):
        if valor is None or str(valor).strip() == "":
            raise ValueError("Debes escoger una editorial.")
        self._id_editorial = validaciones.entero(valor, "Editorial", minimo=1)

    @property
    def categoria(self):
        return self._categoria

    @categoria.setter
    def categoria(self, valor):
        self._categoria = validaciones.texto_obligatorio(valor, "Categoría", maximo=60)

    @property
    def anio(self):
        return self._anio

    @anio.setter
    def anio(self, valor):
        # En la BD el año puede quedar vacío (la columna "Año" no es NOT NULL)
        self._anio = validaciones.entero(valor, "Año", minimo=1, maximo=date.today().year, obligatorio=False)

    @property
    def existencias(self):
        return self._existencias

    @existencias.setter
    def existencias(self, valor):
        self._existencias = validaciones.entero(valor, "Existencias", minimo=0)

    @property
    def disponible(self):
        """True si queda al menos un ejemplar para prestar."""
        return self.existencias > 0

    # ---------- Conversión desde / hacia otros formatos ----------

    @classmethod
    def desde_fila(cls, fila):
        """Crea un Libro a partir de una fila de SQLite (o un diccionario)."""
        return cls(
            isbn=validaciones.columna(fila, "ISBN"),
            titulo=validaciones.columna(fila, "Titulo"),
            id_autor=validaciones.columna(fila, "IdAutor"),
            id_editorial=validaciones.columna(fila, "IdEditorial"),
            categoria=validaciones.columna(fila, "Categoria"),
            anio=validaciones.columna(fila, "Año", "Anio"),
            existencias=validaciones.columna(fila, "Existencias"),
            autor=validaciones.columna(fila, "Autor"),
            editorial=validaciones.columna(fila, "Editorial"),
        )

    @classmethod
    def desde_formulario(cls, datos):
        """Crea un Libro con el diccionario que devuelve VistaLibros.obtener_datos()."""
        return cls.desde_fila(datos)

    def a_diccionario(self):
        """Diccionario con las claves que usa VistaLibros (cargar_tabla y llenar_formulario)."""
        return {
            "ISBN": self.isbn,
            "Titulo": self.titulo,
            "IdAutor": self.id_autor,
            "IdEditorial": self.id_editorial,
            "Categoria": self.categoria,
            "Anio": self.anio if self.anio is not None else "",
            "Existencias": self.existencias,
            "Autor": self.autor,
            "Editorial": self.editorial,
        }

    def a_parametros(self):
        """
        Tupla en el orden de las columnas de la tabla Libros, para usar en un
        INSERT con consulta parametrizada:
            INSERT INTO Libros (ISBN, Titulo, IdAutor, IdEditorial, Categoria, "Año", Existencias)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        return (self.isbn, self.titulo, self.id_autor, self.id_editorial,
                self.categoria, self.anio, self.existencias)

    def __str__(self):
        return f"{self.titulo} ({self.isbn})"
