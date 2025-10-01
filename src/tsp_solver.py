from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import numpy as np

# Distance matrix
distances = np.array([
    [0, 40, 41, 45, 40, 36, 31, 113, 146, 37, 185, 222, 82, 100, 35],
    [40, 0, 5.6, 2.5, 3.6, 11, 13, 70, 182, 5.6, 147, 161, 10, 94, 11],
    [41, 5.6, 0, 3.8, 3.2, 2.6, 6.7, 80, 176, 2.6, 173, 210, 98, 88, 3.7],
    [45, 2.5, 3.8, 0, 1.7, 6.6, 11, 72, 180, 3.4, 177, 163, 102, 92, 8.1],
    [40, 3.6, 3.2, 1.7, 0, 5.4, 10, 78, 178, 2.3, 176, 168, 100, 90, 7.3],
    [36, 11, 2.6, 6.6, 5.4, 0, 4.9, 82, 178, 3.2, 175, 212, 100, 90, 4.2],
    [31, 13, 6.7, 11, 10, 4.9, 0, 86, 182, 6.4, 179, 216, 104, 94, 4.3],
    [113, 70, 80, 72, 78, 82, 86, 0, 157, 82, 75, 94, 174, 63, 82],
    [146, 182, 176, 180, 178, 178, 182, 157, 0, 178, 189, 225, 77, 100, 178],
    [37, 5.6, 2.6, 3.4, 2.3, 3.2, 6.4, 82, 178, 0, 176, 212, 100, 90, 4.7],
    [185, 147, 173, 177, 176, 175, 179, 75, 189, 176, 0, 52, 199, 92, 174],
    [222, 161, 210, 163, 168, 212, 216, 94, 225, 212, 52, 0, 236, 129, 211],
    [82, 10, 98, 102, 100, 100, 104, 174, 77, 100, 199, 236, 0, 118, 104],
    [100, 94, 88, 92, 90, 90, 94, 63, 100, 90, 92, 129, 118, 0, 90],
    [35, 11, 3.7, 8.1, 7.3, 4.2, 4.3, 82, 178, 4.7, 174, 211, 104, 90, 0]
])

# Number of locations
num_locations = distances.shape[0]

# Create the routing index manager
manager = pywrapcp.RoutingIndexManager(num_locations, 1, 0)  # 1 vehicle, starting at index 0

# Create Routing Model
routing = pywrapcp.RoutingModel(manager)

# Distance callback
def distance_callback(from_index, to_index):
    from_node = manager.IndexToNode(from_index)
    to_node = manager.IndexToNode(to_index)
    return int(distances[from_node][to_node])  # OR-Tools requires integer distances

transit_callback_index = routing.RegisterTransitCallback(distance_callback)

# Set the cost function (distance)
routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

# Solve the problem
search_parameters = pywrapcp.DefaultRoutingSearchParameters()
search_parameters.first_solution_strategy = (
    routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

solution = routing.SolveWithParameters(search_parameters)

# Print solution
if solution:
    index = routing.Start(0)
    route = []
    route_distance = 0
    while not routing.IsEnd(index):
        route.append(manager.IndexToNode(index))
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    route.append(manager.IndexToNode(index))
    print("Optimal route:", route)
    print("Total distance:", route_distance)
else:
    print("No solution found!")
