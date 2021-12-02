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
    Se añade la ruta como un arco entre sus aeropuertos correspondientes
    """    
    MainGraph = analyzer["MainGraph"]
    origin = route["Departure"]
    destination = route["Destination"]
    distance = float(route["distance_km"])

    edge = gr.getEdge(MainGraph, origin, destination)
    if edge is None:
        gr.addEdge(MainGraph, origin, destination, distance)


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
    iata_code = airport["IATA"]
    gr.insertVertex(MainGraph, iata_code)


def cityData(city):
    "Filtra la información relevante de determinada ciudad"

    city_data = {"country": city["country"],
                 "id": city["id"],
                 "latitude": city["lat"],
                 "longitude": city["lng"]}
    
    return city_data


# Funciones de consulta
def homonymsREQ4(analyzer, city1, city2):
    CitiesMap = analyzer["CitiesMap"]
    origin_homonyms = me.getValue(mp.get(CitiesMap, city1))
    destination_homonyms = me.getValue(mp.get(CitiesMap, city2))
    
    homonyms_map = mp.newMap(numelements=2, loadfactor = 4)
    mp.put(homonyms_map, "origin", origin_homonyms)
    mp.put(homonyms_map, "destination", destination_homonyms)

    return homonyms_map


# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento
