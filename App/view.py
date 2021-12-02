"""
Reto 4 - view.py

Carlos Arturo Holguín Cárdenas
Daniel Hernández Pineda

"""

import config as cf
import sys
import controller
from time import process_time
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import graph as gr
assert cf


def printMenu():
    print("\n\n-----------------------------------------")
    print("Bienvenido al menú de opciones")
    print("-----------------------------------------")
    print("Opciones preliminares")
    print("1- Cargar datos")
    print("-----------------------------------------")
    print("Requerimientos")
    print("10- Consultar Requerimiento 1")
    print("20- Consultar Requerimiento 2")
    print("30- Consultar Requerimiento 3")
    print("40- Consultar Requerimiento 4")
    print("50- Consultar Requerimiento 5")
    print("-----------------------------------------")
    print("0- Salir\n")


def initAnalyzer():
    """
    Inicializa el catálogo
    """
    return controller.initAnalyzer()


def loadData(analyzer):
    """
    Carga las obras en la estructura de datos
    """
    controller.loadData(analyzer)


def chooseHomonymsREQ3(homonyms_map, city1, city2):
    origin_homonyms = me.getValue(mp.get(homonyms_map, "origin"))
    destination_homonyms = me.getValue(mp.get(homonyms_map, "destination"))
    origin = lt.getElement(origin_homonyms, 1)
    destination = lt.getElement(destination_homonyms, 1)

    if lt.size(origin_homonyms)>1:
        origin_homonyms_size = lt.size(origin_homonyms)
        print("\n\n---------------------------------------------------------------------------------------------------------")
        print("Se encontraron " + str(origin_homonyms_size) + " ciudades llamadas " + city1 + ". A continuación, la información de cada una:")
        print()
        opcion = 1

        while opcion <= origin_homonyms_size:
            city = lt.getElement(origin_homonyms, opcion)
            print("Opción " + str(opcion) + ": ", city)
            opcion += 1

        origin_choice = int(input("\nIngrese la opción de la ciudad que desea consultar: "))
        origin = lt.getElement(origin_homonyms, origin_choice)

    if lt.size(destination_homonyms)>1:
        destination_homonyms_size = lt.size(destination_homonyms)
        print("\n\n---------------------------------------------------------------------------------------------------------")
        print("Se encontraron " + str(destination_homonyms_size) + " ciudades llamadas " + city2 + ". A continuación, la información de cada una:")
        print()
        opcion = 1

        while opcion <= destination_homonyms_size:
            city = lt.getElement(destination_homonyms, opcion)
            print("Opción " + str(opcion) + ": ", city)
            opcion += 1

        destination_choice = int(input("\nIngrese la opción de la ciudad que desea consultar: "))
        destination = lt.getElement(destination_homonyms, destination_choice)

    return origin, destination


while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    print()


    #Carga de datos
    if int(inputs) == 1:
        print("Cargando información de los archivos ....")
        analyzer = initAnalyzer()

        start_time = process_time()
        loadData(analyzer)
        stop_time = process_time()
        running_time = (stop_time - start_time)*1000
        
        print("\nTiempo de carga: " + str(running_time) + " milisegundos")
        
        #DAR ESPECIFICACIONES SOBRE LA CARGA DE DATOS (# de aeropuertos en cada grafo, etc.)



    #Requerimiento 1
    elif int(inputs) == 10:

        start_time = process_time()
        #req1 = controller.REQ1(catalog)
        stop_time = process_time()
        running_time = (stop_time - start_time)*1000

        print("\n\n=============== Requerimiento Número 1 ===============")
        #print("Tiempo de ejecución: " + str(running_time) + " milisegundos")



    #Requerimiento 2
    elif int(inputs) == 20:

        start_time = process_time()
        #req2 = controller.REQ2(catalog)
        stop_time = process_time()
        running_time = (stop_time - start_time)*1000

        print("\n\n=============== Requerimiento Número 2 ===============")
        #print("Tiempo de ejecución: " + str(running_time) + " milisegundos")



    #Requerimiento 3
    elif int(inputs) == 30:

        city1 = input("Ingrese el nombre de la ciudad de origen: ")
        city2 = input("Ingrese el nombre de la ciudad de destino: ")

        homonyms_map = controller.homonymsREQ3(analyzer, city1, city2)
        origin,destination = chooseHomonymsREQ3(homonyms_map, city1, city2)
        
        start_time = process_time()
        req4 = controller.REQ3(analyzer, origin, destination)
        stop_time = process_time()
        running_time = (stop_time - start_time)*1000

        #print("\n\n=============== Requerimiento Número 3 ===============")
        #print("Tiempo de ejecución: " + str(running_time) + " milisegundos\n")



    #Requerimiento 4
    elif int(inputs) == 40:

        start_time = process_time()
        #req3 = controller.REQ4(catalog)
        stop_time = process_time()
        running_time = (stop_time - start_time)*1000

        print("\n\n=============== Requerimiento Número 4 ===============")
        #print("Tiempo de ejecución: " + str(running_time) + " milisegundos")
    



    #Requerimiento 5
    elif int(inputs) == 50:

        start_time = process_time()
        #req5 = controller.REQ5(catalog)
        stop_time = process_time()
        running_time = (stop_time - start_time)*1000

        print("\n\n=============== Requerimiento Número 5 ===============")
        #print("Tiempo de ejecución: " + str(running_time) + " milisegundos\n")



    else:
        sys.exit(0)


sys.exit(0)