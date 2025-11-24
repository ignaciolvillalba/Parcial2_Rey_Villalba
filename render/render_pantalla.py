import pygame
from datos.constantes import ANCHO, COLOR_TEXTO_OSCURO, COLOR_SECUNDARIO, COLOR_TEXTO_CLARO
from .render_elementos import logo_juego, fondo_menu, crear_boton_rect

# --------------------------
# Pantalla principal (menú)
# --------------------------
def pantalla_principal(pantalla):
    logo = logo_juego()
    fondo = fondo_menu()
    
    # Medidas del logo
    ancho_logo = logo.get_width()
    alto_logo = logo.get_height()

    # Posición centrada arriba
    x_logo = (ANCHO - ancho_logo) // 2
    y_logo = 10

    # Botones
    etiquetas = ["Jugar", "Opciones", "Créditos", "Estadísticas", "Salir"]
    claves = ["jugar", "opciones", "creditos", "estadisticas", "salir"]

    ANCHO_BOTON = 160
    ALTO_BOTON = 60
    ESPACIO = 20

    total_ancho_botones = (ANCHO_BOTON * len(etiquetas)) + (ESPACIO * (len(etiquetas) - 1))
    inicio_botones_x = (ANCHO - total_ancho_botones) // 2
    y_botones = y_logo + alto_logo + 20

    botones = []
    pantalla.blit(fondo, (0, 0))
    pantalla.blit(logo, (x_logo, y_logo))

    for i, texto in enumerate(etiquetas):
        x = inicio_botones_x + i * (ANCHO_BOTON + ESPACIO)
        rect = crear_boton_rect(
            pantalla,
            x, y_botones,
            ANCHO_BOTON, ALTO_BOTON,
            texto,
            COLOR_TEXTO_OSCURO,
            COLOR_SECUNDARIO
        )
        botones.append({"accion": claves[i], "rect": rect})

    return botones

# --------------------------
# Pantalla de opciones
# --------------------------
def pantalla_opciones(pantalla):
    pantalla.fill((40, 40, 40))
    fuente = pygame.font.Font(None, 70)
    texto = fuente.render("PANTALLA DE OPCIONES", True, COLOR_TEXTO_CLARO)
    pantalla.blit(texto, (100, 100))
    return []