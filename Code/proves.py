import os
from utils import *
from SearchAlgorithm import *
from TestCases import *

def cost_de_zero(cami, mapa, mode):
    cost = 0
    for i in range(len(cami.route)-1):
        myPath=Path([cami.route[i],cami.route[i+1]])
        cost += calculate_cost([myPath], mapa, mode)[0].g
    return cost

ROOT_FOLDER = '../CityInformation/'
myMap = read_station_information(os.path.join(ROOT_FOLDER, 'Stations.txt'))
connections = read_cost_table(os.path.join(ROOT_FOLDER, 'Time.txt'))
myMap.add_connection(connections)
infoVelocity_clean = read_information(os.path.join(ROOT_FOLDER, 'InfoVelocity.txt'))
myMap.add_velocity(infoVelocity_clean)

#exemple cost des de zero
# mypath = Path([6,5,4,3])
# cost = cost_de_zero(mypath, myMap, 2)
# cost+=euclidean_dist([175,98],[293,101])
# print(cost)

# -------------------------------
# case 1, expand() works just fine
# -------------------------------
# expanded_paths = expand(Path(7), myMap)
# good_paths = [Path([7, 6]), Path([7, 8])]
# expanded_paths = expand(Path([13, 12]), myMap)
# good_paths =  [Path([13, 12, 8]), Path([13, 12, 11]), Path([13, 12, 13])]
# expanded_paths = expand(Path([14, 13, 8, 12]), myMap)
# good_paths = [Path([14, 13, 8, 12, 8]),Path([14, 13, 8, 12, 11]),Path([14, 13, 8, 12, 13])]

# -------------------------------
# case 2, remove_cycles() works just fine
# -------------------------------
# my_paths = expand(Path(7), myMap)
# my_paths = remove_cycles(my_paths)
# good_paths = [Path([7, 6]), Path([7, 8])]
# my_paths = expand(Path([13, 12]), myMap)
# my_paths = remove_cycles(my_paths)
# good_paths = [Path([13, 12, 8]), Path([13, 12, 11])]
# my_paths = expand(Path([14, 13, 8, 12]), myMap)
# my_paths = remove_cycles(my_paths)
# good_paths = [Path([14, 13, 8, 12, 11])]

# -------------------------------
# case 3, depth_first_search() works like a charm
# -------------------------------
# my_paths = depth_first_search(2, 7, myMap)
# good_paths = [Path([2, 5, 6, 7])]
# my_paths = depth_first_search(13, 1, myMap)
# good_paths = [Path([13, 8, 7, 6, 5, 2, 1])]
# my_paths = depth_first_search(5, 12, myMap)
# good_paths = [Path([5, 2, 10, 11, 12])]
# my_paths = depth_first_search(14, 10, myMap)
# good_paths = [Path([14, 13, 8, 7, 6, 5, 2, 10])]

# -------------------------------
# case 4, breadth_first_search() works fine too
# -------------------------------
# my_paths = breadth_first_search(2, 7, myMap)
# good_paths = [Path([2, 5, 6, 7])]
# my_paths = breadth_first_search(13, 1, myMap)
# good_paths = [Path([13, 12, 11, 10, 2, 1])]
# my_paths = breadth_first_search(5, 12, myMap)
# good_paths = [Path([5, 10, 11, 12])]
# my_paths = breadth_first_search(14, 10, myMap)
# good_paths = [Path([14, 13, 12, 11, 10])]

# print_list_of_path([breadth_first_search(9,4,myMap)])


# -------------------------------
# case 5, calculate_cost() works fine!
# -------------------------------
#optimal_path = breadth_first_search(21, 16, myMap)

optimal_path = Astar([91, 163], [293, 101], myMap, 2)

#exemple cost des de zero
# mypath = Path([5,4,3,2,1,7,8])
# cost = cost_de_zero(mypath, myMap, 2)
# print(cost)

# my_paths = []
# good_paths = []
# print("#############\nRoute1 test\n#############")
print("Camí que he trobat:")
# print_list_of_path([optimal_path])
print_list_of_path_with_cost([optimal_path])
# print("Hauria de ser:")
# print_list_of_path(good_paths)
