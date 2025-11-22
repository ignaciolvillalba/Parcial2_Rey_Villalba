import random
import copy
from archivos import cargar_nivel, guardar_puntaje

# === Cargar configuración desde JSON ===
config = cargar_nivel("niveles.json")

simbolos = {int(k): v for k, v in config["simbolos"].items()}
categorias = config["categorias"]
jugadas_especiales = config["jugadas_especiales"]

# Planilla inicial
planilla = {cat: None for cat in categorias}

# --- Utilidades ---
def tirar_dados(cantidad=5):
    return [random.randint(1, 6) for _ in range(cantidad)]

def mostrar_encabezado(planilla):
    total = sum(p for p in planilla.values() if p is not None)
    print("\n==============================")
    print(f"PUNTAJE ACUMULADO: {total}")
    print("==============================")

def mostrar_dados(dados):
    print("\nDADOS ACTUALES")
    print("Posición: ", end="")
    for i in range(len(dados)):
        print(f"({i+1})", end=" | ")
    print()
    print("Símbolo:  ", end="")
    for d in dados:
        print(f"{simbolos[d]}", end=" | ")
    print()
    print("Valor:    ", end="")
    for d in dados:
        print(f"{d}", end=" | ")
    print("\n")

# --- Selección de dados ---
def seleccionar_dados_a_conservar():
    while True:
        eleccion = input("Ingrese las posiciones de los dados a conservar (ej: 1,3,5), 9 para conservar todos, o ENTER para ninguno: ").strip()
        if eleccion == "":
            return []
        if eleccion == "9":
            return [1, 2, 3, 4, 5]
        numeros = []
        numero_actual = ""
        valido = True
        for n in eleccion:
            if n in "12345":
                numero_actual += n
            elif n == ",":
                if numero_actual:
                    valor = int(numero_actual)
                    if 1 <= valor <= 5:
                        numeros.append(valor)
                    else:
                        print(f"El número {valor} no es válido. Solo se permiten 1 a 5.")
                        valido = False
                        break
                    numero_actual = ""
        if numero_actual:
            valor = int(numero_actual)
            if 1 <= valor <= 5:
                numeros.append(valor)
            else:
                print(f"El número {valor} no es válido. Solo se permiten 1 a 5.")
                valido = False
        if valido:
            return numeros
        else:
            print("Intente nuevamente.\n")

# --- Jugadas especiales ---
def es_escalera(dados):
    ordenados = copy.deepcopy(dados)
    ordenados.sort()
    return ordenados == [1,2,3,4,5] or ordenados == [2,3,4,5,6]

def es_full(dados):
    ordenados = copy.deepcopy(dados)
    ordenados.sort()
    return (ordenados[0]==ordenados[1]==ordenados[2] and ordenados[3]==ordenados[4]) or \
           (ordenados[0]==ordenados[1] and ordenados[2]==ordenados[3]==ordenados[4])

def es_poker(dados):
    ordenados = copy.deepcopy(dados)
    ordenados.sort()
    return (ordenados[0]==ordenados[1]==ordenados[2]==ordenados[3]) or \
           (ordenados[1]==ordenados[2]==ordenados[3]==ordenados[4])

def es_generala(dados):
    dado = dados[0]
    for d in dados:
        if d != dado:
            return False
    return True

# --- Turno del jugador ---
def turno_jugador():
    dados = tirar_dados()
    for tiro in range(1, 4):
        print(f"\n<<< TIRO {tiro} de 3 >>>")
        mostrar_encabezado(planilla)
        mostrar_dados(dados)

        if tiro < 3:
            conservar = seleccionar_dados_a_conservar()
            if len(conservar) < 5:
                nuevos = tirar_dados(5 - len(conservar))
                dados_nuevos = []
                for i in range(5):
                    if (i+1) in conservar:   # posiciones 1–5
                        dados_nuevos.append(dados[i])
                    else:
                        dados_nuevos.append(nuevos.pop(0))
                dados = dados_nuevos
    return dados, tiro

# --- Anotar ---
def anotar_jugada(dados, tiro, planilla):
    print("\nOpciones disponibles para anotar:")
    categorias = list(planilla.keys())
    posibles = {}

    for i, categoria in enumerate(categorias, start=1):
        if planilla[categoria] is not None:
            continue
        if categoria == "Escalera":
            puntos = jugadas_especiales["Escalera"] if es_escalera(dados) else 0
        elif categoria == "Full":
            puntos = jugadas_especiales["Full"] if es_full(dados) else 0
        elif categoria == "Poker":
            puntos = jugadas_especiales["Poker"] if es_poker(dados) else 0
        elif categoria == "Generala":
            if es_generala(dados):
                puntos = jugadas_especiales["GeneralaServida"] if tiro == 1 else jugadas_especiales["Generala"]
            else:
                puntos = 0
        else:
            # categorías numéricas
            numero = categorias.index(categoria) + 1
            puntos = sum(d for d in dados if d == numero)
        posibles[i] = (categoria, puntos)
        print(f"[{i}] {categoria}: {puntos} puntos")

    # --- Validación robusta de entrada ---
    while True:
        eleccion = input("\nIngrese el número de la categoría en la que desea anotar: ").strip()
        if eleccion == "":
            print("Debe ingresar un número. Intente nuevamente.")
            continue
        es_digito = True
        for n in eleccion:
            if n not in "0123456789":
                es_digito = False
                break
            if not es_digito:
                print("Ingrese un número válido.")
                continue
        opcion = int(eleccion)
        if opcion in posibles:
            break
        else:
            print("Opción no válida. Intente nuevamente.")
    categoria, puntos = posibles[opcion]
    planilla[categoria] = puntos
    print(f"Anotaste {puntos} puntos en '{categoria}'.")
    mostrar_encabezado(planilla)

def mostrar_planilla(planilla):
    print("\n-------------------------")
    print("PLANILLA DE PUNTUACIONES")
    for categoria, puntos in planilla.items():
        estado = puntos if puntos is not None else "Sin anotar"
        print(f"- {categoria}: {estado}")
    total = sum(p for p in planilla.values() if p is not None)
    print(f"PUNTAJE TOTAL: {total}")
    print("-------------------------\n")

# --- Juego completo ---
def jugar():
    for i in planilla:
        planilla[i] = None
    while None in planilla.values():
        dados, tiro = turno_jugador()
        if es_generala(dados) and tiro == 1:
            print("\n¡¡GENERALA SERVIDA!! Ganaste automáticamente con 100 puntos.")
            planilla["Generala"] = jugadas_especiales["GeneralaServida"]
            break
        anotar_jugada(dados, tiro, planilla)
        mostrar_planilla(planilla)
    print("\n¡Juego terminado!")
    mostrar_planilla(planilla)
    # Guardar puntaje en CSV
    nombre = input("Ingrese su nombre para guardar el puntaje: ")
    total = sum(p for p in planilla.values() if p is not None)
    guardar_puntaje(nombre, total)

def mostrar_creditos():
    print("################################")
    print("Generala Tematica ")
    print("#######################################################")
    print("Autor/es: Mateo Rey, Ignacio Villalba")
    print("Fecha: Noviembre 2025")
    print("Materia: Programacion I")
    print("Docente: Prof. Martín Alejandro García")
    print("Carrera: Tecnicatura Universitaria en Programación")
    print("Mail de contacto:  - ignacioezequielvillalba1@gmail.com")
    print("#######################################################\n")