import pygame
from datos import config_json
pygame.init()
datos = config_json.cargar_datos()
# Ventana
ANCHO = datos["config"]["ventana"]["ancho"]
ALTO = datos["config"]["ventana"]["alto"]
TITULO = datos["config"]["ventana"]["titulo"]
# Fuente
FUENTE_NOMBRE = datos["config"]["fuente"]["nombre"]
FUENTE = FUENTE_NOMBRE
FUENTE_GRANDE = pygame.font.SysFont(FUENTE_NOMBRE, datos["config"]["fuente"]["tamaño_grande"])
FUENTE_CHICA = pygame.font.SysFont(FUENTE_NOMBRE, datos["config"]["fuente"]["tamaño_chico"])
# Colores
COLOR_FONDO = datos["config"]["colores"]["fondo"]
COLOR_TEXTO_OSCURO = datos["config"]["colores"]["texto_oscuro"]
COLOR_TEXTO_CLARO = datos["config"]["colores"]["texto_claro"]
COLOR_PRIMARIO = datos["config"]["colores"]["primario"]
COLOR_SECUNDARIO = datos["config"]["colores"]["secundario"]
COLOR_GRIS = datos["config"]["colores"]["gris"]
COLOR_GRIS_CLARO = datos["config"]["colores"]["gris_claro"]
# Audio
VOLUMEN = datos["config"]["audio"]["volumen"]
