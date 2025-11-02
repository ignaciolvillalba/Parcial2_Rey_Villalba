import random
import copy
planilla = {
    "Dribbling": None,
    "Pases": None,
    "Defensa": None,
    "Tiros": None, 
    "Corner corto": None,
    "Corner largo": None,
    "Escalera": None,
    "Full": None,
    "Poker": None,
    "Penal!": None
}
caras={
    1: "Palo",
    2: "Bocha",
    3: "Arco",
    4: "Jugador",
    5: "Cancha",
    6: "Arquero"
}
def tirar_dados(cantidad=5):
    return [random.randint(1, 6) for _ in range(cantidad)]
def mostrar_dados(dados):
    print("\nDADOS ACTUALES")
    print("Posición: ", end="")
    for i in range(len(dados)):
        print(f"({i+1})", end=" | ")
    print()
    print("Símbolo:  ", end="")
    for d in dados:
        print(f"{caras[d]}", end=" | ")
    print()
    print("Valor:    ", end="")
    for d in dados:
        print(f"{d}", end=" | ")
    print("\n") 

def seleccionar_dados_a_conservar():
    eleccion = input("Ingrese las posiciones de los dados a conservar (ej: 1,3,5) o ENTER para ninguno: ")
    if eleccion.strip() == "":
        return []
    else:
        return [int(x) for x in eleccion.split(",") if x.strip().isdigit()]

def turno_jugador():
    dados = tirar_dados()
    for tiro in range(1, 4):
        print(f"\n<<< TIRO {tiro} de 3 >>>")
        mostrar_dados(dados)

        if tiro < 3:  # Solo pedir conservar si no es el último tiro
            conservar = seleccionar_dados_a_conservar()
            nuevos = tirar_dados(5 - len(conservar))
            # Reemplazar solo los que no se conservaron
            dados = [dados[i] if (i+1) in conservar else nuevos.pop(0) for i in range(5)]
    return dados

def es_escalera(dados):
    ordenados = copy.deepcopy(dados)
    ordenados.sort()
    return ordenados == [1, 2, 3, 4, 5] or ordenados == [2, 3, 4, 5, 6]

def es_full(dados):
    ordenados = copy.deepcopy(dados)
    ordenados.sort()
    return (ordenados[0] == ordenados[1] == ordenados[2] and ordenados[3] == ordenados[4]) or (ordenados[0] == ordenados[1] and ordenados[2] == ordenados[3] == ordenados[4])

def es_poker(dados):
    ordenados = copy.deepcopy(dados)
    ordenados.sort()
    return ordenados[0] == ordenados[1] == ordenados[2] == ordenados[3] or ordenados[1] == ordenados[2] == ordenados[3] == ordenados[4]

def es_generala(dados):
    dado=dados[0]
    for d in dados:
        if d!=dado:
            return False
    return True

def calcular_jugadas(dados):
    jugadas = {}
    if es_escalera(dados):
        jugadas["Escalera"] = 20
    else:
        jugadas["Escalera"] = 0
    if es_full(dados):
        jugadas["Full"] = 30
    else:
        jugadas["Full"] = 0
    if es_poker(dados):
        jugadas["Poker"] = 40
    else:
        jugadas["Poker"] = 0
    if es_generala(dados):
        jugadas["Penal!"] = 50
    else:
        jugadas["Penal!"] = 0 
    return jugadas

def anotacion(dados, planilla):
    print("Opciones disponibles para anotar:")
    jugadas = calcular_jugadas(dados)
    for i, (categoria, valor) in enumerate(planilla.items()):
        if planilla[categoria] is None:
            if categoria in jugadas:
                puntos = jugadas[categoria]
            else:
                numero = i + 1
                puntos = 0
                for d in dados:
                    if d == numero:
                        puntos += d
            print(f"- {categoria}: {puntos} puntos")

def anotar(dados, planilla):
    while True:
        categoria = input("Ingrese la categoría en la que desea anotar: ")
        if categoria in planilla and planilla[categoria] is None:
            break
        else:
            print("Categoría inválida o ya anotada. Intente nuevamente.")
    if categoria == "Escalera":
        puntos = 20 if es_escalera(dados) else 0
    elif categoria == "Full":
        puntos = 30 if es_full(dados) else 0
    elif categoria == "Poker":
        puntos = 40 if es_poker(dados) else 0
    elif categoria == "Penal!":
        puntos = 50 if es_generala(dados) else 0
    else:
        numero = list(planilla).index(categoria) + 1
        puntos = sum(d for d in dados if d == numero)
    planilla[categoria] = puntos
    print(f"Anotaste {puntos} puntos en la categoría '{categoria}'.")

def mostrar_planilla(planilla):
    print("\nPLANILLA DE PUNTUACIONES")
    for categoria, puntos in planilla.items():
        estado = puntos if puntos is not None else "Sin anotar"
        print(f"- {categoria}: {estado} puntos")

def jugar():
    # Reiniciar planilla cada vez que se juega
    for i in planilla:
        planilla[i] = None
    while None in planilla.values():
        resultado = turno_jugador()
        anotacion(resultado, planilla)
        anotar(resultado, planilla)
        mostrar_planilla(planilla)
    print("\n¡Juego terminado! Todas las categorías fueron anotadas.")

