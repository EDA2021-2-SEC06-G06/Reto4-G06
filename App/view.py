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


def printGraphsInfo(analyzer):
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


def printReq1(DataInOrder):
    SizeDataInOrder = lt.size(DataInOrder)
    pos = SizeDataInOrder
    centinela =True
    k=0
    while pos>0 and centinela==True:
        Element = lt.getElement(DataInOrder, pos)
        SizeElement = lt.size(Element)
        if k!=5:         
            if SizeElement==1:
                Element1=lt.getElement(Element,1)
                Airport = lt.getElement(Element1,3)
                City = lt.getElement(Element1,4)
                Country = lt.getElement(Element1,5)
                Iata = lt.getElement(Element1,2)
                Connection = lt.getElement(Element1,1)
                print("El aeropuerto de "+Airport+" esta ubicado en la ciudad de "+City+", en el pais de "+Country+", ademas su codgio IATA es "+Iata+" y cuenta con "+str(Connection)+" conexiones")
                k+=1
                if k==5:
                    break
            if SizeElement>1:
                Pos1 = 1
                while Pos1<=SizeElement:
                    Element1=lt.getElement(Element,Pos1)
                    Airport = lt.getElement(Element1,3)
                    City = lt.getElement(Element1,4)
                    Country = lt.getElement(Element1,5)
                    Iata = lt.getElement(Element1,2)
                    Connection = lt.getElement(Element1,1)
                    print("El aeropuerto de "+Airport+" esta ubicado en la ciudad de "+City+", en el pais de "+Country+", ademas su codgio IATA es "+Iata+" y cuenta con "+str(Connection)+" conexiones")
                    Pos1+=1
                    k+=1
                    if k==5:
                       break
        pos-=1


def printReq2(analyzer, IATA_airport1, IATA_airport2, num_clusters, same_cluster):
    AirportsMap = analyzer["AirportsMap"]
    print("\nNúmero de clusters en la red de aeropuertos: " + str(num_clusters))

    print("\nInformación del aeropuerto 1: ")
    airport1 = me.getValue(mp.get(AirportsMap, IATA_airport1))
    airport1_name = airport1["Name"]
    airport1_city = airport1["City"]
    print("Nombre: " + airport1_name + "   //   " + "Ciudad: " + airport1_city + "   //   " + "Código IATA: " + IATA_airport1)
    
    print("\nInformación del aeropuerto 2: ")
    airport2 = me.getValue(mp.get(AirportsMap, IATA_airport2))
    airport2_name = airport2["Name"]
    airport2_city = airport2["City"]
    print("Nombre: " + airport2_name + "   //   " + "Ciudad: " + airport2_city + "   //   " + "Código IATA: " + IATA_airport2)
    
    resp = "NO"
    if same_cluster:
        resp = "SÍ"

    print("\nLos aeropuertos " + resp + " pertenecen al mismo cluster")


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

    print("\nLa distancia total del recorrido, incluyendo las distancias de las ciudades a los aeropuertos, es: " + str(distance) + " kilómetros")


def printReq5(analyzer, airport, indegree, outdegree, s_degree, affected):
    num_affected = lt.size(affected)

    print("Número de afectados con rutas HACIA " + airport + ": " + str(indegree))
    print("Número de afectados con rutas DESDE " + airport + ": " + str(outdegree))
    print("Número de afectados mutuamente conectados con " + airport + ": " + str(s_degree))

    print("\n********************")
    print("Total de afectados: " + str(num_affected))
    print("********************")
    AirportsMap = analyzer["AirportsMap"]

    for pos_affected in range(3):
        if num_affected >= num_affected:
            IATA_code = lt.getElement(affected, pos_affected)
            airport = me.getValue(mp.get(AirportsMap, IATA_code))
            airport_name = airport["Name"]
            airport_city = airport["City"]
            print("Nombre: " + airport_name + "   //   " + "Ciudad: " + airport_city + "   //   " + "Código IATA: " + IATA_code)

    for pos_affected in range(num_affected-2, num_affected+1):
        if pos_affected > 3:
            IATA_code = lt.getElement(affected, pos_affected)
            airport = me.getValue(mp.get(AirportsMap, IATA_code))
            airport_name = airport["Name"]
            airport_city = airport["City"]
            print("Nombre: " + airport_name + "   //   " + "Ciudad: " + airport_city + "   //   " + "Código IATA: " + IATA_code)



while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    print()


    #Carga de datos
    if int(inputs) == 1:
        file_size = input("Ingrese el sufijo del archivo que desea utilizar (small, large, 10pct...): ")
        #file_size = "small"

        print("Cargando información de los archivos ....")
        analyzer = initAnalyzer()

        start_time = process_time()
        loadData(analyzer, file_size)
        stop_time = process_time()
        running_time = (stop_time - start_time)*1000
        
        print("\nTiempo de carga: " + str(running_time) + " milisegundos")
        
        printGraphsInfo(analyzer)



    #Requerimiento 1
    elif int(inputs) == 10:
        start_time = process_time()
        NumberOfAirports, DataInOrder = controller.REQ1(analyzer)
        stop_time = process_time()
        running_time = (stop_time - start_time)*1000

        print("\n\n=============== Requerimiento Número 1 ===============")
        print("Tiempo de ejecución: " + str(running_time) + " milisegundos")
        print("Hay "+str(NumberOfAirports)+" aeropuertos interconectados")
        printReq1(DataInOrder)



    #Requerimiento 2
    elif int(inputs) == 20:
        airport1 = input("Ingrese el código IATA del primer aeropuerto a consultar: ")
        airport2 = input("Ingrese el código IATA del segundo aeropuerto a consultar: ")

        #Para pruebas
        #airport1 = "LED"
        #airport2 = "RTP"

        start_time = process_time()
        num_clusters, same_cluster = controller.REQ2(analyzer, airport1, airport2)
        stop_time = process_time()
        running_time = (stop_time - start_time)*1000

        print("\n=============== Requerimiento Número 2 ===============")
        print("Tiempo de ejecución: " + str(running_time) + " milisegundos")

        printReq2(analyzer, airport1, airport2, num_clusters, same_cluster)    



    #Requerimiento 3
    elif int(inputs) == 30:
        city1 = input("Ingrese el nombre de la ciudad de origen: ")
        city2 = input("Ingrese el nombre de la ciudad de destino: ")

        #Para pruebas
        #city1 = "Saint Petersburg"
        #city2 = "Lisbon"

        homonyms_map = controller.homonymsREQ3(analyzer, city1, city2)
        origin_city, destination_city = chooseHomonymsREQ3(homonyms_map, city1, city2)
        
        start_time = process_time()
        distance, path, origin_airport, destination_airport = controller.REQ3(analyzer, origin_city, destination_city)
        stop_time = process_time()
        running_time = (stop_time - start_time)*1000

        print("\n=============== Requerimiento Número 3 ===============")
        print("Tiempo de ejecución: " + str(running_time) + " milisegundos\n")
        printReq3(distance, path, origin_airport, destination_airport, origin_city, destination_city)



    #Requerimiento 4
    elif int(inputs) == 40:
        miles = float(input("Ingrese la cantidad de millas disponibles: "))

        #Para pruebas
        #miles = 19850

        start_time = process_time()
        num_airports, weight, distance_km = controller.REQ4(analyzer, miles)
        stop_time = process_time()
        running_time = (stop_time - start_time)*1000

        print("\n=============== Requerimiento Número 4 ===============")
        print("Tiempo de ejecución: " + str(running_time) + " milisegundos\n")

        print("Número de aeropuertos posibles: " + str(num_airports))
        print("Suma de la distancia entre aeropuertos: " + str(weight) + " km")
        print("Distancia disponible: " + str(distance_km) + " km")



    #Requerimiento 5
    elif int(inputs) == 50:
        airport = input("Ingrese el IATA del aeropuerto que desea verificar: ")

        #Para pruebas
        #airport = "DXB"

        start_time = process_time()
        req5, indegree, outdegree, s_degree = controller.REQ5(analyzer, airport)
        stop_time = process_time()
        running_time = (stop_time - start_time)*1000

        print("\n=============== Requerimiento Número 5 ===============")
        print("Tiempo de ejecución: " + str(running_time) + " milisegundos\n")
        printReq5(analyzer, airport, indegree, outdegree, s_degree, req5)

        print("\n¿Desea verificar la nueva estructura del grafo tras eliminar el aeropuerto " + airport + "?")
        opcion5 = input("Digite 1 si así lo desea, o 0 de lo contrario: ")

        if opcion5=="1":
            printGraphsInfo(analyzer)    



    else:
        sys.exit(0)


sys.exit(0)