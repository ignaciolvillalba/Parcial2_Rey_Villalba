import pygame
from datos.constantes import ANCHO, ALTO, COLOR_TEXTO_OSCURO, COLOR_SECUNDARIO, COLOR_TEXTO_CLARO
from render.render_elementos import logo_juego, fondo_menu, crear_boton_rect
from audio.gestor_audio import cargar_efecto, reproducir_efecto, EFECTO_CLICK

def pantalla_menu(pantalla):
    clock = pygame.time.Clock()
    logo = logo_juego()
    fondo = fondo_menu()
    x_logo = 350
    y_logo = 10
    etiquetas = ["Jugar", "Opciones", "Créditos", "Estadísticas", "Salir"]
    claves = ["jugar", "opciones", "creditos", "estadisticas", "salir"]
    ANCHO_BOTON = 160
    ALTO_BOTON = 60
    ESPACIO = 20
    total_ancho_botones = (ANCHO_BOTON * len(etiquetas)) + (ESPACIO * (len(etiquetas) - 1))
    inicio_botones_x = (ANCHO - total_ancho_botones) // 2
    y_botones = 500
    efecto_click = cargar_efecto(EFECTO_CLICK)
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "salir"
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                return "salir"
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                pos = evento.pos
                for i, clave in enumerate(claves):
                    x = inicio_botones_x + i * (ANCHO_BOTON + ESPACIO)
                    rect_temp = pygame.Rect(x, y_botones, ANCHO_BOTON, ALTO_BOTON)
                    if rect_temp.collidepoint(pos):
                        reproducir_efecto(efecto_click)
                        return clave
        pantalla.blit(fondo, (0, 0))
        pantalla.blit(logo, (x_logo, y_logo))
        for i, texto in enumerate(etiquetas):
            x = inicio_botones_x + i * (ANCHO_BOTON + ESPACIO)
            crear_boton_rect(pantalla, x, y_botones, ANCHO_BOTON, ALTO_BOTON, texto, COLOR_TEXTO_OSCURO, COLOR_SECUNDARIO)
        pygame.display.flip()
        clock.tick(60)

def pantalla_opciones(pantalla):
    clock = pygame.time.Clock()
    fuente = pygame.font.Font(None, 70)
    texto = fuente.render("PANTALLA DE OPCIONES", True, COLOR_TEXTO_CLARO)
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "salir"
            if evento.type == pygame.KEYDOWN and evento.key in (pygame.K_ESCAPE, pygame.K_BACKSPACE):
                return "menu"
        pantalla.fill((40, 40, 40))
        pantalla.blit(texto, (100, 100))
        pygame.display.flip()
        clock.tick(60)
