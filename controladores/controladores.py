from servicios.service import Service

class Controlador:
    def __init__(self, servicio, tabla):
        self.servicio = servicio
        self.tabla = tabla

    def guardar(self, modelo):
        return self.servicio.registrar(
            self.tabla, modelo
        )

    def actualizar(self, modelo, codigo):
        return self.servicio.actualizar(
            self.tabla, modelo, codigo
        )

    def obtener_todo(self):
        return self.servicio.listar(self.tabla)

    def obtener_uno(self, columna, codigo):
        return self.servicio.listar_uno(
            self.tabla, columna, codigo
        )

    def eliminar(self, codigo):
        return self.servicio.eliminar(
            self.tabla, codigo
        )
        
class ControladorLibros(Controlador):
    def __init__(self, servicio):
        super().__init__(servicio, "Libros")
        
class ControladorAutores(Controlador):
    def __init__(self, servicio):
        super().__init__(servicio, "Autores")
        
class ControladorEditoriales(Controlador):
    def __init__(self, servicio):
        super().__init__(servicio, "Editoriales")
        
class ControladorUsuarios(Controlador):
    def __init__(self, servicio):
        super().__init__(servicio, "Usuarios")