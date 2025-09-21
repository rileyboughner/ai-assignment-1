from collections import deque
import heapq

def load_romania_graph():
    graph = {
        'Arad': {'Zerind': 75, 'Sibiu': 140, 'Timisoara': 118},
        'Zerind': {'Arad': 75, 'Oradea': 71},
        'Oradea': {'Zerind': 71, 'Sibiu': 151},
        'Timisoara': {'Arad': 118, 'Lugoj': 111},
        'Lugoj': {'Timisoara': 111, 'Mehadia': 70},
        'Mehadia': {'Lugoj': 70, 'Drobeta': 75},
        'Drobeta': {'Mehadia': 75, 'Craiova': 120},
        'Craiova': {'Drobeta': 120, 'Rimnicu Vilcea': 146, 'Pitesti': 138},
        'Sibiu': {'Arad': 140, 'Oradea': 151, 'Fagaras': 99, 'Rimnicu Vilcea': 80},
        'Rimnicu Vilcea': {'Sibiu': 80, 'Craiova': 146, 'Pitesti': 97},
        'Fagaras': {'Sibiu': 99, 'Bucharest': 211},
        'Pitesti': {'Rimnicu Vilcea': 97, 'Craiova': 138, 'Bucharest': 101},
        'Bucharest': {'Fagaras': 211, 'Pitesti': 101, 'Giurgiu': 90, 'Urziceni': 85},
        'Giurgiu': {'Bucharest': 90},
        'Urziceni': {'Bucharest': 85, 'Vaslui': 142, 'Hirsova': 98},
        'Hirsova': {'Urziceni': 98, 'Eforie': 86},
        'Eforie': {'Hirsova': 86},
        'Vaslui': {'Urziceni': 142, 'Iasi': 92},
        'Iasi': {'Vaslui': 92, 'Neamt': 87},
        'Neamt': {'Iasi': 87}
    }
    return graph

def load_sld_to_bucharest():
    sld = {
        'Arad': 366,
        'Bucharest': 0,
        'Craiova': 160,
        'Drobeta': 242,
        'Eforie': 161,
        'Fagaras': 176,
        'Giurgiu': 77,
        'Hirsova': 151,
        'Iasi': 226,
        'Lugoj': 244,
        'Mehadia': 241,
        'Neamt': 234,
        'Oradea': 380,
        'Pitesti': 100,
        'Rimnicu Vilcea': 193,
        'Sibiu': 253,
        'Timisoara': 329,
        'Urziceni': 80,
        'Vaslui': 199,
        'Zerind': 374
    }
    return sld

def bfs(graph, start, goal):
    visited = set([start])
    queue = deque([(start, [start], 0)])  # (city, path_so_far, cost_so_far)

    nodes_expanded = 0
    max_fringe = 1

    while queue:
        max_fringe = max(max_fringe, len(queue))
        city, path, cost = queue.popleft()
        nodes_expanded += 1

        if city == goal:
            return path, cost, nodes_expanded, max_fringe

        for neighbor, edge_cost in graph[city].items():
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor], cost + edge_cost))

    return [], float("inf"), nodes_expanded, max_fringe

def dfs(graph, start, goal):
    visited = set([start])
    stack = [(start, [start], 0)]  # (city, path_so_far, cost_so_far)

    nodes_expanded = 0
    max_fringe = 1

    while stack:
        max_fringe = max(max_fringe, len(stack))
        city, path, cost = stack.pop()
        nodes_expanded += 1

        if city == goal:
            return path, cost, nodes_expanded, max_fringe

        for neighbor, edge_cost in graph[city].items():
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append((neighbor, path + [neighbor], cost + edge_cost))

    return [], float("inf"), nodes_expanded, max_fringe

def greedy_best_first(graph, start, goal, heuristic):
    visited = set([start])
    fringe = [(heuristic(start), start, [start], 0)]  # (h, city, path, cost)

    nodes_expanded = 0
    max_fringe = 1

    while fringe:
        max_fringe = max(max_fringe, len(fringe))
        h, city, path, cost = heapq.heappop(fringe)
        nodes_expanded += 1

        if city == goal:
            return path, cost, nodes_expanded, max_fringe

        for neighbor, edge_cost in graph[city].items():
            if neighbor not in visited:
                visited.add(neighbor)
                heapq.heappush(fringe, (heuristic(neighbor), neighbor, path + [neighbor], cost + edge_cost))

    return [], float("inf"), nodes_expanded, max_fringe

def a_star(graph, start, goal, heuristic):
    visited = set()
    fringe = [(heuristic(start), 0, start, [start])]  # (f, g, city, path)

    nodes_expanded = 0
    max_fringe = 1

    while fringe:
        max_fringe = max(max_fringe, len(fringe))
        f, g, city, path = heapq.heappop(fringe)
        nodes_expanded += 1

        if city == goal:
            return path, g, nodes_expanded, max_fringe

        if city in visited:
            continue
        visited.add(city)

        for neighbor, edge_cost in graph[city].items():
            if neighbor not in visited:
                new_g = g + edge_cost
                new_f = new_g + heuristic(neighbor)
                heapq.heappush(fringe, (new_f, new_g, neighbor, path + [neighbor]))

    return [], float("inf"), nodes_expanded, max_fringe

def heuristic_bucharest(city, sld):
    return sld.get(city, float("inf"))

def heuristic_abs_diff(city, goal, sld):
    return abs(sld.get(city, float("inf")) - sld.get(goal, float("inf")))

def main():
    graph = load_romania_graph()
    sld = load_sld_to_bucharest()

    start = "Arad"
    goal = "Bucharest"

    print("Start:", start)
    print("Goal:", goal)

    # Test BFS
    path, cost, expanded, max_fringe = bfs(graph, start, goal)
    print("\nBFS Result")
    print("Path:", path)
    print("Cost:", cost)
    print("Nodes expanded:", expanded)
    print("Max fringe size:", max_fringe)

    # Test DFS
    path, cost, expanded, max_fringe = dfs(graph, start, goal)
    print("\nDFS Result")
    print("Path:", path)
    print("Cost:", cost)
    print("Nodes expanded:", expanded)
    print("Max fringe size:", max_fringe)

    # Greedy Best-First (Bucharest goal)
    path, cost, expanded, max_fringe = greedy_best_first(
        graph, start, goal, lambda city: heuristic_bucharest(city, sld)
    )
    print("\nGreedy Best-First Result (Bucharest goal)")
    print("Path:", path)
    print("Cost:", cost)
    print("Nodes expanded:", expanded)
    print("Max fringe size:", max_fringe)

    # A* (Bucharest goal)
    path, cost, expanded, max_fringe = a_star(
        graph, start, goal, lambda city: heuristic_bucharest(city, sld)
    )
    print("\nA* Result (Bucharest goal)")
    print("Path:", path)
    print("Cost:", cost)
    print("Nodes expanded:", expanded)
    print("Max fringe size:", max_fringe)

    # Example test with non-Bucharest goal using abs-diff heuristic
    new_goal = "Sibiu"
    path, cost, expanded, max_fringe = a_star(
        graph, start, new_goal, lambda city: heuristic_abs_diff(city, new_goal, sld)
    )
    print(f"\nA* Result (non-Bucharest goal = {new_goal})")
    print("Path:", path)
    print("Cost:", cost)
    print("Nodes expanded:", expanded)
    print("Max fringe size:", max_fringe)


if __name__ == "__main__":
    main()
