"""
Estilos visuales del Sistema de Gestión de Biblioteca.

Todas las ventanas deben tomar sus colores y fuentes de este archivo.
Así, si se quiere cambiar el diseño, se cambia aquí una sola vez.

Uso:
    from utils import estilos
    ctk.CTkLabel(..., text_color=estilos.COLOR_TEXTO, font=estilos.FUENTE_TITULO)
"""

# ==============================
# COLORES GENERALES
# ==============================
COLOR_FONDO = "#eedad4"           # Fondo de toda la ventana
COLOR_PANEL = "#f3e7e4"           # Fondo de los paneles (formulario y tabla)
COLOR_BARRA = "#f7efed"           # Fondo de la barra de búsqueda
COLOR_TEXTO = "#784870"           # Títulos y etiquetas (morado)
COLOR_TEXTO_SECUNDARIO = "#5e3857"  # Texto de ayuda dentro de las cajas

# ==============================
# CAJAS DE TEXTO Y LISTAS
# ==============================
COLOR_CAMPO = "#bb99ac"           # Fondo de las cajas de texto (lila)
COLOR_CAMPO_TEXTO = "#4a2c45"     # Texto que escribe el usuario
COLOR_CAMPO_BORDE = "#bb99ac"

# ==============================
# TABLA
# ==============================
COLOR_TABLA_FONDO = "#f7efed"
COLOR_TABLA_ENCABEZADO = "#bb99ac"
COLOR_TABLA_SELECCION = "#d9bfcc"

# ==============================
# BOTONES (color normal / color al pasar el mouse)
# ==============================
COLOR_BOTON_PRINCIPAL = "#784870"        # Guardar
COLOR_BOTON_PRINCIPAL_HOVER = "#5e3857"
COLOR_BOTON_PELIGRO = "#b5536b"          # Eliminar
COLOR_BOTON_PELIGRO_HOVER = "#94405a"
COLOR_BOTON_SECUNDARIO = "#bb99ac"       # Limpiar
COLOR_BOTON_SECUNDARIO_HOVER = "#a07f92"
COLOR_BOTON_BUSCAR = "#ead7d1"           # Buscar (claro, como en el mockup)
COLOR_BOTON_BUSCAR_HOVER = "#dcc3bb"
COLOR_TEXTO_BOTON = "#ffffff"

# ==============================
# FUENTES (nombre, tamaño, estilo)
# ==============================
FUENTE_FAMILIA = "Times New Roman"
FUENTE_TITULO = (FUENTE_FAMILIA, 36, "bold")
FUENTE_SUBTITULO = (FUENTE_FAMILIA, 18, "bold")
FUENTE_ETIQUETA = (FUENTE_FAMILIA, 17)
FUENTE_CAMPO = (FUENTE_FAMILIA, 14)
FUENTE_BOTON = (FUENTE_FAMILIA, 14, "bold")
FUENTE_TABLA = (FUENTE_FAMILIA, 12)
FUENTE_TABLA_ENCABEZADO = (FUENTE_FAMILIA, 13, "bold")

# ==============================
# MEDIDAS
# ==============================
RADIO_BORDE = 15        # Qué tan redondeadas son las esquinas
ANCHO_CAMPO = 200       # Ancho de las cajas del formulario
ALTO_CAMPO = 32