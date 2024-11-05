from flask import Flask, render_template, request, jsonify
import heapq

app = Flask(__name__)

# Define the graph
graph = {
    0: [ ( 1136, 'right', 22), (250, 'straight',23)],
    1: [(1175, 'straight', 2)],
    2: [(1032, 'right', 3), (1032, 'left', 4), (775, 'straight', 5), (1175, 'straight',1)],
    3: [(1032, 'straight', 2)],
    4: [(1032, 'straight', 2)],
    5: [(250, 'left', 20), (250,'right', 6),(775,'straight',2)],
    6: [(880, 'straight', 7), (250, 'left', 5)],
    7: [(523, 'straight', 8), (880, 'straight', 6)],
    8: [(523, 'straight', 7), (1136, 'straight', 9), (1050, 'straight', 10)],
    9: [(1136, 'right', 8), (250, 'straight', 10)],
    10: [(250, 'straight', 9), (1050, 'left', 8)],
    20: [ (250, 'right', 5), (880, 'straight', 21)],
    21: [ ( 880, 'straight', 20), (350, 'straight', 22)],
    22: [ ( 350, 'straight', 21), (1136, 'straight', 23), (1136, 'straight', 0)],
    23: [ ( 1136, 'left', 22), (250, 'straight',0)]
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
