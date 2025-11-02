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
simbolos={
    1: "Palo",
    2: "Bocha",
    3: "Arco",
    4: "Jugador",
    5: "Cancha",
    6: "Arquero"
}

def turno_jugador():
    dados = tirar_dados()
    for tiro in range(1, 4):
        print(f"\n<<< TIRO {tiro} de 3 >>>")
        mostrar_dados(dados)

        if tiro < 3:
            conservar = seleccionar_dados_a_conservar()
            nuevos = tirar_dados(5 - len(conservar))
            dados = [dados[i] if (i+1) in conservar else nuevos.pop(0) for i in range(5)]
    return dados
#Un turno completo, llama tirar_dados para el primer tiro, mostrar_dados los muestra en pantalla, llama a conservar dados y tira los dados no conservados hasta 3 tiros.

def tirar_dados(cantidad=5):
    return [random.randint(1, 6) for _ in range(cantidad)]
#Genera 5 dados aleatorios entre 1 y 6.

def mostrar_dados(dados):
    print("\nDADOS ACTUALES")
    print("Posición: ", end="")
    for i in range(len(dados)):
        print(f"({i+1})", end=" | ")
    print()
    print("Símbolo:  ", end="")
    for d in dados: #for dado in dados
        print(f"{simbolos[d]}", end=" | ")
    print()
    print("Valor:    ", end="")
    for d in dados:
        print(f"{d}", end=" | ")
    print("\n") 
#Muestra los dados actuales con su posición, símbolo (tematica) y valor(numero real).

def seleccionar_dados_a_conservar():
    eleccion = input("Ingrese las posiciones de los dados a conservar (ej: 1,3,5) o ENTER para ninguno: ")
    if eleccion.strip() == "":
        return []
    numeros = []
    numero_actual = ""
    for n in eleccion:
        if n.isdigit():
            numero_actual += n
        elif n == ",":
            if numero_actual:
                numeros.append(int(numero_actual))
                numero_actual = ""
    if numero_actual:
        numeros.append(int(numero_actual))
    return numeros
#Selecciona los dados conservados por el jugador, devuelve una lista con las posiciones de los dados a conservar.

def es_escalera(dados):
    ordenados = copy.deepcopy(dados)
    ordenados.sort()
    return ordenados == [1, 2, 3, 4, 5] or ordenados == [2, 3, 4, 5, 6]
#Crea una copia de los dados, los ordena y verifica si son una escalera.

def es_full(dados):
    ordenados = copy.deepcopy(dados)
    ordenados.sort()
    return (ordenados[0] == ordenados[1] == ordenados[2] and ordenados[3] == ordenados[4]) or (ordenados[0] == ordenados[1] and ordenados[2] == ordenados[3] == ordenados[4])
#Crea una copia de los dados, los ordena y verifica si son un full.

def es_poker(dados):
    ordenados = copy.deepcopy(dados)
    ordenados.sort()
    return ordenados[0] == ordenados[1] == ordenados[2] == ordenados[3] or ordenados[1] == ordenados[2] == ordenados[3] == ordenados[4]
#crea una copia de los dados, los ordena y verifica si son un poker.

def es_generala(dados):
    dado=dados[0]
    for d in dados:
        if d!=dado:
            return False
    return True
#Verifica si todos los dados son iguales(generala).

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
#LLama a las funciones de cada jugada y crea un diccionario que devuelve las jugadas con sus puntos.

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
#Anota los puntos en la planilla

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
#El jugador elige la categoría donde anotar, se verifican las condiciones y se anotan los puntos en la planilla (aca hice algo raro pq hay dos funciones que anotan en planilla pero creo que
# esta funcionando bien).

def mostrar_planilla(planilla):
    print("\n-------------------------")
    print("\nPLANILLA DE PUNTUACIONES")
    for categoria, puntos in planilla.items():
        estado = puntos if puntos is not None else "Sin anotar"
        print(f"- {categoria}: {estado} puntos")
    print("\n-------------------------\n")
#Muestra la planilla de puntuaciones actualizada.

def jugar():
    for i in planilla:
        planilla[i] = None
    while None in planilla.values():
        resultado = turno_jugador()
        anotacion(resultado, planilla)
        anotar(resultado, planilla)
        mostrar_planilla(planilla)
    print("\n¡Juego terminado! Todas las categorías fueron anotadas.")

