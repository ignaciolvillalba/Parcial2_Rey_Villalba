import datos.config_json as config_json 

# Cargar datos desde el archivo JSON
datos = config_json.cargar_datos()

# Ventana
ANCHO = datos["config"]["ventana"]["ancho"]
ALTO = datos["config"]["ventana"]["alto"]
TITULO = datos["config"]["ventana"]["titulo"]

# Colores
COLOR_FONDO = tuple(datos["config"]["colores"]["fondo"])
COLOR_TEXTO_OSCURO = tuple(datos["config"]["colores"]["texto_oscuro"])
COLOR_TEXTO_CLARO = tuple(datos["config"]["colores"]["texto_claro"])
COLOR_PRIMARIO = tuple(datos["config"]["colores"]["primario"])
COLOR_SECUNDARIO = tuple(datos["config"]["colores"]["secundario"])
COLOR_GRIS = tuple(datos["config"]["colores"]["gris"])
COLOR_GRIS_CLARO = tuple(datos["config"]["colores"]["gris_claro"])

# Audio
VOLUMEN = datos["config"]["audio"]["volumen"]