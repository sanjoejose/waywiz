import heapq

# Sample Floor Graphs (Dictionary Representation)
graphs = {
    "g1010": {  # Floor 1 of Building 01
        101001: [(5, "right", 101002), (10, "stairs", 102001)],  # Node 101001 connected to 101002 (right) & stairs to 102001
        101002: [(5, "left", 101001)],
    },
    "g1020": {  # Floor 2 of Building 01
        102001: [(10, "stairs", 101001), (5, "right", 102002)],
        102002: [(5, "left", 102001)],
    }
}

# Inter-floor Connections (elevators, stairs)
inter_floor_links = {
    (101001, 102001): 10,  # Stairs between node 101001 (floor 1) and 102001 (floor 2) with cost 10
}

# Dijkstra's Algorithm for Shortest Path
def dijkstra(graph, start, end):
    pq = []  # Priority queue for Dijkstra
    heapq.heappush(pq, (0, start))  # (cost, node)
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    previous_nodes = {node: None for node in graph}

    while pq:
        current_distance, current_node = heapq.heappop(pq)

        if current_node == end:
            break  # Destination reached

        for distance, direction, neighbor in graph.get(current_node, []):
            new_distance = current_distance + distance
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(pq, (new_distance, neighbor))

    # Reconstruct the path
    path = []
    node = end
    while node is not None:
        path.insert(0, node)
        node = previous_nodes[node]

    return path if path[0] == start else None  # Return path if found, else None

# Multi-Floor Navigation Algorithm
def find_shortest_path(source, destination):
    source_building = str(source)[:2]
    source_floor = str(source)[2:4]
    dest_building = str(destination)[:2]
    dest_floor = str(destination)[2:4]

    # Case 1: Same Floor, Same Building
    if source_building == dest_building and source_floor == dest_floor:
        return dijkstra(graphs[f"g{source_building}{source_floor}"], source, destination)

    # Case 2: Different Floors, Same Building
    if source_building == dest_building:
        paths = []
        for (start, end), cost in inter_floor_links.items():
            if start == source:
                path1 = dijkstra(graphs[f"g{source_building}{source_floor}"], source, start)
                path2 = dijkstra(graphs[f"g{dest_building}{dest_floor}"], end, destination)
                if path1 and path2:
                    paths.append((path1 + path2[1:], cost + len(path1) + len(path2)))

        return min(paths, key=lambda x: x[1])[0] if paths else None

    # Case 3: Different Buildings (Future Expansion)
    return None  # Implement later when inter-building paths are added

# Example Usage:
source_node = 101001  # Room 001, Floor 01, Building 01
dest_node = 102002  # Room 002, Floor 02, Building 01

shortest_path = find_shortest_path(source_node, dest_node)
print("Shortest Path:", shortest_path)
