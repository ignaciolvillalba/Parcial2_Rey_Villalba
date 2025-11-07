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
            nombre = ""
            puntos_texto = ""
            coma_encontrada = False
            for c in linea:
                if c == "," and not coma_encontrada:
                    coma_encontrada = True
                elif not coma_encontrada:
                    if c != '"':  # ignoramos comillas
                        nombre += c
                else:
                    if c != "\n":
                        puntos_texto += c
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