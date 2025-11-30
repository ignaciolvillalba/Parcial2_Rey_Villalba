import random
import copy
from archivos import cargar_nivel, guardar_puntaje

config = cargar_nivel("niveles.json")
simbolos = {}
for key, value in config["simbolos"].items():
    simbolos[int(key)] = value
categorias = config["categorias"]
jugadas_especiales = config["jugadas_especiales"]
planilla = {cat: None for cat in categorias}
dados = []

def tirar_dados(cantidad=5):
    dados = []
    for i in range(cantidad):
        dados.append(random.randint(1, 6))
    return dados

def turno_jugador():
    dados = tirar_dados(5)
    for tiro in range(1, 4):
        print("\n<<< TIRO " + str(tiro) + " de 3 >>>")
        mostrar_encabezado(planilla)
        mostrar_dados(dados)
        if tiro < 3:
            conservar = seleccionar_dados_a_conservar()
            if len(conservar) < 5:
                nuevos = tirar_dados(5 - len(conservar))
                dados_nuevos = []
                for i in range(5):
                    if (i + 1) in conservar:
                        dados_nuevos.append(dados[i])
                    else:
                        dados_nuevos.append(nuevos.pop(0))
                dados = dados_nuevos
    return dados, tiro

def mostrar_encabezado(planilla):
    total = 0
    for puntos in planilla.values():
        if puntos is not None:
            total += puntos
    print("\n==============================")
    print("PUNTAJE ACUMULADO: " + str(total))
    print("==============================")

def mostrar_dados(dados):
    print("\nDADOS ACTUALES")
    print("Posición: ", end="")
    for i in range(len(dados)):
        print("(" + str(i + 1) + ")", end=" | ")
    print()
    print("Símbolo:  ", end="")
    for d in dados:
        print(str(simbolos[d]), end=" | ")
    print()
    print("Valor:    ", end="")
    for d in dados:
        print(str(d), end=" | ")
    print("\n")

def seleccionar_dados_a_conservar():
    while True:
        eleccion = input("Ingrese las posiciones de los dados a conservar (ej: 1,3,5), 9 para conservar todos, o ENTER para ninguno: ").strip()
        if eleccion == "":
            return []
        if eleccion == "9":
            return [1, 2, 3, 4, 5]
        partes = eleccion.split(",")
        numeros = []
        valido = True
        for p in partes:
            p = p.strip()
            for i in p:
                if i not in "0123456789":
                    valido = False
                    break
            if not valido:
                break
            if p != "":
                n = int(p)
                if 1 <= n <= 5:
                    numeros.append(n)
                else:
                    valido = False
                    break
        if valido:
            return numeros
        else:
            print("Entrada inválida. Solo se permiten números entre 1 y 5.\n")

def es_escalera(dados):
    ordenados = copy.deepcopy(dados)
    ordenados.sort()
    if ordenados == [1, 2, 3, 4, 5]:
        return True
    elif ordenados == [2, 3, 4, 5, 6]:
        return True
    else:
        return False

def es_full(dados):
    ordenados = copy.deepcopy(dados)
    ordenados.sort()
    if ordenados[0] == ordenados[1] == ordenados[2] and ordenados[3] == ordenados[4]:
        return True
    elif ordenados[0] == ordenados[1] and ordenados[2] == ordenados[3] == ordenados[4]:
        return True
    else:
        return False

def es_poker(dados):
    ordenados = copy.deepcopy(dados)
    ordenados.sort()
    if ordenados[0] == ordenados[1] == ordenados[2] == ordenados[3]:
        return True
    elif ordenados[1] == ordenados[2] == ordenados[3] == ordenados[4]:
        return True
    else:
        return False

def es_generala(dados):
    dado = dados[0]
    for d in dados:
        if d != dado:
            return False
    return True

def calcular_puntos_posibles(dados, tiro, planilla):
    posibles = {}
    for i, (categoria, valor) in enumerate(planilla.items(), start=1):
        if valor is not None:
            continue
        if categoria == "Escalera":
            if es_escalera(dados):
                puntos = jugadas_especiales["Escalera"]
            else:
                puntos = 0
        elif categoria == "Full":
            if es_full(dados):
                puntos = jugadas_especiales["Full"]
            else:
                puntos = 0
        elif categoria == "Poker":
            if es_poker(dados):
                puntos = jugadas_especiales["Poker"]
            else:
                puntos = 0
        elif categoria == "Generala":
            if es_generala(dados):
                if tiro == 1:
                    puntos = jugadas_especiales["Generala Servida"]
                else:
                    puntos = jugadas_especiales["Generala"]
            else:
                puntos = 0
        else:
            numero = i
            puntos = 0
            for d in dados:
                if d == numero:
                    puntos += d
        posibles[categoria] = puntos
    return posibles

def anotar_jugada(dados, tiro, planilla):
    posibles = calcular_puntos_posibles(dados, tiro, planilla)
    print("\nOpciones disponibles para anotar:")
    contador = 1
    categorias_lista = []
    for categoria, puntos in posibles.items():
        print("[" + str(contador) + "] " + categoria + ": " + str(puntos) + " puntos")
        categorias_lista.append((categoria, puntos))
        contador += 1
    while True:
        eleccion = input("\nIngrese el número de la categoría en la que desea anotar: ").strip()
        if not eleccion.isdigit():
            print("Ingrese un número válido.")
            continue
        opcion = int(eleccion)
        if 1 <= opcion <= len(categorias_lista):
            break
        else:
            print("Opción no válida. Intente nuevamente.")
    categoria, puntos = categorias_lista[opcion - 1]
    planilla[categoria] = puntos
    print("Anotaste " + str(puntos) + " puntos en '" + categoria + "'.")
    mostrar_encabezado(planilla)

def mostrar_planilla(planilla):
    print("\n-------------------------")
    print("PLANILLA DE PUNTUACIONES")
    for categoria, puntos in planilla.items():
        if puntos is None:
            estado = "sin anotar"
        else:
            estado = str(puntos)
        print("- " + categoria + ": " + estado)
    total = 0
    for puntos in planilla.values():
        if puntos is not None:
            total += puntos
    print("PUNTAJE TOTAL: " + str(total))
    print("-------------------------\n")

def jugar():
    for i in planilla:
        planilla[i] = None
    while None in planilla.values():
        dados, tiro = turno_jugador()
        if es_generala(dados) and tiro == 1:
            print("\n¡¡GENERALA SERVIDA!! Ganaste automáticamente con 100 puntos.")
            planilla["Generala"] = jugadas_especiales["Generala Servida"]
            break
        anotar_jugada(dados, tiro, planilla)
    print("\n¡Juego terminado!")
    mostrar_planilla(planilla)
    nombre = input("Ingrese su nombre para guardar el puntaje: ")
    total = 0
    for puntos in planilla.values():
        if puntos is not None:
            total += puntos
    guardar_puntaje(nombre, total)

def mostrar_creditos():
    print("##########################################################################")
    print("Generala Tematica")
    print("##########################################################################")
    print("Autor/es: Mateo Rey, Ignacio Villalba")
    print("Fecha: Noviembre 2025")
    print("Materia: Programacion I")
    print("Docente: Prof. Martín Alejandro García")
    print("Carrera: Tecnicatura Universitaria en Programación")
    print("Mail de contacto: reym1414@gmail.com - ignacioezequielvillalba1@gmail.com")
    print("##########################################################################\n")
