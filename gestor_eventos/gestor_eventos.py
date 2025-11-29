import pygame
import generala
from audio.gestor_audio import cargar_efecto, reproducir_efecto, EFECTO_CLICK

def gestionar_eventos(evento, pantalla_actual, botones, tiradas_realizadas, botones_anotar,posibles, dados_bloqueados):
    if botones is None:
        return pantalla_actual, tiradas_realizadas, dados_bloqueados

    if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
        pos = evento.pos

        # Si estamos en el tercer tiro y se clickea un botón de anotar
        if tiradas_realizadas == 3 and botones_anotar:
            for categoria, rect in botones_anotar.items():
                if rect.collidepoint(pos):
                    # Guardar puntaje en la planilla
                    generala.planilla[categoria] = posibles[categoria]
                    tiradas_realizadas = 0
                    dados_bloqueados = [False] * 5
                    if None not in generala.planilla.values():
                        pantalla_actual = "final"

        # Detección de clic sobre botones generales
        for boton in botones:
            if boton["rect"].collidepoint(pos):
                print("CLICK DETECTADO SOBRE:", boton["accion"])
                efecto = cargar_efecto(EFECTO_CLICK)
                reproducir_efecto(efecto)
                accion = boton["accion"]

                if pantalla_actual == "menu":
                    if accion == "jugar":
                        return "jugar", tiradas_realizadas, dados_bloqueados
                    if accion == "opciones":
                        return "opciones", tiradas_realizadas, dados_bloqueados
                    if accion == "estadisticas":
                        return "estadisticas", tiradas_realizadas, dados_bloqueados
                    if accion == "creditos":
                        return "creditos", tiradas_realizadas, dados_bloqueados
                    if accion == "salir":
                        return "salir", tiradas_realizadas, dados_bloqueados

                elif pantalla_actual == "juego":
                    if accion == "tirar":
                        return "tirar", tiradas_realizadas, dados_bloqueados
                    if accion == "volver":
                        return "menu", tiradas_realizadas, dados_bloqueados

                elif pantalla_actual == "estadisticas":
                    if accion == "volver":
                        return "menu", tiradas_realizadas, dados_bloqueados

                elif pantalla_actual == "creditos":
                    if accion == "volver":
                        return "menu", tiradas_realizadas, dados_bloqueados

    return pantalla_actual, tiradas_realizadas, dados_bloqueados