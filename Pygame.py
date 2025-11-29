import pygame, sys
from datos import constantes
from gestor_eventos.gestor_eventos import gestionar_eventos
from audio import gestor_audio
from render import render_pantalla
import archivos
import generala
from render.render_elementos import render_juego, render_planilla_calculos, render_creditos

pygame.init()
pantalla = pygame.display.set_mode((constantes.ANCHO, constantes.ALTO))
pygame.display.set_caption(constantes.TITULO)
clock = pygame.time.Clock()
pantalla_actual = "menu"
gestor_audio.reproducir_musica()

valores_dados = [1, 2, 3, 4, 5]
dados_bloqueados = [False] * 5
tiradas_realizadas = 0
mostrar_menu_jugadas = False
botones_anotar = {}
posibles = {}

# Layout de dados y candados
DADO_W, DADO_H = 120, 120
ESPACIO = 130
x_inicial = 30
y_inicial = constantes.ALTO - DADO_H - 30
CANDADO_W, CANDADO_H = 40, 40
CANDADO_OFFSET_X = (DADO_W - CANDADO_W) // 2
CANDADO_OFFSET_Y = 10
boton_tirada = pygame.Rect(x_inicial + 5 * ESPACIO + 20, y_inicial, 250, 50)

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

        # Pantallas principales
        if pantalla_actual == "menu":
            botones = render_pantalla.pantalla_principal(pantalla)
            pantalla_actual, tiradas_realizadas, dados_bloqueados = gestionar_eventos(
                evento, pantalla_actual, botones, tiradas_realizadas, botones_anotar, posibles, dados_bloqueados
            )

        elif pantalla_actual == "opciones":
            botones = render_pantalla.pantalla_opciones(pantalla)
            pantalla_actual, tiradas_realizadas, dados_bloqueados = gestionar_eventos(
                evento, pantalla_actual, botones, tiradas_realizadas, botones_anotar, posibles, dados_bloqueados
            )

        elif pantalla_actual == "estadisticas":
            registros = archivos.leer_estadisticas()
            from render.render_elementos import render_estadisticas
            render_estadisticas(pantalla, None, fuente, fuente_small, registros)
            botones = [{"accion": "volver", "rect": pygame.Rect(constantes.ANCHO-200, constantes.ALTO-80, 160, 40)}]
            pantalla_actual, tiradas_realizadas, dados_bloqueados = gestionar_eventos(
                evento, pantalla_actual, botones, tiradas_realizadas, botones_anotar, posibles, dados_bloqueados
            )

        elif pantalla_actual == "creditos":
            render_creditos(pantalla)
            botones = [{"accion": "volver", "rect": pygame.Rect(constantes.ANCHO-200, constantes.ALTO-80, 160, 40)}]
            pantalla_actual, tiradas_realizadas, dados_bloqueados = gestionar_eventos(
                evento, pantalla_actual, botones, tiradas_realizadas, botones_anotar, posibles, dados_bloqueados
            )

        elif pantalla_actual == "jugar":
            # Render del juego
            render_juego(
                pantalla, valores_dados, dados_bloqueados, boton_tirada,
                tiradas_realizadas, mostrar_menu_jugadas,
                x_inicial, y_inicial, ESPACIO, DADO_W, DADO_H,
                CANDADO_H, CANDADO_OFFSET_X, CANDADO_OFFSET_Y
            )

            # Calcular posibles puntos y renderizar planilla con botones de anotar
            posibles = generala.calcular_puntos_posibles(valores_dados, tiradas_realizadas, generala.planilla)
            botones_anotar = render_planilla_calculos(pantalla, posibles, 960, 50, tiradas_realizadas)

            # Eventos de clic
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                pos = evento.pos

                # Botón tirar dados
                if boton_tirada.collidepoint(pos) and tiradas_realizadas < 3 and not mostrar_menu_jugadas:
                    nuevos = generala.tirar_dados(5)
                    for i in range(5):
                        if not dados_bloqueados[i]:
                            valores_dados[i] = nuevos[i]
                    tiradas_realizadas += 1
                    if tiradas_realizadas == 3:
                        mostrar_menu_jugadas = True

                # Candados
                for i in range(5):
                    x = x_inicial + i * ESPACIO
                    y = y_inicial
                    rect_candado = pygame.Rect(
                        x + CANDADO_OFFSET_X,
                        y - CANDADO_H - CANDADO_OFFSET_Y,
                        CANDADO_W, CANDADO_H
                    )
                    if rect_candado.collidepoint(pos):
                        dados_bloqueados[i] = not dados_bloqueados[i]

                # Botones de anotar
                if tiradas_realizadas == 3 and botones_anotar:
                    for categoria, rect in botones_anotar.items():
                        if rect.collidepoint(pos):
                            generala.planilla[categoria] = posibles[categoria]
                            tiradas_realizadas = 0
                            dados_bloqueados = [False] * 5
                            mostrar_menu_jugadas = False
                            if None not in generala.planilla.values():
                                pantalla_actual = "final"

    pygame.display.flip()
    clock.tick(60)