"""
Reto 4 - controller.py

Carlos Arturo Holguín Cárdenas
Daniel Hernández Pineda

"""

from App.model import CreateReversedMainGraphREQ5
import config as cf
import model
import csv


# ==============================================
# Inicialización del analizador
# ==============================================
def initAnalyzer():
    """
    Llama la funcion de inicializació del catálogo del modelo
    """
    analyzer = model.newAnalyzer()
    return analyzer


# ==============================================
# Funciones para la carga de datos
# ==============================================
def loadData(analyzer, file_size):
    loadAirports(analyzer, file_size)
    loadRoutes(analyzer, file_size)
    loadCities(analyzer)
    CreateReversedMainGraphREQ5(analyzer)


def loadAirports(analyzer, file_size):
    airports_file = cf.data_dir + "airports-utf8-" + file_size + '.csv'
    input_file = csv.DictReader(open(airports_file, encoding='utf-8'))

    for airport in input_file:
        model.AddAirport(analyzer, airport)


def loadRoutes(analyzer, file_size):
    routes_file = cf.data_dir + "routes-utf8-" + file_size + '.csv'
    input_file = csv.DictReader(open(routes_file, encoding='utf-8'))

    for route in input_file:
        model.AddRoute(analyzer, route)
        #model.AddRouteND(analyzer, route)


def loadCities(analyzer):
    cities_file = cf.data_dir + "worldcities-utf8.csv"
    input_file = csv.DictReader(open(cities_file, encoding='utf-8'))

    for city in input_file:
        model.AddCity(analyzer, city)


# ==============================================
# Funciones de ordenamiento
# ==============================================


# ==============================================
# Funciones de consulta sobre el analizador
# ==============================================
def REQ1(analyzer):
    return model.REQ1(analyzer)

def REQ2(analyzer, airport1, airport2):
    return model.REQ2(analyzer, airport1, airport2)

def homonymsREQ3(analyzer, city1, city2):
    return model.homonymsREQ3(analyzer, city1, city2)

def REQ3(analyzer, origin, destination):
    return model.REQ3(analyzer, origin, destination)

def REQ4(analyzer, Origin, miles):
    return model.REQ4(analyzer, Origin, miles)

def REQ5(analyzer, airport):
    return model.REQ5(analyzer, airport)
