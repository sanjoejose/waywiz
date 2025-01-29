import sys

def dijkstra_multi_target(G, sources, targets):
    L = []  # List to store paths for each source-target pair

    for S, T in zip(sources, targets):
        n = len(G)  # Number of nodes in the graph
        distance = [sys.maxsize] * n  # Initialize distances to infinity
        previous = [None] * n  # Stores previous nodes for path reconstruction
        used = [False] * n  # Tracks visited nodes

        distance[S] = 0  # Source node has zero distance

        while True:
            min_distance = sys.maxsize
            min_node = None

            # Find the unvisited node with the smallest distance
            for m in range(n):
                if not used[m] and distance[m] < min_distance:
                    min_distance = distance[m]
                    min_node = m

            if min_distance == sys.maxsize:  # No more reachable nodes
                break

            used[min_node] = True

            # Update distances to neighbors
            for l in range(n):
                if G[min_node][l] > 0:  # Check if edge exists
                    shortest_to_min_node = distance[min_node]
                    distance_to_next_node = G[min_node][l]
                    total_distance = shortest_to_min_node + distance_to_next_node

                    if total_distance < distance[l]:
                        distance[l] = total_distance
                        previous[l] = min_node

        # If target node is unreachable, return None
        if distance[T] == sys.maxsize:
            return None

        # Reconstruct the shortest path
        current_node = T
        nodes_path = []
        while current_node is not None:
            nodes_path.append(current_node)
            current_node = previous[current_node]

        nodes_path.reverse()  # Reverse to get correct path order

        # Append path to result list
        L.append(nodes_path)

    return L  # Return all paths found
