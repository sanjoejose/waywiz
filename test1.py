import heapq


graphs = {
    "g1010": {  
        101001: [(5, "right", 101002), (10, "stairs", 102001)],  
        101002: [(5, "left", 101001)],
    },
    "g1020": {  
        102001: [(10, "stairs", 101001), (5, "right", 102002)],
        102002: [(5, "left", 102001)],
    }
}


inter_floor_links = {
    (101001, 102001): 10,  
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
            new_distance = current_distance + distance
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(pq, (new_distance, neighbor))

    
    path = []
    node = end
    while node is not None:
        path.insert(0, node)
        node = previous_nodes[node]

    return path if path[0] == start else None  


def find_shortest_path(source, destination):
    source_building = str(source)[:2]
    source_floor = str(source)[2:4]
    dest_building = str(destination)[:2]
    dest_floor = str(destination)[2:4]

    
    if source_building == dest_building and source_floor == dest_floor:
        return dijkstra(graphs[f"g{source_building}{source_floor}"], source, destination)

    
    if source_building == dest_building:
        paths = []
        for (stairb, staire), cost in inter_floor_links.items():
            if stairb == source:
                path1 = dijkstra(graphs[f"g{source_building}{source_floor}"], source, stairb)
                path2 = dijkstra(graphs[f"g{dest_building}{dest_floor}"], staire, destination)
                if path1 and path2:
                    paths.append((path1 + path2[1:], cost + len(path1) + len(path2)))

        return min(paths, key=lambda x: x[1])[0] if paths else None

    
    return None  


source_node = 101001  
dest_node = 102002  

shortest_path = find_shortest_path(source_node, dest_node)
print("Shortest Path:", shortest_path)
