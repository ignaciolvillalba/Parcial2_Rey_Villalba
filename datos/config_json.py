import json
import os

# Ruta del archivo de configuración
ARCHIVO_CONFIG = "datos/config.json"

# Configuración por defecto
CONFIGURACION_DEFAULT = {
    "config": {
        "ventana": {"ancho": 1000, "alto": 600, "titulo": "Generala Temática"},
        "audio": {"volumen": 0.7},
        "colores": {
            "fondo": [0, 0, 0],
            "primario": [0, 0, 180],
            "secundario": [0, 180, 0],
            "texto_claro": [255, 255, 255],
            "texto_oscuro": [0, 0, 0],
            "gris": [50, 50, 50],
            "gris_claro": [200, 200, 200]
        }
    }
}

# --------------------------
# Funciones básicas
# --------------------------
def guardar_datos(datos):
    """Guarda la configuración en el archivo JSON."""
    os.makedirs(os.path.dirname(ARCHIVO_CONFIG), exist_ok=True)
    with open(ARCHIVO_CONFIG, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4)

def cargar_datos():
    """Carga la configuración desde el archivo JSON, o crea una por defecto."""
    if not os.path.exists(ARCHIVO_CONFIG) or os.path.getsize(ARCHIVO_CONFIG) == 0:
        guardar_datos(CONFIGURACION_DEFAULT)
        return CONFIGURACION_DEFAULT

    with open(ARCHIVO_CONFIG, "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)

    # Validación mínima
    if "config" not in datos:
        guardar_datos(CONFIGURACION_DEFAULT)
        return CONFIGURACION_DEFAULT

    return datos

# --------------------------
# Funciones de actualización
# --------------------------
def actualizar_valor(seccion, clave, valor):
    """
    Actualiza un valor dentro de la configuración.
    Ejemplo: actualizar_valor("ventana", "ancho", 1280)
    """
    datos = cargar_datos()
    if seccion in datos["config"]:
        datos["config"][seccion][clave] = valor
        guardar_datos(datos)
    else:
        raise KeyError(f"La sección '{seccion}' no existe en la configuración.")

def actualizar_color(nombre_color, rgb):
    """
    Actualiza un color dentro de la configuración.
    Ejemplo: actualizar_color("fondo", [10, 20, 30])
    """
    datos = cargar_datos()
    if "colores" in datos["config"] and nombre_color in datos["config"]["colores"]:
        datos["config"]["colores"][nombre_color] = rgb
        guardar_datos(datos)
    else:
        raise KeyError(f"El color '{nombre_color}' no existe en la configuración.")
