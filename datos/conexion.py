import sqlite3
from contextlib import contextmanager
from pathlib import Path

RUTA_BD = Path(__file__).resolve().parent.parent / "AcaBiblioteca.db"


def obtener_conexion():
    conn = sqlite3.connect(str(RUTA_BD))
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn


@contextmanager
def conexion():
    conn = obtener_conexion()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()