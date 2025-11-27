import generala as g
from archivos import mostrar_estadisticas
while True:
    print("----------------")
    print("     Generala")
    print("----------------")
    print("1. Jugar")
    print("2. Estadisticas")
    print("3. Creditos")
    print("4. Salir")
    opcion = input("Seleccione una opcion: ")
    if opcion == "1":
        g.jugar()
    elif opcion == "2":
        mostrar_estadisticas()
    elif opcion == "3":
        g.mostrar_creditos()
    elif opcion == "4":
        print("Gracias por jugar. ¡Hasta luego!")
    while opcion not in ["1", "2", "3", "4"]:
        opcion = input("Opcion invalida. Seleccione una opcion: ")
        break