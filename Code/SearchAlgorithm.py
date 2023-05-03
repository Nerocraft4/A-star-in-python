# This file contains all the required routines to make an A* search algorithm.
#
__authors__ = '1600959'
__group__ = 'Pau Blasco Roca'

# _________________________________________________________________________________________
# Intel.ligencia Artificial
# Curs 2020- 2021
# Universitat Autonoma de Barcelona
# _______________________________________________________________________________________

from SubwayMap import *
from utils import *
import os
import math
import copy
#import time


def expand(path, map):
    """
     It expands a SINGLE station and returns the list of class Path.
     Format of the parameter is:
        Args:
            path (object of Path class): Specific path to be expanded
            map (object of Map class):: All the information needed to expand
            the node
        Returns:
            path_list (list): List of paths that are connected to the given path.
    """
    path_list = []  # comencem amb una llista buida
    # mirar amb la matriu d'adjacència amb quines estacions connecta el path.last
    current_station = path.last
    current_station_connections = map.connections[current_station]
    for station in current_station_connections.keys():
        #important to use deepcopy as if we don't it breaks the logic
        new_path = copy.deepcopy(path)
        new_path.add_route(int(station))
        path_list.append(new_path)
    return path_list


def remove_cycles(path_list):
    """
     It removes from path_list the set of paths that include some cycles in
     their path.
     Format of the parameter is:
        Args:
            path_list (LIST of Path Class): Expanded paths
        Returns:
            path_list (list): Expanded paths without cycles.
    """
    for path in path_list:
        unique_stations = set(path.route)
        if len(unique_stations) < len(path.route):
            path_list.remove(path)
    return path_list


def insert_depth_first_search(expand_paths, list_of_path):
    """
     expand_paths is inserted to the list_of_path according to DEPTH FIRST
     SEARCH algorithm
     Format of the parameter is:
        Args:
            expand_paths (LIST of Path Class): Expanded paths
            list_of_path (LIST of Path Class): The paths to be visited
        Returns:
            list_of_path (LIST of Path Class): List of Paths where Expanded
            Path is inserted
    """
    for path in expand_paths[::-1]:
        list_of_path.append(path)
    return list_of_path


def depth_first_search(origin_id, destination_id, map):
    """
     Depth First Search algorithm
     Format of the parameter is:
        Args:
            origin_id (int): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
        Returns:
            list_of_path[0] (Path Class): the route that goes from origin_id
            to destination_id
    """
    new_path = Path(origin_id)
    open_paths = [new_path]
    while open_paths[-1].last != destination_id and open_paths != []:
        head_path = open_paths[-1]
        open_paths.pop()
        expanded_paths = expand(head_path, map)
        expanded_paths = remove_cycles(expanded_paths)
        open_paths = insert_depth_first_search(expanded_paths, open_paths)
        open_paths = remove_cycles(open_paths)
    if open_paths:
        return [open_paths[-1]][0]
    else:
        return "No existeix solució"


def insert_breadth_first_search(expand_paths, list_of_path):
    """
        expand_paths is inserted to the list_of_path according to BREADTH FIRST
        SEARCH algorithm
        Format of the parameter is:
           Args:
               expand_paths (LIST of Path Class): Expanded paths
               list_of_path (LIST of Path Class): The paths to be visited
           Returns:
               list_of_path (LIST of Path Class): List of Paths where Expanded
               Path is inserted
    """
    # els afegim al final, ja que és al revés de la teoria.
    # voldrem expandir sempre path.last
    expand_paths = expand_paths[::-1]
    for path in list_of_path:
        expand_paths.append(path)
    return expand_paths


def breadth_first_search(origin_id, destination_id, map):
    """
     Breadth First Search algorithm
     Format of the parameter is:
        Args:
            origin_id (int): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
        Returns:
            list_of_path[0] (Path Class): The route that goes from origin_id to
            destination_id
    """
    new_path = Path(origin_id)
    open_paths = [new_path]
    while open_paths[-1].last != destination_id and open_paths != []:
        head_path = open_paths[-1]
        open_paths.pop()
        expanded_paths = expand(head_path, map)
        expanded_paths = remove_cycles(expanded_paths)
        open_paths = insert_breadth_first_search(expanded_paths, open_paths)
        open_paths = remove_cycles(open_paths)
    if open_paths:
        return [open_paths[-1]][0]
    else:
        return "No existeix solució"


def calculate_cost(expand_paths, map, type_preference):
    """
         Calculate the cost according to type preference
         Format of the parameter is:
            Args:
                expand_paths (LIST of Paths Class): Expanded paths
                map (object of Map class): All the map information
                type_preference: INTEGER Value to indicate the preference selected:
                                0 - Adjacency
                                1 - minimum Time
                                2 - minimum Distance
                                3 - minimum Transfers
            Returns:
                expand_paths (LIST of Paths): Expanded path with updated cost
    """
    if type_preference==0: #adjacency (n nodes)
        for path in expand_paths:
            if len(path.route)!=1:
                path.g+=1
        return expand_paths
    elif type_preference==1: #time
        for path in expand_paths:
            path.g += map.connections[path.last][path.penultimate]
        return expand_paths
    elif type_preference==2:
        for path in expand_paths:
            #cal multiplicar per la VELOCITAT
            #cada línia te la seva VELOCITAT, a myMap.stations
            if(map.stations[path.last]["line"]==map.stations[path.penultimate]["line"]):
                line = map.stations[path.last]["line"]
                velocity = map.velocity
                path.g += map.connections[path.last][path.penultimate] * velocity[line]
        #print_list_of_path_with_cost(expand_paths)
            #nota: en els transbords, considerem distància zero?
        return expand_paths
    elif type_preference==3:
        for path in expand_paths:
            if(map.stations[path.last]["line"]!=map.stations[path.penultimate]["line"]):
                #si les línies són diferents, hi ha un Transfer
                #print("Transfer!")
                path.g += 1
        return expand_paths
    else:
        return "Incorrect type_preference"
    return expand_paths


def insert_cost(expand_paths, list_of_path):
    """
        expand_paths is inserted to the list_of_path according to COST VALUE
        Format of the parameter is:
           Args:
               expand_paths (LIST of Path Class): Expanded paths
               list_of_path (LIST of Path Class): The paths to be visited
           Returns:
               list_of_path (LIST of Path Class): List of Paths where
               expanded_path is inserted according to cost
    """
    #this seems to be better than inserting one by one (as I did first)
    #since inserting one by one (com jo ho feia) is O(n^2) and sort is O(n*log(n))
    list_of_path = list_of_path + expand_paths
    list_of_path.sort(key=lambda path:[path.g, len(path.route)])
    return list_of_path[::-1]


def uniform_cost_search(origin_id, destination_id, map, type_preference=0):
    """
     Uniform Cost Search algorithm
     Format of the parameter is:
        Args:
            origin_id (int): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
        Returns:
            list_of_path[0] (Path Class): The route that goes from origin_id
            to destination_id
    """
    new_path = Path(origin_id)
    open_paths = [new_path]
    while open_paths != [] and open_paths[-1].last != destination_id:
        head_path = open_paths[-1]
        open_paths.pop()
        expanded_paths = expand(head_path, map)
        expanded_paths = remove_cycles(expanded_paths)
        expanded_paths = calculate_cost(expanded_paths, map, type_preference)
        open_paths = insert_cost(expanded_paths, open_paths)
        open_paths = remove_cycles(open_paths)

    if open_paths:
        return [open_paths[-1]][0]
    else:
        return "No existeix solució"


def calculate_heuristics(expand_paths, map, destination_id, type_preference=0):
    """
     Calculate and UPDATE the heuristics of a path according to type preference
     WARNING: In calculate_cost, we didn't update the cost of the path inside
              the function for the reasons which will be clear when you code
              Astar (HINT: check remove_redundant_paths() function).
     Format of the parameter is:
        Args:
            expand_paths (LIST of Path Class): Expanded paths
            map (object of Map class): All the map information
            type_preference: INTEGER Value to indicate the preference selected:
                            0 - Adjacency
                            1 - minimum Time
                            2 - minimum Distance
                            3 - minimum Transfers
        Returns:
            expand_paths (LIST of Path Class): Expanded paths with updated
            heuristics
    """
    if (type_preference==0):
        for path in expand_paths:
            if(path.last==destination_id):
                path.h = 0
            else:
                path.h = 1
        return expand_paths
    elif (type_preference==1):
        max_speed = max(map.velocity.values())
        for path in expand_paths:
            point_a = map.stations[path.last]
            point_b = map.stations[destination_id]
            a = [point_a['x'], point_a['y']]
            b = [point_b['x'], point_b['y']]
            path.h = euclidean_dist(a,b)/max_speed
        return expand_paths
    elif (type_preference==2):
        max_speed = max(map.velocity)
        for path in expand_paths:
            point_a = map.stations[path.last]
            point_b = map.stations[destination_id]
            a = [point_a['x'], point_a['y']]
            b = [point_b['x'], point_b['y']]
            path.h = euclidean_dist(a,b)
        return expand_paths
    elif (type_preference==3):
        for path in expand_paths:
            if(map.stations[path.last]["line"]==map.stations[path.penultimate]["line"]):
                path.h = 0
            else:
                path.h = 1

        return expand_paths

    pass


def update_f(expand_paths):
    """
      Update the f of a path
      Format of the parameter is:
         Args:
             expand_paths (LIST of Path Class): Expanded paths
         Returns:
             expand_paths (LIST of Path Class): Expanded paths with updated costs
    """
    for path in expand_paths:
        path.update_f()
    return expand_paths


def remove_redundant_paths(expand_paths, list_of_path, visited_stations_cost):
    """
      It removes the Redundant Paths. They are not optimal solution!
      If a station is visited and have a lower g in this moment, we should
      remove this path.
      Format of the parameter is:
         Args:
             expand_paths (LIST of Path Class): Expanded paths
             list_of_path (LIST of Path Class): All the paths to be expanded
             visited_stations_cost (dict): All visited stations cost
         Returns:
             new_paths (LIST of Path Class): Expanded paths without redundant paths
             list_of_path (LIST of Path Class): list_of_path without redundant paths
    """
    new_expanded_paths = []
    new_list_of_paths = []
    for path in expand_paths:
        if(path.last in visited_stations_cost.keys()):
            if(path.g<=visited_stations_cost[path.last]):
                new_expanded_paths.append(path)
                visited_stations_cost[path.last]=path.g
        else:
            new_expanded_paths.append(path)
            visited_stations_cost[path.last]=path.g
    for path in list_of_path:
        if(path.g<=visited_stations_cost[path.last]):
            new_list_of_paths.append(path)
            visited_stations_cost[path.last]=path.g
    return new_expanded_paths, new_list_of_paths, visited_stations_cost


def insert_cost_f(expand_paths, list_of_path):
    """
        expand_paths is inserted to the list_of_path according to f VALUE
        Format of the parameter is:
           Args:
               expand_paths (LIST of Path Class): Expanded paths
               list_of_path (LIST of Path Class): The paths to be visited
           Returns:
               list_of_path (LIST of Path Class): List of Paths where
               expanded_path is inserted according to f
    """
    for path_to_add in expand_paths:
        inserted = 0
        index = 0
        while inserted == 0 and index<len(list_of_path):
            if list_of_path[index].f <= path_to_add.f:
                list_of_path.insert(index, path_to_add)
                inserted = 1
            else:
                index += 1
        if index==len(list_of_path):
            list_of_path.append(path_to_add)
    return list_of_path


def coord2station(coord, map):
    """
        From coordinates, it searches the closest station.
        Format of the parameter is:
        Args:
            coord (list):  Two REAL values, which refer to the coordinates
            of a point in the city.
            map (object of Map class): All the map information
        Returns:
            possible_origins (list): List of the Indexes of stations, which
            corresponds to the closest station
    """
    min_dist = 100000
    possible_origins = []
    for identifier in map.stations:
        station = map.stations[identifier]
        distance_to_station = euclidean_dist(coord, [station['x'], station['y']])
        if distance_to_station <= min_dist:
            if distance_to_station == min_dist:
                possible_origins.append(identifier)
            else:
                possible_origins = [identifier]
                min_dist = distance_to_station
    return possible_origins


def Astar(origin_coor, destin_coor, map, type_preference=0):
    """
     A* Search algorithm
     Format of the parameter is:
        Args:
            origin_coor (list): Starting station coords
            dest_coor (int): Final station coords
            map (object of Map class): All the map information
            type_preference: INTEGER Value to indicate the preference selected:
                            0 - Adjacency
                            1 - minimum Time
                            2 - minimum Distance
                            3 - minimum Transfers
        Returns:
            list_of_path[0] (Path Class): The route that goes from origin_id
            to destination_id
    """
    origin_stations = coord2station(origin_coor, map)
    destin_stations = coord2station(destin_coor, map)
    open_paths = []
    list_of_solutions = []
    for destination in destin_stations:
        print("Desti: ",destination,"\n")
        for origin_id in origin_stations:
            new_path = Path(origin_id)
            open_paths.append(new_path)
        while open_paths[-1].last != destination and open_paths != []:
            head_path = open_paths[-1]
            open_paths.pop()
            expanded_paths = expand(head_path, map)
            expanded_paths = remove_cycles(expanded_paths)
            expanded_paths = calculate_cost(expanded_paths, map, type_preference)
            expanded_paths = calculate_heuristics(expanded_paths, map, destination, type_preference)
            expanded_paths = update_f(expanded_paths)
            open_paths = insert_cost_f(expanded_paths, open_paths)
            open_paths = remove_cycles(open_paths)
        if open_paths:
            list_of_solutions.append([open_paths[-1]][0])
        open_paths=[]
        print("\n\n")
    if list_of_solutions:
        mincost = 1000000
        for solution in list_of_solutions:
            if solution.g<mincost:
                best_solution=solution
        return best_solution
    else:
        return "No existeix solució"
