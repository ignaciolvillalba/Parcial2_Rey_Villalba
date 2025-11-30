import json
import os

ruta_json="niveles.json"
ruta_csv="puntajes.csv"

def cargar_nivel(ruta_json):
    with open(ruta_json, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_puntaje(nombre, puntos, ruta="puntajes.csv"):
    with open(ruta, "a", encoding="utf-8") as f:
        f.write(f"{nombre},{puntos}\n")

def leer_estadisticas(ruta="puntajes.csv"):
    if not os.path.exists(ruta):
        return []
    puntajes = []
    with open(ruta, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip()
            if linea == "":
                continue  # salta líneas vacías

            partes = linea.split(",")
            if len(partes) != 2:
                continue  # ignora líneas mal formateadas

            nombre = partes[0].strip()
            puntos_texto = partes[1].strip()

            if puntos_texto.isdigit():
                puntos = int(puntos_texto)
                puntajes.append((nombre, puntos))
    puntajes.sort(key=lambda x: x[1], reverse=True)
    return puntajes[:10]

def mostrar_estadisticas():
    estadisticas = leer_estadisticas()
    if not estadisticas:
        print("No hay estadísticas disponibles.")
        return
    print("\n--- Top 10 ---")
    print("Nombre - Puntaje")
    for nombre, puntaje in estadisticas:
        print(f"{nombre} - {puntaje}")
    print("-------------------------------\n")