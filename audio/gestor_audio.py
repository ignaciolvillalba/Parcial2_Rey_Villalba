import pygame
from datos.constantes import VOLUMEN

MUSICA_PRINCIPAL = "assets/intro.mp3"
EFECTO_CLICK = "assets/boton_principal.mp3"

VOLUMEN_MUSICA = VOLUMEN

def reproducir_musica(ruta = MUSICA_PRINCIPAL, loop = True):
    """Reproduce la música principal del juego."""
    pygame.mixer.music.load(ruta)
    
    if loop == True:
        repeticiones = -1
    else:
        repeticiones = 0

    pygame.mixer.music.set_volume(VOLUMEN_MUSICA)
    pygame.mixer.music.play(repeticiones)

def detener_musica():
    """Detiene cualquier música que esté sonando."""
    pygame.mixer.music.stop()

def pausar_musica():
    """Pausa la música (puede reanudarse después)."""
    pygame.mixer.music.pause()

def reanudar_musica():
    """Reanuda la música si estaba pausada."""
    pygame.mixer.music.unpause()

def cambiar_volumen(valor):
    """Cambia el volumen de la música."""
    pygame.mixer.music.set_volume(valor)


def cargar_efecto(ruta):
    """Carga un efecto de sonido desde una ruta."""
    efecto = pygame.mixer.Sound(ruta)
    nuevo_volumen = VOLUMEN_MUSICA + 0.2
    if nuevo_volumen > 1.0:
        nuevo_volumen = 1.0
    
    efecto.set_volume(nuevo_volumen)
    return efecto

def reproducir_efecto(efecto):
    """Reproduce un efecto que ya fue cargado."""
    efecto.play()
