# Search Algorithms Implementation Report

## 1. How the algorithms were implemented

**BFS** uses a queue to explore nodes level by level. It stores (city, path, cost) tuples and maintains a visited set. Finds solutions with minimum edges but not minimum cost in weighted graphs.
```python
queue = deque([(start, [start], 0)])
city, path, cost = queue.popleft()
queue.append((neighbor, path + [neighbor], cost + edge_cost))
```

**DFS** uses a stack to explore depth-first. Same data structure as BFS but processes nodes in LIFO order. Can get stuck in long paths and doesn't guarantee optimal solutions.
```python
stack = [(start, [start], 0)]
city, path, cost = stack.pop()  # LIFO instead of FIFO
```

**Greedy Best-First** uses a priority queue that always selects the node with lowest heuristic value. Fast but potentially suboptimal since it only considers the heuristic estimate.
```python
fringe = [(heuristic(start), start, [start], 0)]
h, city, path, cost = heapq.heappop(fringe)  # Always lowest h
```

**A*** combines actual cost g(n) with heuristic h(n) using f(n) = g(n) + h(n). Uses a priority queue and only marks nodes visited when expanded. Optimal with admissible heuristics.
```python
fringe = [(heuristic(start), 0, start, [start])]  # (f, g, city, path)
new_f = new_g + heuristic(neighbor)  # f = g + h
```

## 2. Description of the heuristic functions used

**Straight-Line Distance Heuristic** returns precomputed distances from any city to Bucharest (0-380 range). Admissible because straight-line distance never overestimates road distance. Perfect for Bucharest searches.
```python
def heuristic_bucharest(city, sld):
    return sld.get(city, float("inf"))
# sld = {'Arad': 366, 'Bucharest': 0, 'Pitesti': 100, ...}
```

**Absolute Difference Heuristic** calculates |distance_to_bucharest(city) - distance_to_bucharest(goal)|. Assumes cities with similar Bucharest distances are close to each other. Not admissible - can overestimate and break A* optimality.
```python
def heuristic_abs_diff(city, goal, sld):
    return abs(sld.get(city, float("inf")) - sld.get(goal, float("inf")))
# Example: |366 - 253| = 113 for Arad->Sibiu
```