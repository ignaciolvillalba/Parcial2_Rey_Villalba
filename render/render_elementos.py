import pygame
from datos.constantes import ANCHO, ALTO, COLOR_TEXTO_CLARO, COLOR_TEXTO_OSCURO

# Cargar assets UNA SOLA VEZ
LOGO = pygame.image.load("assets/logo_juego.png")
LOGO = pygame.transform.scale(LOGO, (500, 500))

FONDO = pygame.image.load("assets/fondo.jpg")
FONDO = pygame.transform.scale(FONDO, (ANCHO, ALTO))

DADOS_IMAGENES = {
    1: pygame.image.load("assets/dado1.png"),
    2: pygame.image.load("assets/dado2.png"),
    3: pygame.image.load("assets/dado3.png"),
    4: pygame.image.load("assets/dado4.png"),
    5: pygame.image.load("assets/dado5.png"),
    6: pygame.image.load("assets/dado6.png"),
}
for i in DADOS_IMAGENES:
    DADOS_IMAGENES[i] = pygame.transform.scale(DADOS_IMAGENES[i], (120, 120))

CANDADO_ABIERTO = pygame.image.load("assets/candado1.png")
CANDADO_CERRADO = pygame.image.load("assets/candado2.png")
CANDADO_ABIERTO = pygame.transform.scale(CANDADO_ABIERTO, (40, 40))
CANDADO_CERRADO = pygame.transform.scale(CANDADO_CERRADO, (40, 40))

def logo_juego():
    return LOGO

def fondo_menu():
    return FONDO


def crear_boton_rect(superficie, x, y, ancho, alto, texto, color, color_texto):
    fuente = pygame.font.Font(None, 40)
    rectangulo = pygame.Rect(x, y, ancho, alto)

    pygame.draw.rect(superficie, color, rectangulo, border_radius=10)
    texto_img = fuente.render(texto, True, color_texto)
    texto_x = x + (ancho - texto_img.get_width()) // 2
    texto_y = y + (alto - texto_img.get_height()) // 2

    superficie.blit(texto_img, (texto_x, texto_y))

    return rectangulo

def crear_boton_imagen(superficie, x, y, ancho, alto, ruta_imagen):
    imagen = pygame.image.load(ruta_imagen)
    imagen = pygame.transform.scale(imagen, (ancho, alto))
    forma = imagen.get_rect(topleft=(x, y))
    superficie.blit(imagen, forma.topleft)
    return forma


def render_juego(pantalla, valores_dados, dados_bloqueados, boton_tirada, tiradas_realizadas, mostrar_menu_jugadas, x_inicial, y_inicial, ESPACIO, DADO_W, DADO_H, CANDADO_H, CANDADO_OFFSET_X, CANDADO_OFFSET_Y):
    pantalla.blit(FONDO, (0, 0))


    texto_turno = f"Tiro {tiradas_realizadas} de 3"
    txt = pygame.font.Font(None, 36).render(texto_turno, True, COLOR_TEXTO_CLARO)
    pantalla.blit(txt, (20, 20))

    for i, valor in enumerate(valores_dados):
        x = x_inicial + i * ESPACIO
        y = y_inicial

        if valor in DADOS_IMAGENES:
            pantalla.blit(DADOS_IMAGENES[valor], (x, y))
        else:
            pygame.draw.rect(pantalla, COLOR_TEXTO_OSCURO, (x, y, DADO_W, DADO_H), border_radius=8)
            num = pygame.font.Font(None, 72).render(str(valor), True, COLOR_TEXTO_CLARO)
            pantalla.blit(num, num.get_rect(center=(x + DADO_W // 2, y + DADO_H // 2)))

        candado_img = CANDADO_CERRADO if dados_bloqueados[i] else CANDADO_ABIERTO
        pantalla.blit(candado_img, (x + CANDADO_OFFSET_X, y - CANDADO_H - CANDADO_OFFSET_Y))

    if tiradas_realizadas < 3 and not mostrar_menu_jugadas:
        crear_boton_rect(
            pantalla,
            boton_tirada.x, boton_tirada.y,
            boton_tirada.width, boton_tirada.height,
            "Tirar dados",
            COLOR_TEXTO_OSCURO, COLOR_TEXTO_CLARO
        )

def render_menu_jugadas(pantalla, categorias_disponibles):
    pantalla.fill((0, 0, 0)) 

    subt = pygame.font.Font(None, 42).render(
        "Elegí una categoría para anotar", True, COLOR_TEXTO_CLARO
    )
    pantalla.blit(subt, subt.get_rect(center=(ANCHO // 2, 120)))

    botones = {}
    col = 3
    ANCHO_BOTON, ALTO_BOTON = 220, 50
    ESPACIO_X, ESPACIO_Y = 20, 16

    total_cols = col
    grid_w = total_cols * ANCHO_BOTON + (total_cols - 1) * ESPACIO_X
    inicio_x = (ANCHO - grid_w) // 2
    inicio_y = 180

    for i, nombre in enumerate(categorias_disponibles):
        fila = i // col
        columna = i % col
        x = inicio_x + columna * (ANCHO_BOTON + ESPACIO_X)
        y = inicio_y + fila * (ALTO_BOTON + ESPACIO_Y)
        rect = crear_boton_rect(
            pantalla, x, y, ANCHO_BOTON, ALTO_BOTON,
            nombre, COLOR_TEXTO_OSCURO, COLOR_TEXTO_CLARO
        )
        botones[nombre] = {"rect": rect}

    return botones