import sqlite3
from datos.conexion import obtener_conexion
from pathlib import Path
from pendulum import date



# ==============================
# Consulta con JOIN para libros
# ==============================
_SELECT_LIBROS = """
    SELECT l.ISBN,
            l.Titulo,
            l.Categoria,
            l.Año,
            l.Existencias,
            l.IdAutor,
            l.IdEditorial,
            a.Nombre || ' ' || a.Apellido AS Autor,
            e.Nombre AS Editorial
    FROM Libros l
    JOIN Autores a ON a.IdAutor = l.IdAutor
    JOIN Editoriales e ON e.IdEditorial = l.IdEditorial
"""

# ==============================
# Gestor genérico (CRUD)
# ==============================
class GestorSQL:

    def __init__(self):
        self.conn = obtener_conexion()
        self.cur = self.conn.cursor()
        self.ultimo_error = ""   # el service lo usa para dar mensajes claros

    def guardar(self, tabla, datos):
        columnas = ", ".join(datos.keys())
        marcas = ", ".join(["?"] * len(datos))
        try:
            self.cur.execute(
                f"INSERT INTO {tabla} ({columnas}) VALUES ({marcas})",
                tuple(datos.values()),
            )
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            self.conn.rollback()
            self.ultimo_error = str(e)
            print(f"Error al guardar: {e}")
            return False
 
    def obtener_todo(self, tabla):
        self.cur.execute(f"SELECT * FROM {tabla}")
        return [dict(fila) for fila in self.cur.fetchall()]
 
    def obtener_por(self, tabla, tipo, valor):
        """Devuelve un solo registro (dict) o None."""
        self.cur.execute(f"SELECT * FROM {tabla} WHERE {tipo}=?", (valor,))
        fila = self.cur.fetchone()
        return dict(fila) if fila else None

    def eliminar(self, tabla, tipo, valor):
        try:
            self.cur.execute(f"DELETE FROM {tabla} WHERE {tipo}=?", (valor,))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            self.conn.rollback()
            self.ultimo_error = str(e)
            print(f"Error al eliminar: {e}")
            return False

    def editar(self, tabla, tipo, valor, datos):
        columnas = ", ".join([f"{columna}=?" for columna in datos.keys()])
        valores = tuple(datos.values()) + (valor,)
        try:
            self.cur.execute(f"UPDATE {tabla} SET {columnas} WHERE {tipo}=?", valores)
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            self.conn.rollback()
            self.ultimo_error = str(e)
            print(f"Error al editar: {e}")
            return False
        
    def transaccion(self, consultas):
        try:
            for consulta in consultas:
                sql, datos, comprobar = consulta

                self.cur.execute(sql, datos)

                if comprobar and self.cur.rowcount != 1:
                    raise sqlite3.IntegrityError(
                        "La operación no modificó el registro esperado."
                    )

            self.conn.commit()
            return True

        except sqlite3.Error as e:
            self.conn.rollback()
            self.ultimo_error = str(e)
            print(f"Error en transacción: {e}")
            return False


    def cancelar(self):
        self.conn.rollback()


    # ==============================
    # Consulta de búsqueda
    # ==============================
    def buscar_libros(self, texto):
        texto = (texto or "").strip()
        try:
            if not texto:
                self.cur.execute(_SELECT_LIBROS + " ORDER BY l.Titulo")
            else:
                filtro = f"%{texto}%"
                self.cur.execute(
                    _SELECT_LIBROS
                    + """
                    WHERE l.ISBN LIKE ?
                    OR l.Titulo LIKE ?
                    OR l.Categoria LIKE ?
                    OR (a.Nombre || ' ' || a.Apellido) LIKE ?
                    OR e.Nombre LIKE ?
                    ORDER BY l.Titulo
                    """,
                    (filtro, filtro, filtro, filtro, filtro),
                )
            return [dict(fila) for fila in self.cur.fetchall()]
        except sqlite3.Error as e:
            print(f"Error en búsqueda: {e}")
            return []

    def cerrar(self):
        self.conn.close()
