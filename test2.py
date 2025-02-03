import heapq

# Define graphs for different floors
graphs = {
    "g1010": {  # Floor 1 of Building 1
        101001: [(3, "right", 101002), (10, "stairs", 102001)],  
        101002: [(3, "left", 101001), (4, "right", 101003)],  
        101003: [(4, "left", 101002)],  
    },
    "g1020": {  # Floor 2 of Building 1
        102001: [(10, "stairs", 101001), (5, "right", 102002)],  
        102002: [(5, "left", 102001), (6, "right", 102003)],  
        102003: [(6, "left", 102002)],  
    }
}


inter_floor_links = {
    (101001, 102001): 10, 
    (102001, 101001): 10, 
}


def dijkstra(graph, start, end):
    pq = [] 
    heapq.heappush(pq, (0, start))  
    
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    
    previous_nodes = {node: None for node in graph}

    while pq:
        current_distance, current_node = heapq.heappop(pq)

        if current_node == end:
            break  

        for distance, direction, neighbor in graph.get(current_node, []):
            if neighbor not in distances:
                continue  # Skip if neighbor is not in the current floor graph

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

    return path if path[0] == start else None  

# Function to find the shortest path across floors if needed
def find_shortest_path(source, destination):
    source_building = str(source)[:2]
    source_floor = str(source)[2:4]
    dest_building = str(destination)[:2]
    dest_floor = str(destination)[2:4]

    # If source and destination are on the same floor, use normal Dijkstra
    if source_building == dest_building and source_floor == dest_floor:
        return dijkstra(graphs[f"g{source_building}{source_floor}"], source, destination)

    # If source and destination are on different floors of the same building
    if source_building == dest_building:
        best_path = None
        best_cost = float("inf")

        for (stair_entry, stair_exit), stair_cost in inter_floor_links.items():
            if str(stair_entry)[:4] == f"{source_building}{source_floor}" and str(stair_exit)[:4] == f"{dest_building}{dest_floor}":
                
                path_to_stair = dijkstra(graphs[f"g{source_building}{source_floor}"], source, stair_entry)
                if not path_to_stair:
                    continue  

                path_from_stair = dijkstra(graphs[f"g{dest_building}{dest_floor}"], stair_exit, destination)
                if not path_from_stair:
                    continue  

                total_cost = len(path_to_stair) + stair_cost + len(path_from_stair)

                if total_cost < best_cost:
                    best_cost = total_cost
                    best_path = path_to_stair + path_from_stair

        return best_path if best_path else None

    return None  # No path found if buildings are different

# Example: Find the shortest path from 101001 (Floor 1) to 102002 (Floor 2)
source_node = 101001  
dest_node = 102002  

shortest_path = find_shortest_path(source_node, dest_node)
print("Shortest Path:", shortest_path)
