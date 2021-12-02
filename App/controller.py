﻿"""
Reto 4 - controller.py

Carlos Arturo Holguín Cárdenas
Daniel Hernández Pineda

"""

import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

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
def loadData(analyzer):
    loadAirports(analyzer)
    loadRoutes(analyzer)


def loadAirports(analyzer):
    airports_file = cf.data_dir + "airports_full.csv"
    input_file = csv.DictReader(open(airports_file, encoding='utf-8'))

    for airport in input_file:
        model.AddAirport(analyzer, airport)


def loadRoutes(analyzer):
    routes_file = cf.data_dir + "routes_full.csv"
    input_file = csv.DictReader(open(routes_file, encoding='utf-8'))

    for route in input_file:
        model.AddRoute(analyzer, route)
        model.AddRouteND(analyzer, route)



# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
