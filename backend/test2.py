# Define the graph with nodes as a matrix of (distance, direction, next node)
# Example: graph[node] = [(distance, direction, next_node), ...]
graph = {
    0: [ ( 1, 'right', 22), (1, 'straight',23)],
    1: [(1, 'straight', 2)],
    2: [(1, 'right', 3), (1, 'left', 4), (1, 'straight', 5), (1, 'straight',1)],
    3: [(1, 'straight', 2)],
    4: [(1, 'straight', 2)],
    5: [(1, 'left', 20), (1,'right', 6),(1,'straight',2)],
    6: [(1, 'straight', 7), (1, 'left', 5)],
    7: [(1, 'straight', 8), (1, 'straight', 6)],
    8: [(1, 'straight', 7), (1, 'straight', 9), (1, 'straight', 10)],
    9: [(1, 'right', 8), (1, 'straight', 10)],
    10: [(1, 'straight', 9), (1, 'left', 8)],
    20: [ (1, 'right', 5), (1, 'straight', 21)],
    21: [ ( 1, 'straight', 20), (1, 'straight', 22)],
    22: [ ( 1, 'straight', 21), (1, 'straight', 23), (1, 'straight', 0)],
    23: [ ( 1, 'left', 22), (1, 'straight',0)]
}

def shortest_path(graph, start, end):
    import heapq
    # Priority queue to store (cost, current_node, path, directions)
    queue = [(0, start, [], [])]
    visited = set()

    while queue:
        (cost, node, path, directions) = heapq.heappop(queue)
        
        # Skip the node if it's already visited
        if node in visited:
            continue
        visited.add(node)
        
        # Update path
        path = path + [node]
        
        # Check if the destination is reached
        if node == end:
            return cost, path, directions
        
        # Explore neighbors
        for distance, direction, next_node in graph.get(node, []):
            if next_node not in visited:
                # Add direction to the directions list
                heapq.heappush(queue, (cost + distance, next_node, path, directions + [direction]))
    
    return float("inf"), [], []  # If there's no path from start to end

# Example usage
start_node = 1
end_node = 23
total_distance, path_taken, directions_taken = shortest_path(graph, start_node, end_node)

# Print the results
print(f"Shortest path from {start_node} to {end_node}: {path_taken} with total distance {total_distance}")
print("Directions:")
for i in range(len(directions_taken)):
    print(f"Step {i+1}: Go {directions_taken[i]}")
