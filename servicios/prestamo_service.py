from modelos.prestamo import Prestamo
from datetime import date

class PrestamoService:

    def __init__(self, gestor):
        self.gestor = gestor

    def guardar_prestamo(self, prestamo):

        datos = prestamo.a_diccionario()

        id_usuario = datos["IdUsuarios"]
        isbn = datos["ISBN"]

        usuario = self.gestor.obtener_por("Usuarios", "IdUsuarios",id_usuario)

        if usuario is None: return "Usuario no existe."

        libro = self.gestor.obtener_por("Libros", "ISBN", isbn)

        if libro is None: return "Libro no existe."

        if libro["Existencias"] <= 0: return "No hay existencias."

        consultas = [
        ("INSERT INTO Prestamos (IdUsuarios, ISBN, FechaPrestamo, FechaDevolucion, Estado) VALUES (?, ?, ?, ?, ?)",
            (id_usuario,isbn,datos["FechaPrestamo"],datos["FechaDevolucion"],"Prestado"),True),
        
        ("UPDATE Libros SET Existencias = Existencias - 1 WHERE ISBN = ? AND Existencias > 0", (isbn,), True)
        ]

        resultado = self.gestor.transaccion(consultas)
        return resultado

    def devolucion(self, codigo):

        prestamo = self.gestor.obtener_por("Prestamos", "IdPrestamo",codigo)

        if prestamo is None: return "Préstamo no existe."

        if prestamo["Estado"] != "Prestado": return "Prestamo ya fue devuelto."

        isbn = prestamo["ISBN"]

        consultas = [
        ("UPDATE Prestamos SET Estado = ?, FechaDevolucion = ? WHERE IdPrestamo = ? AND Estado = 'Prestado'", ("Devuelto", date.today().isoformat(), codigo), True),
        
        ("UPDATE Libros SET Existencias = Existencias + 1 WHERE ISBN = ?", (isbn,), True)
        ]

        return self.gestor.transaccion(consultas)

    def listar_todo(self):

        filas = self.gestor.obtener_todo("Prestamos")

        if filas is None: return None

        return [Prestamo.desde_fila(fila) for fila in filas]

    def listar_uno(self, codigo):

        fila = self.gestor.obtener_por("Prestamos", "IdPrestamo",codigo)

        if fila is None: return None

        return Prestamo.desde_fila(fila)