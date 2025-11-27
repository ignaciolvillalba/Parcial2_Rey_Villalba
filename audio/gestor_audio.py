import pygame
from datos.constantes import VOLUMEN

MUSICA_PRINCIPAL = "assets/intro.mp3"
EFECTO_CLICK = "assets/boton_principal.mp3"

VOLUMEN_MUSICA = VOLUMEN

def reproducir_musica(ruta=MUSICA_PRINCIPAL, loop=True):
    pygame.mixer.music.load(ruta)
    if loop:
        cantidad_repeticiones = -1
    else:
        cantidad_repeticiones = 0
    pygame.mixer.music.play(cantidad_repeticiones)

def detener_musica():
    pygame.mixer.music.stop()

def pausar_musica():
    pygame.mixer.music.pause()

def reanudar_musica():
    pygame.mixer.music.unpause()

def cambiar_volumen(valor):
    pygame.mixer.music.set_volume(valor)

def cargar_efecto(ruta):
    efecto = pygame.mixer.Sound(ruta)
    efecto.set_volume(min(VOLUMEN_MUSICA + 0.2, 1.0))
    return efecto

def reproducir_efecto(efecto):
    efecto.play()