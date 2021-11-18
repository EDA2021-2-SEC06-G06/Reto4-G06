"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from datetime import datetime, date
from time import process_time
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

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

def initCatalog():
    """
    Inicializa el catálogo
    """
    return controller.initCatalog()


def loadData(catalog, file_size):
    """
    Carga las obras en la estructura de datos
    """
    controller.loadData(catalog, file_size)

while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")

    elif int(inputs[0]) == 2:
        pass
    if int(inputs) == 1:
        #file_size = input("Ingrese el sufijo del archivo que desea utilizar (small, large, 10pct...): ")
        file_size = "small"

        #Cargar archivos
        print("\nCargando información de los archivos ....")
        catalog = initCatalog()

        start_time = process_time()
        loadData(catalog, file_size)
        stop_time = process_time()
        running_time = (stop_time - start_time)*1000

        print("\nTiempo de carga: " + str(running_time) + " milisegundos")


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

        start_time = process_time()
        #req3 = controller.REQ3(catalog)
        stop_time = process_time()
        running_time = (stop_time - start_time)*1000

        print("\n\n=============== Requerimiento Número 3 ===============")
        #print("Tiempo de ejecución: " + str(running_time) + " milisegundos")



    #Requerimiento 4
    elif int(inputs) == 40:

        start_time = process_time()
        #req4 = controller.REQ4(catalog)
        stop_time = process_time()
        running_time = (stop_time - start_time)*1000

        print("\n\n=============== Requerimiento Número 4 ===============")
        #print("Tiempo de ejecución: " + str(running_time) + " milisegundos\n")



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