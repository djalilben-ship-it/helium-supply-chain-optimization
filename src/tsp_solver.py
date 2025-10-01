# src/tsp_solver.py
from ortools.constraint_solver import pywrapcp, routing_enums_pb2
import pandas as pd
import argparse

def create_data_model(clients_file):
    df = pd.read_csv(clients_file)
    coords = df[['x', 'y']].values

    def distance(a, b):
        return ((a[0]-b[0])**2 + (a[1]-b[1])**2) ** 0.5

    n = len(coords)
    matrix = [[int(distance(coords[i], coords[j])) for j in range(n)] for i in range(n)]

    return {"distance_matrix": matrix, "num_vehicles": 1, "depot": 0}

def solve_tsp(data):
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']), data['num_vehicles'], data['depot'])
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        return data['distance_matrix'][manager.IndexToNode(from_index)][manager.IndexToNode(to_index)]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    search_params = pywrapcp.DefaultRoutingSearchParameters()
    search_params.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC

    solution = routing.SolveWithParameters(search_params)
    if solution:
        index = routing.Start(0)
        route = []
        while not routing.IsEnd(index):
            route.append(manager.IndexToNode(index))
            index = solution.Value(routing.NextVar(index))
        route.append(manager.IndexToNode(index))
        return route
    return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--clients", type=str, required=True, help="CSV file with client 'x','y' coordinates")
    args = parser.parse_args()

    data = create_data_model(args.clients)
    route = solve_tsp(data)
    print("Optimal Route:", route)
