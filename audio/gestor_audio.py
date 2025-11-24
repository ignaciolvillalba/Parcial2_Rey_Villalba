import pygame
from datos.constantes import VOLUMEN

# Rutas de archivos de audio
MUSICA_PRINCIPAL = "assets/intro.mp3"
EFECTO_CLICK = "assets/boton_principal.mp3"

# Volumen inicial
VOLUMEN_MUSICA = VOLUMEN

# --------------------------
# Funciones de música
# --------------------------
def reproducir_musica(ruta=MUSICA_PRINCIPAL, loop=True):
    """Reproduce música de fondo."""
    pygame.mixer.music.load(ruta)
    cantidad_reproducciones = -1 if loop else 0
    pygame.mixer.music.set_volume(VOLUMEN_MUSICA)
    pygame.mixer.music.play(cantidad_reproducciones)

def detener_musica():
    """Detiene la música."""
    pygame.mixer.music.stop()

def pausar_musica():
    """Pausa la música."""
    pygame.mixer.music.pause()

def reanudar_musica():
    """Reanuda la música pausada."""
    pygame.mixer.music.unpause()

def cambiar_volumen(valor):
    """Cambia el volumen de la música."""
    pygame.mixer.music.set_volume(valor)

# --------------------------
# Funciones de efectos
# --------------------------
def cargar_efecto(ruta):
    """Carga un efecto de sonido desde archivo."""
    efecto = pygame.mixer.Sound(ruta)
    efecto.set_volume(min(VOLUMEN_MUSICA + 0.2, 1.0))  # límite máximo 1.0
    return efecto

def reproducir_efecto(efecto):
    """Reproduce un efecto de sonido cargado."""
    efecto.play()