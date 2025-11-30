import pygame
from archivos import leer_estadisticas
from datos.constantes import COLOR_FONDO, COLOR_TEXTO_CLARO, FUENTE_CHICA, FUENTE_GRANDE

def pantalla_estadisticas(pantalla):
    clock = pygame.time.Clock()
    registros = leer_estadisticas()
    desplazamiento = 0
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "salir"
            if evento.type == pygame.KEYDOWN and evento.key in (pygame.K_ESCAPE, pygame.K_BACKSPACE):
                return "menu"
            if evento.type == pygame.MOUSEWHEEL:
                desplazamiento += evento.y * 20
        pantalla.fill(COLOR_FONDO)
        titulo = FUENTE_GRANDE.render("ESTADÍSTICAS", True, COLOR_TEXTO_CLARO)
        pantalla.blit(titulo, (50, 30))
        cabecera = FUENTE_CHICA.render("Jugador          | Puntaje total", True, COLOR_TEXTO_CLARO)
        pantalla.blit(cabecera, (50, 100))
        pygame.draw.line(pantalla, COLOR_TEXTO_CLARO, (40, 130), (800, 130), 2)
        y = 150 + desplazamiento
        for fila in registros:
            texto = FUENTE_CHICA.render(str(fila[0]) + "  " + str(fila[1]), True, COLOR_TEXTO_CLARO)
            pantalla.blit(texto, (50, y))
            y += 30
        msg = FUENTE_CHICA.render("Presione ESC para volver", True, COLOR_TEXTO_CLARO)
        pantalla.blit(msg, (50, 500))
        pygame.display.flip()
        clock.tick(60)
