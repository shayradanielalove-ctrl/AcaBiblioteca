"""
Funciones de validación que comparten todos los modelos.

Cada función recibe un valor (por ejemplo lo que el usuario escribió en una
caja de texto), lo limpia y lo devuelve listo para guardar.
Si el valor no sirve, lanza un ValueError con un mensaje claro en español,
que el servicio o el controlador pueden mostrar en pantalla.
"""

import re
from datetime import date, datetime

PATRON_CORREO = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def columna(fila, *nombres):
    """
    Lee una columna de una fila de la base de datos (sqlite3.Row o diccionario).
    Se pueden dar varios nombres porque en la BD algunos están escritos distinto,
    por ejemplo "Año" o "Anio", "Ideditorial" o "IdEditorial".
    Si no encuentra ninguno, devuelve None.
    """
    claves = fila.keys()
    for nombre in nombres:
        if nombre in claves:
            return fila[nombre]
    return None


def texto_obligatorio(valor, campo, maximo=100):
    """Texto que no puede quedar vacío. Ejemplo: el título de un libro."""
    texto = "" if valor is None else str(valor).strip()
    if not texto:
        raise ValueError(f"El campo {campo} es obligatorio.")
    if len(texto) > maximo:
        raise ValueError(f"El campo {campo} no puede tener más de {maximo} caracteres.")
    return texto


def entero(valor, campo, minimo=None, maximo=None, obligatorio=True):
    """
    Número entero. Acepta 5 o "5" (lo que llega de una caja de texto es texto).
    Si no es obligatorio y viene vacío, devuelve None.
    """
    if valor is None or str(valor).strip() == "":
        if obligatorio:
            raise ValueError(f"El campo {campo} es obligatorio.")
        return None
    try:
        numero = int(str(valor).strip())
    except ValueError:
        raise ValueError(f"El campo {campo} debe ser un número entero.") from None
    if minimo is not None and numero < minimo:
        raise ValueError(f"El campo {campo} no puede ser menor que {minimo}.")
    if maximo is not None and numero > maximo:
        raise ValueError(f"El campo {campo} no puede ser mayor que {maximo}.")
    return numero


def id_opcional(valor, campo):
    """
    Identificador (Id) de una tabla. Puede ser None cuando el objeto es nuevo,
    porque SQLite lo asigna solo con AUTOINCREMENT al insertar.
    """
    return entero(valor, campo, minimo=1, obligatorio=False)


def correo(valor, campo="Correo"):
    texto = texto_obligatorio(valor, campo, maximo=100)
    if not PATRON_CORREO.match(texto):
        raise ValueError(f"El campo {campo} no tiene un formato válido (ejemplo: ana@gmail.com).")
    return texto


def solo_digitos(valor, campo, minimo, maximo):
    """Texto formado solo por números, como un documento o un teléfono."""
    texto = texto_obligatorio(valor, campo, maximo=maximo)
    if not texto.isdigit():
        raise ValueError(f"El campo {campo} solo puede tener números.")
    if len(texto) < minimo:
        raise ValueError(f"El campo {campo} debe tener al menos {minimo} dígitos.")
    return texto


def fecha(valor, campo, obligatorio=True):
    """
    Fecha. Acepta un objeto date o un texto "AAAA-MM-DD"
    (así guarda SQLite las fechas). Devuelve un objeto date.
    """
    if valor is None or str(valor).strip() == "":
        if obligatorio:
            raise ValueError(f"El campo {campo} es obligatorio.")
        return None
    if isinstance(valor, datetime):
        return valor.date()
    if isinstance(valor, date):
        return valor
    try:
        return datetime.strptime(str(valor).strip(), "%Y-%m-%d").date()
    except ValueError:
        raise ValueError(f"El campo {campo} debe tener el formato AAAA-MM-DD.") from None
