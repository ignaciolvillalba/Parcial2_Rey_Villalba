import pygame
from datos.constantes import ANCHO, ALTO, TITULO
from audio import gestor_audio
from menu import pantalla_menu, pantalla_opciones
from play import pantalla_juego
from estadisticas import pantalla_estadisticas
from render.render_elementos import render_creditos

pygame.init()
pygame.mixer.init()
gestor_audio.reproducir_musica()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption(TITULO)

pantalla_actual = "menu"
corriendo = True

while corriendo:
    if pantalla_actual == "menu":
        pantalla_actual = pantalla_menu(pantalla)
    elif pantalla_actual == "jugar":
        pantalla_actual = pantalla_juego(pantalla)
    elif pantalla_actual == "opciones":
        pantalla_actual = pantalla_opciones(pantalla)
    elif pantalla_actual == "estadisticas":
        pantalla_actual = pantalla_estadisticas(pantalla)
    elif pantalla_actual == "creditos":
        pantalla_actual = render_creditos(pantalla)
    elif pantalla_actual == "salir":
        corriendo = False

pygame.quit()
