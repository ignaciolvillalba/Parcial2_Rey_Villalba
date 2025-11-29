import pygame
import generala
from datos.constantes import (
    ANCHO, ALTO,
    COLOR_TEXTO_CLARO, COLOR_TEXTO_OSCURO,
    FUENTE_GRANDE, FUENTE_CHICA
)

# Cargar assets UNA SOLA VEZ
LOGO = pygame.image.load("assets/logo_juego.png")
LOGO = pygame.transform.scale(LOGO, (500, 500))

FONDO = pygame.image.load("assets/fondo.jpg")
FONDO = pygame.transform.scale(FONDO, (ANCHO, ALTO))

PLANILLA = pygame.image.load("assets/planilla.jpg")
PLANILLA = pygame.transform.scale(PLANILLA, (600, 800))

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

# Accesos simples
def logo_juego():
    return LOGO

def fondo_menu():
    return FONDO

# Botón rectangular con texto
def crear_boton_rect(superficie, x, y, ancho, alto, texto, color, color_texto):
    rectangulo = pygame.Rect(x, y, ancho, alto)
    pygame.draw.rect(superficie, color, rectangulo, border_radius=10)

    texto_img = FUENTE_CHICA.render(texto, True, color_texto)
    texto_x = x + (ancho - texto_img.get_width()) // 2
    texto_y = y + (alto - texto_img.get_height()) // 2
    superficie.blit(texto_img, (texto_x, texto_y))

    return rectangulo

# Botón con imagen
def crear_boton_imagen(pantalla, x, y, ancho, alto, ruta_imagen):
    imagen = pygame.image.load(ruta_imagen)
    imagen = pygame.transform.scale(imagen, (ancho, alto))
    forma = imagen.get_rect(topleft=(x, y))
    pantalla.blit(imagen, forma.topleft)
    return forma

# Render principal del juego
def render_juego(pantalla, valores_dados, dados_bloqueados, boton_tirada, tiradas_realizadas, mostrar_menu_jugadas, x_inicial, y_inicial, ESPACIO, DADO_W, DADO_H, CANDADO_H, CANDADO_OFFSET_X, CANDADO_OFFSET_Y):
    pantalla.blit(FONDO, (0, 0))

    texto_turno = f"Tiro {tiradas_realizadas} de 3"
    txt = FUENTE_CHICA.render(texto_turno, True, COLOR_TEXTO_CLARO)
    pantalla.blit(txt, (20, 20))

    for i, valor in enumerate(valores_dados):
        x = x_inicial + i * ESPACIO
        y = y_inicial

        if valor in DADOS_IMAGENES:
            pantalla.blit(DADOS_IMAGENES[valor], (x, y))
        else:
            pygame.draw.rect(pantalla, COLOR_TEXTO_OSCURO, (x, y, DADO_W, DADO_H), border_radius=8)
            num = FUENTE_GRANDE.render(str(valor), True, COLOR_TEXTO_CLARO)
            pantalla.blit(num, num.get_rect(center=(x + DADO_W // 2, y + DADO_H // 2)))

        ruta_candado = "assets/candado2.png" if dados_bloqueados[i] else "assets/candado1.png"
        crear_boton_imagen(
            pantalla,
            x + CANDADO_OFFSET_X,
            y - CANDADO_H - CANDADO_OFFSET_Y,
            40,
            40,
            ruta_candado
        )

    if tiradas_realizadas < 3 and not mostrar_menu_jugadas:
        crear_boton_rect(pantalla, boton_tirada.x, boton_tirada.y, boton_tirada.width, boton_tirada.height, "Tirar dados", COLOR_TEXTO_OSCURO, COLOR_TEXTO_CLARO)

# Render de planilla dinámica con fondo temático
def render_planilla_calculos(pantalla, posibles, x, y, tiradas_realizadas):
    pantalla.blit(PLANILLA, (x, y))
    offset_y = 230
    alto_fila = 50

    botones_anotar = {}

    for i, (categoria, valor) in enumerate(generala.planilla.items()):
        y_fila = y + offset_y + i * alto_fila

        # Si ya está anotado en la planilla, mostrar ese valor fijo
        if valor is not None:
            puntos = valor
        else:
            puntos = posibles.get(categoria, 0)

        txt_categoria = FUENTE_CHICA.render(str(categoria), True, COLOR_TEXTO_OSCURO)
        txt_puntos = FUENTE_CHICA.render(str(puntos), True, COLOR_TEXTO_OSCURO)

        pantalla.blit(txt_categoria, (x + 40, y_fila))
        pantalla.blit(txt_puntos, (x + 300, y_fila))

        if valor is None and tiradas_realizadas == 3:
            rect_anotar = crear_boton_imagen(pantalla,x + 500,y_fila - 18,47,47,"assets/anotar.png")
            botones_anotar[categoria] = rect_anotar

    return botones_anotar


def render_creditos(pantalla):
    texto1 = FUENTE_GRANDE.render("Generala Tematica", True, COLOR_TEXTO_CLARO)
    texto2 = FUENTE_CHICA.render("Autor/es: Mateo Rey, Ignacio Villalba", True, COLOR_TEXTO_CLARO)
    texto3 = FUENTE_CHICA.render("Fecha: Noviembre 2025", True, COLOR_TEXTO_CLARO)
    texto4 = FUENTE_CHICA.render("Docente: Prof. Martin Alejandro Garciá", True, COLOR_TEXTO_CLARO)
    texto5 = FUENTE_CHICA.render("Carrera: Tecnicatura Universitaria en Programación", True, COLOR_TEXTO_CLARO)
    texto6 = FUENTE_CHICA.render("Mail de contacto: reym1414@gmail.com  - ignacioezequielvillalba1@gmail.com", True, COLOR_TEXTO_CLARO)
    texto7 = FUENTE_CHICA.render("Musica: Wii Party - Main Theme (Nintendo)", True, COLOR_TEXTO_CLARO)
    texto8 = FUENTE_CHICA.render("Presione cualquier tecla para volver al menú principal.", True, COLOR_TEXTO_CLARO)
    pantalla.fill((0, 0, 0))
    pantalla.blit(texto1, (0, 0))
    pantalla.blit(texto2, (0, 80))
    pantalla.blit(texto3, (0, 140))
    pantalla.blit(texto4, (0, 200))
    pantalla.blit(texto5, (0, 260))
    pantalla.blit(texto6, (0, 320))
    pantalla.blit(texto7, (0, 380))
    pantalla.blit(texto8, (0, 500))
    # Espera a interacción del usuario
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                esperando = False
