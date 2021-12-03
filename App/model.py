"""
Reto 4 - model.py

Carlos Arturo Holguín Cárdenas
Daniel Hernández Pineda

"""


import config as cf
from DISClib.Utils import error as error
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import graph as gr
from DISClib.Algorithms.Graphs import dfo
from DISClib.Algorithms.Graphs import dfs
from DISClib.Algorithms.Graphs import scc
assert cf


# ==============================================
# Construccion de modelos
# ==============================================
def newAnalyzer():
    """
    Inicializa el catálogo de avistamientos
    """
    analyzer = {"MainGraph": None,
               "SecondaryGraph": None,
               "AirportsMap": None,
               "RoutesMap": None,
               "CitiesMap": None} 

    analyzer["MainGraph"] = gr.newGraph(datastructure='ADJ_LIST',
                                       directed=True,
                                       size=10000)
                                       #comparefunction=compareStopIds)
                                       
    analyzer["SecondaryGraph"] = gr.newGraph(datastructure='ADJ_LIST',
                                            directed=False,
                                            size=10000)
                                            #comparefunction=compareStopIds)

    analyzer["AirportsMap"] = mp.newMap(10000,
                                        maptype='PROBING',
                                        loadfactor=0.5)

    analyzer["RoutesMap"] = mp.newMap(10,
                                      maptype='PROBING',
                                      loadfactor=0.5)
    
    analyzer["CitiesMap"] = mp.newMap(40000,
                                      maptype='PROBING',
                                      loadfactor=0.5)
    
    return analyzer


# Funciones para agregar informacion al catalogo
def AddAirport(analyzer, airport):
    """
    Se añade cada aeropuerto al mapa de aeropuertos y a los grafos
    """
    addAirportToMap(analyzer, airport)
    addAirportToMainGraph(analyzer, airport)


def AddRoute(analyzer, route):
    """
    Se añade cada aeropuerto al mapa de aeropuertos y a los grafos
    """
    addRouteToMainGraph(analyzer, route)
    addRouteToSecondaryGraph(analyzer, route)


def AddCity(analyzer, city):
    """
    Crea una tabla de hash de la forma 'key'= nombre de ciudad, 'value'= lista de ciudades homónimas
    """
    CitiesMap = analyzer["CitiesMap"]
    city_name = city["city_ascii"]
    city_data = cityData(city)
    exists_city= mp.contains(CitiesMap, city_name)
    
    if not exists_city:    #Se crea la llave y la lista de ciudades homónimas
        homonym_cities = lt.newList("ARRAY_LIST")
        lt.addLast(homonym_cities, city_data)
        mp.put(CitiesMap, city_name, homonym_cities)
    
    else:                  #Se añade la información de la ciudad en la entrada ya existente
        entry = mp.get(CitiesMap, city_name)
        homonym_cities = me.getValue(entry)
        lt.addLast(homonym_cities, city_data)


def AddRouteND(analyzer, route):
    """
    Se añade la ruta como un arco entre sus aeropuertos correspondientes
    """ 
    pos=1
    MainGraph = analyzer["MainGraph"]   
    SecondaryGraph = analyzer["SecondaryGraph"]
    sizeEdges= gr.numEdges(MainGraph)
    Vertices=gr.vertices(MainGraph)
    SizeVertices=lt.size(Vertices)
    while pos<=SizeVertices:
        MapOfJointVertices= mp.newMap()
        Vertice= lt.getElement(Vertices, pos)
        dfs.dfsVertex(MapOfJointVertices, MainGraph, Vertice)
        pos+=1
        cat=1
    Gau=dfs.DepthFirstSearch(MainGraph,"AAE")
    miaau=1


# Funciones para creacion de datos
def addAirportToMap(analyzer, airport):
    """
    Se añaden los aeropuertos a un mapa según su código IATA
    """
    AirportsMap = analyzer["AirportsMap"]
    airport_info = mp.newMap(numelements=5, maptype="CHAINING", loadfactor=4)
 
    mp.put(airport_info, "Name", airport["Name"])
    mp.put(airport_info, "City", airport["City"])
    mp.put(airport_info, "Country", airport["Country"])
    mp.put(airport_info, "Latitude", airport["Latitude"])
    mp.put(airport_info, "Longitude", airport["Longitude"])

    mp.put(AirportsMap, airport["IATA"], airport_info)


def addAirportToMainGraph(analyzer, airport):
    """
    Se añaden los códigos IATA de los aeropuertos como vértices del grafo principal
    """
    MainGraph = analyzer["MainGraph"]
    SecondaryGraph = analyzer["SecondaryGraph"]
    iata_code = airport["IATA"]
    gr.insertVertex(MainGraph, iata_code)
    gr.insertVertex(SecondaryGraph, iata_code)


def addRouteToMainGraph(analyzer, route):
    """
    Se añade la ruta como un arco entre sus aeropuertos correspondientes
    """    
    MainGraph = analyzer["MainGraph"]
    origin = route["Departure"]
    destination = route["Destination"]
    distance = float(route["distance_km"])

    edge = gr.getEdge(MainGraph, origin, destination)
    if edge is None:
        gr.addEdge(MainGraph, origin, destination, distance)


def addRouteToMap(analyzer, airport1, airport2, distance):
    """
    Se agrega una ruta entre dos aeropuertos al mapa de rutas
    """
    RoutesMap = analyzer["RoutesMap"]
    airport1_entry = mp.get(RoutesMap, airport1)
    
    if airport1_entry is None:    
        airport1_map = mp.newMap(numelements=100, loadfactor=4)
        mp.put(airport1_map, airport2, distance)
        mp.put(RoutesMap, airport1, airport1_map)

    else:
        airport1_map = me.getValue(airport1_entry)
        mp.put(airport1_map, airport2, distance)


def addRouteToSecondaryGraph(analyzer, route):
    """
    Se agrega una ruta al grafo si en un mapa auxiliar se tiene registro de una ruta inversa a la actual
    Nota: si la ruta actual es de la forma origen->destino, entonces la ruta inversa se refiere a que es
    de la forma destino->origen
    """    
    SecondaryGraph = analyzer["SecondaryGraph"]
    RoutesMap = analyzer["RoutesMap"]
    origin = route["Departure"]
    destination = route["Destination"]
    distance = float(route["distance_km"])

    edge = gr.getEdge(SecondaryGraph, origin, destination)
    
    if edge is None: #Verificar si ya existe una ruta entre los aeropuertos
        destination_entry = mp.get(RoutesMap, destination)
        
        if destination_entry is not None: #Para determinar si existe ruta desde destination hasta origin
            destination_map = me.getValue(destination_entry)
            strongly_connected = mp.get(destination_map, origin) is not None
             
            if strongly_connected: #Los aeropuertos tienen rutas entre sí
                gr.addEdge(SecondaryGraph, origin, destination, distance)

    addRouteToMap(analyzer, origin, destination, distance) 
            

def cityData(city):
    "Filtra la información relevante de determinada ciudad"

    city_data = {"country": city["country"],
                 "id": city["id"],
                 "latitude": city["lat"],
                 "longitude": city["lng"]}
    
    return city_data


# Funciones de consulta
def REQ2(analyzer, airport1, airport2):
    MainGraph = analyzer["MainGraph"]
    kosaraju_scc = scc.KosarajuSCC(MainGraph)
    num_clusters = kosaraju_scc["components"]
    same_cluster = scc.stronglyConnected(kosaraju_scc, airport1, airport2)

    return num_clusters, same_cluster


def homonymsREQ3(analyzer, city1, city2):
    CitiesMap = analyzer["CitiesMap"]
    origin_homonyms = me.getValue(mp.get(CitiesMap, city1))
    destination_homonyms = me.getValue(mp.get(CitiesMap, city2))
    
    homonyms_map = mp.newMap(numelements=2, loadfactor = 4)
    mp.put(homonyms_map, "origin", origin_homonyms)
    mp.put(homonyms_map, "destination", destination_homonyms)

    return homonyms_map


def REQ5(analyzer, airport):
    MainGraph = analyzer["MainGraph"]
    SecondaryGraph = analyzer["SecondaryGraph"]
    affected_routes = gr.adjacentEdges(MainGraph, airport)
    
    affected = gr.adjacents(SecondaryGraph, airport)
    indegree = gr.indegree(MainGraph, airport)
    outdegree = gr.outdegree(MainGraph, airport)

    """
    num_routes = lt.size(affected_routes)
    i=1
    while i<=num_routes:
        route = lt.getElement(affected_routes, i)
        print(route)
        i+=1"""

    return affected, indegree, outdegree




# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento



"""#PRUEBA
test_graph = gr.newGraph(datastructure='ADJ_LIST', directed=True, size=7)
gr.insertVertex(test_graph, "A")
gr.insertVertex(test_graph, "B")
gr.insertVertex(test_graph, "C")
gr.insertVertex(test_graph, "D")
gr.insertVertex(test_graph, "E")

gr.addEdge(test_graph, "A", "B")
gr.addEdge(test_graph, "A", "D")
gr.addEdge(test_graph, "B", "A")
gr.addEdge(test_graph, "C", "E")
gr.addEdge(test_graph, "D", "A")
gr.addEdge(test_graph, "D", "E")
gr.addEdge(test_graph, "E", "C")


scc_test = scc.KosarajuSCC(test_graph)

print(scc_test)"""