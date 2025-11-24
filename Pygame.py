import pygame, sys
from datos import constantes
from gestor_eventos import gestor_eventos
from audio import gestor_audio
from render import render_pantalla
import archivos
import generala
from render.render_elementos import render_juego, render_menu_jugadas

pygame.init()

# --------------------------
# Inicialización
# --------------------------
pantalla = pygame.display.set_mode((constantes.ANCHO, constantes.ALTO))
pygame.display.set_caption(constantes.TITULO)
clock = pygame.time.Clock()

# Fuentes
fuente = pygame.font.SysFont("Arial", 32)
fuente_small = pygame.font.SysFont("Arial", 24)

# Estado
pantalla_actual = "menu"

# Estado del juego
valores_dados = [1, 2, 3, 4, 5]
dados_bloqueados = [False] * 5
tiradas_realizadas = 0
mostrar_menu_jugadas = False
botones_jugadas = {}

# Layout de dados y candados
DADO_W, DADO_H = 120, 120
ESPACIO = 130
x_inicial = 30
y_inicial = constantes.ALTO - DADO_H - 30
CANDADO_W, CANDADO_H = 40, 40
CANDADO_OFFSET_X = (DADO_W - CANDADO_W) // 2
CANDADO_OFFSET_Y = 10
boton_tirada = pygame.Rect(x_inicial + 5 * ESPACIO + 20, y_inicial, 250, 50)

# Música de fondo
gestor_audio.reproducir_musica()

# --------------------------
# Bucle principal
# --------------------------
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

        # Gestión de eventos con botones
        if pantalla_actual == "menu":
            botones = render_pantalla.pantalla_principal(pantalla)
            pantalla_actual = gestor_eventos.gestionar_eventos(evento, pantalla_actual, botones)

        elif pantalla_actual == "opciones":
            botones = render_pantalla.pantalla_opciones(pantalla)
            pantalla_actual = gestor_eventos.gestionar_eventos(evento, pantalla_actual, botones)

        elif pantalla_actual == "estadisticas":
            registros = archivos.leer_estadisticas()
            from render_elementos import render_estadisticas
            render_estadisticas(pantalla, None, fuente, fuente_small, registros)
            botones = [{"accion": "volver", "rect": pygame.Rect(constantes.ANCHO-200, constantes.ALTO-80, 160, 40)}]
            pantalla_actual = gestor_eventos.gestionar_eventos(evento, pantalla_actual, botones)

        elif pantalla_actual == "creditos":
            from render_elementos import render_creditos
            render_creditos(pantalla, None, fuente_small)
            botones = [{"accion": "volver", "rect": pygame.Rect(constantes.ANCHO-200, constantes.ALTO-80, 160, 40)}]
            pantalla_actual = gestor_eventos.gestionar_eventos(evento, pantalla_actual, botones)

        elif pantalla_actual == "jugar":
            # Dibujar la pantalla de juego
            render_juego(
                pantalla, fuente,
                valores_dados, dados_bloqueados,
                boton_tirada, tiradas_realizadas, mostrar_menu_jugadas,
                x_inicial, y_inicial, ESPACIO, DADO_W, DADO_H,
                CANDADO_W, CANDADO_H, CANDADO_OFFSET_X, CANDADO_OFFSET_Y
            )

            if mostrar_menu_jugadas:
                categorias_disponibles = [c for c, p in generala.planilla.items() if p is None]
                botones_jugadas = render_menu_jugadas(pantalla, fuente, categorias_disponibles)

            # Eventos dentro del juego
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                pos = evento.pos

                # Botón tirar
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

                # Selección de jugada
                if mostrar_menu_jugadas:
                    for nombre, datos in botones_jugadas.items():
                        if datos["rect"].collidepoint(pos):
                            # Calcular puntos según lógica de generala.py
                            if nombre == "Escalera":
                                puntos = generala.jugadas_especiales["Escalera"] if generala.es_escalera(valores_dados) else 0
                            elif nombre == "Full":
                                puntos = generala.jugadas_especiales["Full"] if generala.es_full(valores_dados) else 0
                            elif nombre == "Poker":
                                puntos = generala.jugadas_especiales["Poker"] if generala.es_poker(valores_dados) else 0
                            elif nombre == "Generala":
                                if generala.es_generala(valores_dados):
                                    puntos = generala.jugadas_especiales["GeneralaServida"] if tiradas_realizadas == 1 else generala.jugadas_especiales["Generala"]
                                else:
                                    puntos = 0
                            else:
                                numero = generala.categorias.index(nombre) + 1
                                puntos = sum(d for d in valores_dados if d == numero)

                            generala.planilla[nombre] = puntos

                            # Reiniciar turno
                            tiradas_realizadas = 0
                            dados_bloqueados = [False] * 5
                            mostrar_menu_jugadas = False

                            # Verificar fin de juego
                            if None not in generala.planilla.values():
                                pantalla_actual = "final"

    pygame.display.flip()
    clock.tick(60)