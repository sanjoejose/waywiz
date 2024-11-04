from flask import Flask, render_template, request, jsonify
import heapq

app = Flask(__name__)

# Define the graph
graph = {
    0: [(1, 'right', 22), (1, 'straight', 23)],
    1: [(1, 'straight', 2)],
    2: [(1, 'right', 3), (1, 'left', 4), (1, 'straight', 5), (1, 'straight', 1)],
    3: [(1, 'straight', 2)],
    4: [(1, 'straight', 2)],
    5: [(1, 'left', 20), (1, 'right', 6), (1, 'straight', 2)],
    6: [(1, 'straight', 7), (1, 'left', 5)],
    7: [(1, 'straight', 8), (1, 'straight', 6)],
    8: [(1, 'straight', 7), (1, 'straight', 9), (1, 'straight', 10)],
    9: [(1, 'right', 8), (1, 'straight', 10)],
    10: [(1, 'straight', 9), (1, 'left', 8)],
    20: [(1, 'right', 5), (1, 'straight', 21)],
    21: [(1, 'straight', 20), (1, 'straight', 22)],
    22: [(1, 'straight', 21), (1, 'straight', 23), (1, 'straight', 0)],
    23: [(1, 'left', 22), (1, 'straight', 0)]
}

# Shortest path function
def shortest_path(graph, start, end):
    queue = [(0, start, [], [])]
    visited = set()
    
    while queue:
        (cost, node, path, directions) = heapq.heappop(queue)
        
        if node in visited:
            continue
        visited.add(node)
        
        path = path + [node]
        
        if node == end:
            return cost, path, directions
        
        for distance, direction, next_node in graph.get(node, []):
            if next_node not in visited:
                heapq.heappush(queue, (cost + distance, next_node, path, directions + [direction]))
    
    return float("inf"), [], []

# API endpoint
@app.route('/shortest-path', methods=['POST'])
def get_shortest_path():
    data = request.json
    start = int(data.get('start'))
    end = int(data.get('end'))
    total_distance, path_taken, directions_taken = shortest_path(graph, start, end)
    
    return jsonify({
        'distance': total_distance,
        'path': path_taken,
        'directions': directions_taken
    })

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
