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

    def registrar(self, tabla, modelo):
        if tabla not in self.permitidos:
            return False

        datos = modelo.a_diccionario()

        if not datos:
            return False

        if not set(datos.keys()).issubset(self.permitidos[tabla]):
            return False

        return self.gestor.guardar(tabla, datos)

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

    def actualizar(self, tabla, modelo, codigo):
        if tabla not in self.identificadores:
            return False

        datos = modelo.a_diccionario()

        if not datos or not set(datos).issubset(self.permitidos[tabla]):
            return False

        tipo = self.identificadores[tabla]

        return self.gestor.editar(tabla, tipo, codigo, datos)

    def eliminar(self, tabla, codigo):
        if tabla not in self.identificadores:
            return False

        tipo = self.identificadores[tabla]

        return self.gestor.eliminar(tabla, tipo, codigo)