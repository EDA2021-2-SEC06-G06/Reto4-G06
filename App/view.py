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

sys.setrecursionlimit(2**20)

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


def loadData(analyzer, file_size):
    """
    Carga las obras en la estructura de datos
    """
    controller.loadData(analyzer, file_size)


def chooseHomonymsREQ3(homonyms_map, city1, city2):
    origin_map = me.getValue(mp.get(homonyms_map, "origin"))
    destination_map = me.getValue(mp.get(homonyms_map, "destination"))
    origin_homonyms = mp.valueSet(origin_map)
    destination_homonyms = mp.valueSet(destination_map)
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


def printReq3(distance, path, origin_airport, destination_airport, origin_city, destination_city):
    
    print("El aeropuerto de salida más cercano a " + origin_city["name"] + " es: ")
    print("Nombre - " + origin_airport["Name"])
    print("Ciudad - " + origin_airport["City"])
    print("País - " + origin_airport["Country"])

    print("\nEl aeropuerto de llegada más cercano a " + destination_city["name"] + " es: ")
    print("Nombre - " + destination_airport["Name"])
    print("Ciudad - " + destination_airport["City"])
    print("País - " + destination_airport["Country"])

    print("\nEl camino recorrido es: ")
    i = 1
    while i<=lt.size(path):
        route = lt.getElement(path, i)
        print(route["vertexA"] + " --> " + route["vertexB"] + " // Distancia: " + str(route["weight"]) + " km")
        i+=1

    print("\nLa distancia total del recorrido, incluyendo las distancias de las ciudades a los aeropuertos, es:")
    print(str(distance) + " kilómetros")




while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    print()


    #Carga de datos
    if int(inputs) == 1:
        #file_size = input("Ingrese el sufijo del archivo que desea utilizar (small, large, 10pct...): ")
        file_size = "small"

        print("Cargando información de los archivos ....")
        analyzer = initAnalyzer()

        start_time = process_time()
        loadData(analyzer, file_size)
        stop_time = process_time()
        running_time = (stop_time - start_time)*1000
        
        print("\nTiempo de carga: " + str(running_time) + " milisegundos")
        
        #DAR ESPECIFICACIONES SOBRE LA CARGA DE DATOS (# de aeropuertos en cada grafo, etc.)
        print("\n===Digrafo de aeropuertos y rutas===")
        num_airports1 = gr.numVertices(analyzer["MainGraph"])
        num_routes1 = gr.numEdges(analyzer["MainGraph"])
        print("Número de aeropuertos: " + str(num_airports1))
        print("Número de rutas: " + str(num_routes1))

        print("\n===Grafo no dirigido de aeropuertos y rutas===")
        num_airports2 = gr.numVertices(analyzer["SecondaryGraph"])
        num_routes2 = gr.numEdges(analyzer["SecondaryGraph"])
        print("Número de aeropuertos: " + str(num_airports2))
        print("Número de rutas: " + str(num_routes2))



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
        #airport1 = input("Ingrese el código IATA del primer aeropuerto a consultar: ")
        #airport2 = input("Ingrese el código IATA del segundo aeropuerto a consultar: ")
        airport1 = "LED"
        airport2 = "RTP"

        start_time = process_time()
        num_clusters, same_cluster = controller.REQ2(analyzer, airport1, airport2)
        stop_time = process_time()
        running_time = (stop_time - start_time)*1000

        print("\n\n=============== Requerimiento Número 2 ===============")
        print("Tiempo de ejecución: " + str(running_time) + " milisegundos")

        print("\nNúmero de clusters: " + str(num_clusters))
        print("¿" + airport1 + " y " + airport2 + " pertenecen al mismo cluster? " + str(same_cluster))



    #Requerimiento 3
    elif int(inputs) == 30:

        #city1 = input("Ingrese el nombre de la ciudad de origen: ")
        #city2 = input("Ingrese el nombre de la ciudad de destino: ")

        #Para pruebas
        city1 = "Saint Petersburg"
        city2 = "Lisbon"

        homonyms_map = controller.homonymsREQ3(analyzer, city1, city2)
        origin_city, destination_city = chooseHomonymsREQ3(homonyms_map, city1, city2)
        
        start_time = process_time()
        distance, path, origin_airport, destination_airport = controller.REQ3(analyzer, origin_city, destination_city)
        stop_time = process_time()
        running_time = (stop_time - start_time)*1000

        print("\n\n=============== Requerimiento Número 3 ===============")
        print("Tiempo de ejecución: " + str(running_time) + " milisegundos\n")
        printReq3(distance, path, origin_airport, destination_airport, origin_city, destination_city)


    #Requerimiento 4
    elif int(inputs) == 40:

        start_time = process_time()
        #req4 = controller.REQ4(catalog)
        stop_time = process_time()
        running_time = (stop_time - start_time)*1000

        print("\n\n=============== Requerimiento Número 4 ===============")
        #print("Tiempo de ejecución: " + str(running_time) + " milisegundos")
    


    #Requerimiento 5
    elif int(inputs) == 50:
        airport = "DXB"

        start_time = process_time()
        in_req5, out_req5, req5, indegree, outdegree = controller.REQ5(analyzer, airport)
        stop_time = process_time()
        running_time = (stop_time - start_time)*1000

        print("\n\n=============== Requerimiento Número 5 ===============")
        print("Tiempo de ejecución: " + str(running_time) + " milisegundos\n")
        print()
        print(in_req5["elements"])
        print(out_req5["elements"])
        print(req5["elements"])
        print("Indegree: " + str(indegree))
        print("Outdegree: " + str(outdegree))
        


    else:
        sys.exit(0)


sys.exit(0)