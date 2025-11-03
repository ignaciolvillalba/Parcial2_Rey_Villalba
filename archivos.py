import json
import csv
import os

# Carpeta donde está main.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def cargar_nivel(ruta="niveles.json"):
    ruta_completa = os.path.join(BASE_DIR, ruta)
    with open(ruta_completa, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_puntaje(nombre, puntos, ruta="puntajes.csv"):
    ruta_completa = os.path.join(BASE_DIR, ruta)
    with open(ruta_completa, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([nombre, puntos])

def leer_estadisticas(ruta="puntajes.csv"):
    ruta_completa = os.path.join(BASE_DIR, ruta)
    if not os.path.exists(ruta_completa):
        return []  # si no existe todavía, devolvemos lista vacía
    with open(ruta_completa, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        puntajes = [(fila[0], int(fila[1])) for fila in reader]
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