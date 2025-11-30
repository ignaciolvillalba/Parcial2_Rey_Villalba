import pygame
import generala
from datos.constantes import ANCHO, ALTO, COLOR_TEXTO_CLARO, COLOR_TEXTO_OSCURO, FUENTE_GRANDE, FUENTE_CHICA

LOGO = pygame.image.load("assets/logo_juego.png")
LOGO = pygame.transform.scale(LOGO, (300, 300))

FONDO = pygame.image.load("assets/fondo.jpg")
FONDO = pygame.transform.scale(FONDO, (ANCHO, ALTO))

PLANILLA = pygame.image.load("assets/planilla.jpg")
PLANILLA = pygame.transform.scale(PLANILLA, (400, 450))

DADOS_IMAGENES = {
    1: pygame.image.load("assets/dado1.png"),
    2: pygame.image.load("assets/dado2.png"),
    3: pygame.image.load("assets/dado3.png"),
    4: pygame.image.load("assets/dado4.png"),
    5: pygame.image.load("assets/dado5.png"),
    6: pygame.image.load("assets/dado6.png"),
}

for i in DADOS_IMAGENES:
    DADOS_IMAGENES[i] = pygame.transform.scale(DADOS_IMAGENES[i], (80, 80))

def logo_juego(): return LOGO

def fondo_menu(): return FONDO

def crear_boton_rect(superficie, x, y, ancho, alto, texto, color, color_texto):
    rectangulo = pygame.Rect(x, y, ancho, alto)
    pygame.draw.rect(superficie, color, rectangulo, border_radius=10)
    texto_img = FUENTE_CHICA.render(texto, True, color_texto)
    texto_x = x + (ancho - texto_img.get_width()) // 2
    texto_y = y + (alto - texto_img.get_height()) // 2
    superficie.blit(texto_img, (texto_x, texto_y))
    return rectangulo

# Botón que usa una imagen
def crear_boton_imagen(pantalla, x, y, ancho, alto, ruta_imagen):
    imagen = pygame.image.load(ruta_imagen)
    imagen = pygame.transform.scale(imagen, (ancho, alto))
    forma = imagen.get_rect(topleft=(x, y))
    pantalla.blit(imagen, forma.topleft)
    return forma

def render_juego(pantalla, valores_dados, dados_bloqueados, boton_tirada, tiradas_realizadas, x_inicial, y_inicial, ESPACIO, DADO_ANCHO, DADO_ALTURA, CANDADO_ALTURA, CANDADO_OFFSET_X, CANDADO_OFFSET_Y):
    pantalla.blit(FONDO, (0, 0))
    numero_tiro = tiradas_realizadas
    texto_turno = f"Tiro {numero_tiro} de 3"
    txt = FUENTE_CHICA.render(texto_turno, True, COLOR_TEXTO_CLARO)
    pantalla.blit(txt, (20, 20))
    for i, valor in enumerate(valores_dados):
        x = x_inicial + i * ESPACIO
        y = y_inicial
        if valor in DADOS_IMAGENES:
            pantalla.blit(DADOS_IMAGENES[valor], (x, y))
        else:
            pygame.draw.rect(pantalla, COLOR_TEXTO_OSCURO, (x, y, DADO_ANCHO, DADO_ALTURA), border_radius=8)
            num = FUENTE_GRANDE.render(str(valor), True, COLOR_TEXTO_CLARO)
            pantalla.blit(num, num.get_rect(center=(x + DADO_ANCHO // 2, y + DADO_ALTURA // 2)))
        ruta_candado = ""
        if dados_bloqueados[i]:
            ruta_candado = "assets/candado2.png"
        else:
            ruta_candado = "assets/candado1.png"
        crear_boton_imagen(pantalla, x + CANDADO_OFFSET_X, y - CANDADO_ALTURA - CANDADO_OFFSET_Y, 25, 25, ruta_candado)
    if tiradas_realizadas < 3:
        crear_boton_rect(pantalla, boton_tirada.x, boton_tirada.y, 180, 60, "Tirar dados", COLOR_TEXTO_OSCURO, COLOR_TEXTO_CLARO)

def render_planilla_calculos(pantalla, posibles, x, y, tiradas_realizadas):
    pantalla.blit(PLANILLA, (x, y))
    offset_y = 116
    alto_fila = 29
    botones_anotar = {}

    for i, (categoria, valor) in enumerate(generala.planilla.items()):
        y_fila = y + offset_y + i * alto_fila

        if valor is not None:
            puntos = valor
        else:
            puntos = posibles.get(categoria, 0)

        txt_categoria = FUENTE_CHICA.render(str(categoria), True, COLOR_TEXTO_OSCURO)
        txt_puntos = FUENTE_CHICA.render(str(puntos), True, COLOR_TEXTO_OSCURO)
        pantalla.blit(txt_categoria, (x + 40, y_fila))
        pantalla.blit(txt_puntos, (x + 300, y_fila))

        if valor is None and tiradas_realizadas == 3:
            rect_anotar = crear_boton_imagen(pantalla, x + 350, y_fila - 8, 30, 30, "assets/anotar.png")
            botones_anotar[categoria] = rect_anotar

    return botones_anotar

def render_creditos(pantalla):
    texto1 = FUENTE_GRANDE.render("Generala Tematica", True, COLOR_TEXTO_CLARO)
    texto2 = FUENTE_CHICA.render("Autor/es: Mateo Rey, Ignacio Villalba", True, COLOR_TEXTO_CLARO)
    texto3 = FUENTE_CHICA.render("Fecha: Noviembre 2025", True, COLOR_TEXTO_CLARO)
    texto4 = FUENTE_CHICA.render("Docente: Prof. Martin Alejandro García", True, COLOR_TEXTO_CLARO)
    texto5 = FUENTE_CHICA.render("Carrera: Tecnicatura Universitaria en Programación", True, COLOR_TEXTO_CLARO)
    texto6 = FUENTE_CHICA.render("Mail: reym1414@gmail.com - ignacioezequielvillalba1@gmail.com", True, COLOR_TEXTO_CLARO)
    texto7 = FUENTE_CHICA.render("Música: Wii Party - Main Theme (Nintendo)", True, COLOR_TEXTO_CLARO)
    texto8 = FUENTE_CHICA.render("Presione cualquier tecla para volver al menú principal.", True, COLOR_TEXTO_CLARO)

    pantalla.fill((0, 0, 0))
    pantalla.blit(texto1, (20, 20))
    pantalla.blit(texto2, (20, 100))
    pantalla.blit(texto3, (20, 160))
    pantalla.blit(texto4, (20, 220))
    pantalla.blit(texto5, (20, 280))
    pantalla.blit(texto6, (20, 340))
    pantalla.blit(texto7, (20, 400))
    pantalla.blit(texto8, (20, 500))

    pygame.display.flip()
    clock = pygame.time.Clock()
    esperando = True

    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "salir"
            if evento.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                return "menu"
        clock.tick(60)

def solicitar_nombre(pantalla, FUENTE_CHICA):
    nombre = ""
    activo = True

    while activo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    activo = False
                elif evento.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                else:
                    nombre = nombre + evento.unicode

        pantalla.fill((0, 0, 0))
        instruccion = FUENTE_CHICA.render("Ingrese su nombre y presione ENTER:", True, COLOR_TEXTO_CLARO)
        entrada = FUENTE_CHICA.render(nombre, True, COLOR_TEXTO_CLARO)
        pantalla.blit(instruccion, (0, 0))
        pantalla.blit(entrada, (0, 50))
        pygame.display.flip()

    return nombre
