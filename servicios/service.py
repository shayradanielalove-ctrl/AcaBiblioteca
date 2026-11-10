from modelos.libro import Libro
from modelos.autor import Autor
from modelos.editorial import Editorial
from modelos.usuario import Usuario

class Service:
    def __init__(self, gestor):
        self.gestor = gestor

        self.identificadores = {
            "Libros": "ISBN",
            "Autores": "IdAutor",
            "Editoriales": "IdEditorial",
            "Usuarios": "IdUsuarios"
        }

        self.permitidos = {
            "Libros": {
                "ISBN", "Titulo", "IdAutor",
                "IdEditorial", "Categoria", "Año",
                "Existencias"
            },
            "Autores": {
                "IdAutor", "Nombre", "Apellido"
            },
            "Editoriales": {
                "IdEditorial", "Nombre"
            },
            "Usuarios": {
                "IdUsuarios", "Nombre", "Apellido",
                "Documento", "Telefono", "Correo"
            }
        }

        
    def _preparar_datos(self, tabla, modelo, actualizar=False):
        if tabla not in self.permitidos:
            return None

        datos = modelo.a_diccionario()

        if not datos:
            return None

        # Los nombres del autor y la editorial son solo para mostrar.
        # No son columnas de la tabla Libros.
        if tabla == "Libros":
            datos.pop("Autor", None)
            datos.pop("Editorial", None)

            # El modelo usa "Anio", pero SQLite tiene la columna "Año".
            if "Anio" in datos:
                datos["Año"] = datos.pop("Anio")

        # En las demás tablas, el identificador se utiliza en el WHERE.
        # No debe modificarse durante la actualización.
        elif actualizar:
            tipo = self.identificadores[tabla]
            datos.pop(tipo, None)

        if not set(datos.keys()).issubset(self.permitidos[tabla]):
            return None

        return datos


    def registrar(self, tabla, modelo):
        datos = self._preparar_datos(tabla, modelo)

        if not datos:
            return False

        return self.gestor.guardar(tabla, datos)


    def actualizar(self, tabla, modelo, codigo):
        if tabla not in self.identificadores:
            return False

        datos = self._preparar_datos(tabla, modelo, actualizar=True)

        if not datos:
            return False

        tipo = self.identificadores[tabla]

        return self.gestor.editar(tabla, tipo, codigo, datos)


    def listar(self, tabla):
        modelos = {
            "Libros": Libro,
            "Autores": Autor,
            "Editoriales": Editorial,
            "Usuarios": Usuario
        }

        if tabla not in modelos:return None

        filas = self.gestor.obtener_todo(tabla)

        return [modelos[tabla].desde_fila(fila)for fila in filas]


    def listar_uno(self, tabla, columna, codigo):
        modelos = {
            "Libros": Libro,
            "Autores": Autor,
            "Editoriales": Editorial,
            "Usuarios": Usuario
        }

        if tabla not in modelos:
            return None

        if columna not in self.permitidos[tabla]:
            return None

        fila = self.gestor.obtener_por(tabla, columna, codigo)

        if fila is None:
            return None

        return modelos[tabla].desde_fila(fila) 

        
    def eliminar(self, tabla, codigo):
        if tabla not in self.identificadores:
            return False

        tipo = self.identificadores[tabla]

        return self.gestor.eliminar(tabla, tipo, codigo)