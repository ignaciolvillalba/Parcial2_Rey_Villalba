import pygame
import generala
from datos.constantes import ALTO, FUENTE_CHICA
from archivos import guardar_puntaje
from render.render_elementos import render_juego, render_planilla_calculos, solicitar_nombre

def pantalla_juego(pantalla):
    clock = pygame.time.Clock()
    valores_dados = generala.tirar_dados(5)
    dados_bloqueados = [False] * 5
    tiradas_realizadas = 1
    botones_anotar = {}
    posibles = {}
    DADO_ANCHO, DADO_ALTURA = 80, 80
    ESPACIO = 100
    x_inicial = 40
    y_inicial = ALTO - DADO_ALTURA - 30
    CANDADO_ANCHO, CANDADO_ALTURA = 25, 25
    CANDADO_OFFSET_X = 20
    CANDADO_OFFSET_Y = 5
    boton_tirada = pygame.Rect(x_inicial + 5 * ESPACIO + 20, y_inicial, 250, 50)
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "salir"
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                return "menu"
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                pos = evento.pos
                if boton_tirada.collidepoint(pos) and tiradas_realizadas < 3:
                    nuevos = generala.tirar_dados(5)
                    for i in range(5):
                        if not dados_bloqueados[i]:
                            valores_dados[i] = nuevos[i]
                    tiradas_realizadas += 1
                for i in range(5):
                    x = x_inicial + i * ESPACIO
                    y = y_inicial
                    rect_candado = pygame.Rect(x + CANDADO_OFFSET_X, y - CANDADO_ALTURA - CANDADO_OFFSET_Y, CANDADO_ANCHO, CANDADO_ALTURA)
                    if rect_candado.collidepoint(pos):
                        dados_bloqueados[i] = not dados_bloqueados[i]
                if tiradas_realizadas == 3 and botones_anotar:
                    for categoria, rect in botones_anotar.items():
                        if rect.collidepoint(pos):
                            generala.planilla[categoria] = posibles[categoria]
                            valores_dados = generala.tirar_dados(5)
                            tiradas_realizadas = 1
                            dados_bloqueados = [False] * 5
                            if None not in generala.planilla.values():
                                total = 0
                                for puntos in generala.planilla.values():
                                    total += puntos
                                nombre = solicitar_nombre(pantalla, FUENTE_CHICA)
                                guardar_puntaje(nombre, total)
                                return "menu"
        render_juego(pantalla, valores_dados, dados_bloqueados, boton_tirada, tiradas_realizadas, x_inicial, y_inicial, ESPACIO, DADO_ANCHO, DADO_ALTURA, CANDADO_ALTURA, CANDADO_OFFSET_X, CANDADO_OFFSET_Y)
        posibles = generala.calcular_puntos_posibles(valores_dados, tiradas_realizadas, generala.planilla)
        botones_anotar = render_planilla_calculos(pantalla, posibles, 550, 20, tiradas_realizadas)
        pygame.display.flip()
        clock.tick(60)
