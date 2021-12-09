"""
Reto 4 - model.py

Carlos Arturo Holguín Cárdenas
Daniel Hernández Pineda

"""


import config as cf
from DISClib.Utils import error as error
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import graph as gr
from DISClib.Algorithms.Graphs import dfs
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.DataStructures import edge as e
assert cf

from haversine import haversine

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
               "CitiesMap": None,
               "CoordinateTreeReq3": None,
               "ReversedMainGraphReq5": None} 

    analyzer["MainGraph"] = gr.newGraph(datastructure='ADJ_LIST',
                                       directed=True,
                                       size=100000)
                                       
    analyzer["SecondaryGraph"] = gr.newGraph(datastructure='ADJ_LIST',
                                            directed=False,
                                            size=100000)

    analyzer["AirportsMap"] = mp.newMap(10000,
                                        maptype='PROBING',
                                        loadfactor=0.5)

    analyzer["RoutesMap"] = mp.newMap(93000,
                                      maptype='PROBING',
                                      loadfactor=0.5)
    
    analyzer["CitiesMap"] = mp.newMap(40000,
                                      maptype='PROBING',
                                      loadfactor=0.5)

    analyzer["CoordinateTreeReq3"] = om.newMap(omaptype="RBT")
    
    return analyzer



# ==============================================
# Funciones para agregar informacion al catalogo
# ==============================================
def AddAirport(analyzer, airport):
    """
    Se añade cada aeropuerto al mapa de aeropuertos y a los grafos
    """
    addAirportToMap(analyzer, airport)
    addAirportToGraphs(analyzer, airport)
    addAirportToTreeREQ3(analyzer, airport)


def AddRoute(analyzer, route):
    """
    Se añade cada aeropuerto al mapa de aeropuertos y a los grafos
    """
    addRouteToMainGraph(analyzer, route)
    addRouteToSecondaryGraph(analyzer, route)


def AddCity(analyzer, city):
    """
    Crea una tabla de hash de la forma 'key'= nombre de ciudad, 'value'= hashmap de ciudades homónimas según su id
    """
    CitiesMap = analyzer["CitiesMap"]
    city_name = city["city_ascii"]
    city_id = city["id"]
    city_data = cityData(city)
    exists_city= mp.contains(CitiesMap, city_name)
    
    if not exists_city:    #Se crea la llave y el hashmap de ciudades homónimas
        homonym_cities = mp.newMap()
        mp.put(homonym_cities, city_id, city_data)
        mp.put(CitiesMap, city_name, homonym_cities)
    
    else:                  #Se añade la información de la ciudad en la entrada ya existente
        entry = mp.get(CitiesMap, city_name)
        homonym_cities = me.getValue(entry)
        mp.put(homonym_cities, city_id, city_data)


def CreateReversedMainGraphREQ5(analyzer):
    analyzer["ReversedMainGraphReq5"] = scc.reverseGraph(analyzer["MainGraph"])


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



# ==============================================
# Funciones para creacion de datos
# ==============================================
def addAirportToMap(analyzer, airport):
    """
    Se añade un aeropuerto al un mapa de aeropuertos según su código IATA
    """
    AirportsMap = analyzer["AirportsMap"]
    mp.put(AirportsMap, airport["IATA"], airport)


def addAirportToGraphs(analyzer, airport):
    """
    Se añaden los códigos IATA de los aeropuertos como vértices del grafo principal
    """
    MainGraph = analyzer["MainGraph"]
    SecondaryGraph = analyzer["SecondaryGraph"]
    iata_code = airport["IATA"]
    gr.insertVertex(MainGraph, iata_code)
    gr.insertVertex(SecondaryGraph, iata_code)


def addAirportToTreeREQ3(analyzer, airport):
    """
    Crea un árbol cuyos nodos son de la forma 'key'= longitud, 'value'= árbol de ciudades según latitud
    """
    LongitudeTree = analyzer["CoordinateTreeReq3"]
    longitude = round(float(airport["Longitude"]),2)
    latitude = round(float(airport["Latitude"]),2)
    longitude_entry = om.get(LongitudeTree, longitude)

    if longitude_entry is None:
        LatitudeTree = om.newMap(omaptype="RBT")
        om.put(LatitudeTree, latitude, airport)
        om.put(LongitudeTree, longitude, LatitudeTree)

    else:
        LatitudeTree= me.getValue(longitude_entry)
        om.put(LatitudeTree, latitude, airport)
        #No hace falta verificar la entrada porque no hay dos aeropuertos en la misma coordenada    


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

    city_data = {"name": city["city_ascii"],
                 "id": city["id"],
                 "country": city["country"],
                 "latitude": round(float(city["lat"]),2),
                 "longitude": round(float(city["lng"]),2)}
    
    return city_data



# ==============================================
# Funciones de consulta
# ==============================================

#Requerimiento 2
def REQ2(analyzer, airport1, airport2):
    MainGraph = analyzer["MainGraph"]
    kosaraju_scc = scc.KosarajuSCC(MainGraph)
    num_clusters = kosaraju_scc["components"]
    same_cluster = scc.stronglyConnected(kosaraju_scc, airport1, airport2)

    return num_clusters, same_cluster


#Requerimiento 3
def homonymsREQ3(analyzer, city1, city2):
    CitiesMap = analyzer["CitiesMap"]
    origin_homonyms = me.getValue(mp.get(CitiesMap, city1))
    destination_homonyms = me.getValue(mp.get(CitiesMap, city2))
    
    homonyms_map = mp.newMap(numelements=2, loadfactor = 4)
    mp.put(homonyms_map, "origin", origin_homonyms)
    mp.put(homonyms_map, "destination", destination_homonyms)

    return homonyms_map


def calculateRangeREQ3(lon_low, lon_high, lat_low, lat_high):
    
    lon_low = lon_low - 5
    lon_high = lon_high + 5
    lat_low = lat_low - 5
    lat_high = lat_high + 5

    return lon_low, lon_high, lat_low, lat_high


def findNearestAirportREQ3(analyzer, city):

    LongitudeTree = analyzer["CoordinateTreeReq3"]
    city_longitude = city["longitude"]
    city_latitude = city["latitude"]
    coord_city = (city_latitude, city_longitude) #(lat,long)
    lon_low, lon_high, lat_low, lat_high = calculateRangeREQ3(city_longitude, city_longitude,
                                                              city_latitude, city_latitude)
    
    final_airport = None
    min_distance = 100000000000000000000000000
    found = False
    
    while not found:
        longitudesInRange = om.values(LongitudeTree, lon_low, lon_high)
        longitude_size = lt.size(longitudesInRange)
        pos_longitude = 1
        
        while pos_longitude <= longitude_size:
            LatitudeTree = lt.getElement(longitudesInRange, pos_longitude)
            latitudesInRange = om.values(LatitudeTree, lat_low, lat_high)
            latitudes_size = lt.size(latitudesInRange)
            pos_latitude = 1
            
            while pos_latitude <= latitudes_size:
                found = True
                airport = lt.getElement(latitudesInRange, pos_latitude)
                coord_airport = (float(airport["Latitude"]),float(airport["Longitude"]))
                distance = haversine(coord_city, coord_airport)
                
                if distance < min_distance:
                    final_airport = airport
                    min_distance = distance

                pos_latitude += 1
            pos_longitude += 1

        lon_low, lon_high, lat_low, lat_high = calculateRangeREQ3(city_longitude, city_longitude,
                                                                  city_latitude, city_latitude)

    return final_airport, distance


def REQ3(analyzer, origin_city, destination_city):
    origin_airport, origin_airport_distance = findNearestAirportREQ3(analyzer, origin_city)
    destination_airport, destination_airport_distance = findNearestAirportREQ3(analyzer, destination_city)

    search = djk.Dijkstra(analyzer["MainGraph"], origin_airport["IATA"])
    path = djk.pathTo(search, destination_airport["IATA"])
    distance_between_airports = djk.distTo(search, destination_airport["IATA"])
    
    total_distance = round(origin_airport_distance + destination_airport_distance + distance_between_airports,3)

    return total_distance, path, origin_airport, destination_airport


#Requerimiento 5
def getUnrepeatedREQ5(in_affected, out_affected):
    affected_map = mp.newMap()

    size_in = lt.size(in_affected)
    pos_in = 1

    while pos_in <= size_in:
        airport = lt.getElement(in_affected, pos_in)
        mp.put(affected_map, airport, 0)
        pos_in +=1


    size_out = lt.size(out_affected)
    pos_out = 1

    while pos_out <= size_out:
        airport = lt.getElement(out_affected, pos_out)
        mp.put(affected_map, airport, 0)
        pos_out +=1

    affected = mp.keySet(affected_map)
    
    return affected


def removeEdgeREQ5(graph, vertexa, vertexb):
    """
    Elimina el arco asociado a los vertices vertexa ---- vertexb

    Args:
        graph: El grafo sobre el que se ejecuta la operacion
        vertexa: Vertice de inicio
        vertexb: Vertice destino

    Raises:
        Exception
    """
    try:
        element = mp.get(graph['vertices'], vertexa)
        lst = element['value']
        i = 1
        lst_size = lt.size(lst)

        while i<=lst_size: #E recorridos en el peor caso
            edge = lt.getElement(lst, i)
            if (graph['directed']):
                if (e.either(edge) == vertexa) and ((e.other(edge, e.either(edge)) == vertexb)):
                    lt.deleteElement(lst, i) #E recorridos en el peor caso
                    break

            elif(e.either(edge) == vertexa or (e.other(edge, e.either(edge)) == vertexa)):
                if (e.either(edge) == vertexb or
                   (e.other(edge, e.either(edge)) == vertexb)):
                    lt.deleteElement(lst, i) #E recorridos en el peor caso
                    break
            i+=1
        graph["edges"] -= 1
        
    except Exception as exp:
        error.reraise(exp, 'ajlist:getedge')


def removeVertexREQ5(analyzer, airport, in_affected, out_affected):
    MainGraph = analyzer["MainGraph"]
    SecondaryGraph = analyzer["SecondaryGraph"]
    num_in = lt.size(in_affected)
    num_out = lt.size(out_affected)

    #Eliminar el vértice y todas las rutas que salen de él
    mp.remove(MainGraph["vertices"], airport) #Cte porque la lista 'table' es un arreglo
    mp.remove(SecondaryGraph["vertices"], airport)
    MainGraph["edges"] -= num_out

    #Ajustar los indegree en el digrafo
    mp.remove(MainGraph["indegree"], airport)
    pos_out = 1
    while pos_out<=num_out: #V recorridos en el peor caso
        out_airport = lt.getElement(out_affected, pos_out)
        actual_indegree = me.getValue(mp.get(MainGraph["indegree"], out_airport))
        mp.put(MainGraph["indegree"], out_airport, actual_indegree-1)
        pos_out += 1

    #Eliminar las rutas que llegan al vértice desde los demás vértices
    pos_in = 1
    while pos_in <= num_in: #V recorridos en el peor caso
        in_airport = lt.getElement(in_affected, pos_in)
        removeEdgeREQ5(MainGraph, in_airport, airport) #E^2 recorridos en el peor caso
        removeEdgeREQ5(SecondaryGraph, in_airport, airport) #E^2 recorridos en el peor caso
        pos_in += 1


def REQ5(analyzer, airport):
    MainGraph = analyzer["MainGraph"]
    ReversedMainGraph = analyzer["ReversedMainGraphReq5"]
    
    in_affected = gr.adjacents(ReversedMainGraph, airport)
    out_affected = gr.adjacents(MainGraph, airport)
    indegree = gr.indegree(MainGraph, airport)
    outdegree = gr.outdegree(MainGraph, airport)

    affected = getUnrepeatedREQ5(in_affected, out_affected)

    removeVertexREQ5(analyzer, airport, in_affected, out_affected)
    
    return affected, indegree, outdegree

