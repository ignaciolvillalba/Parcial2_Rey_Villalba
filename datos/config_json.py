import json
import os

ARCHIVO_CONFIG = "datos/config.json"

CONFIGURACION_DEFAULT = ARCHIVO_CONFIG

def guardar_datos(datos):
    carpeta = os.path.dirname(ARCHIVO_CONFIG)
    os.makedirs(carpeta, exist_ok=True)
    archivo = open(ARCHIVO_CONFIG, "w", encoding="utf-8")
    json.dump(datos, archivo, indent=4)
    archivo.close()


def cargar_datos():
    if not os.path.exists(ARCHIVO_CONFIG) or os.path.getsize(ARCHIVO_CONFIG) == 0:
        guardar_datos(CONFIGURACION_DEFAULT)
        return CONFIGURACION_DEFAULT
    archivo = open(ARCHIVO_CONFIG, "r", encoding="utf-8")
    datos = json.load(archivo)
    archivo.close()
    if "config" not in datos:
        guardar_datos(CONFIGURACION_DEFAULT)
        return CONFIGURACION_DEFAULT
    return datos
