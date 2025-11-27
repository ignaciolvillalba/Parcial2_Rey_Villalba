import json
import os

ARCHIVO_CONFIG = "datos/config.json"

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


def guardar_datos(datos):
    os.makedirs(os.path.dirname(ARCHIVO_CONFIG), exist_ok=True)
    with open(ARCHIVO_CONFIG, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4)

def cargar_datos():
    if not os.path.exists(ARCHIVO_CONFIG) or os.path.getsize(ARCHIVO_CONFIG) == 0:
        guardar_datos(CONFIGURACION_DEFAULT)
        return CONFIGURACION_DEFAULT

    with open(ARCHIVO_CONFIG, "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)

    if "config" not in datos:
        guardar_datos(CONFIGURACION_DEFAULT)
        return CONFIGURACION_DEFAULT

    return datos
