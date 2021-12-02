"""
Reto 4 - model.py

Carlos Arturo Holguín Cárdenas
Daniel Hernández Pineda

"""


import config as cf
from DISClib.Utils import error as error
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import graph as gr
from DISClib.Algorithms.Graphs import dfs as dfs
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# ==============================================
# Construccion de modelos
# ==============================================
def newAnalyzer():
    """
    Inicializa el catálogo de avistamientos
    """
    analyzer = {"MainGraph": None,
               "SecondaryGraph": None,
               "AirportsMap": None} 

    analyzer["MainGraph"] = gr.newGraph(datastructure='ADJ_LIST',
                                       directed=True,
                                       size=93000)
                                       #comparefunction=compareStopIds)
                                       
    analyzer["SecondaryGraph"] = gr.newGraph(datastructure='ADJ_LIST',
                                            directed=False,
                                            size=2)
                                            #comparefunction=compareStopIds)

    analyzer["AirportsMap"] = mp.newMap(9100,
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
    iata_code = airport["IATA"]
    gr.insertVertex(MainGraph, iata_code)


# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento


"""
#PRUEBAS
analyzer = newAnalyzer()
secundario = analyzer["SecondaryGraph"]

vertex1 = "ABC"
gr.insertVertex(secundario, vertex1)

vertex2 = "DEF"
gr.insertVertex(secundario, vertex2)


gr.addEdge(secundario, vertex1, vertex2, 50)

print(gr.numEdges(secundario))
print(gr.numVertices(secundario))"""