from flask import Flask, render_template, request, jsonify
import heapq

app = Flask(__name__)

# Define the graph
graph = {
    0: [ ( 1136, 'right', 22), (250, 'straight',23)],
    1: [(1175, 'straight', 2)],
    2: [(1032, 'right', 3), (1032, 'left', 4), (775, 'straight', 5), (1175, 'straight',1)],
    3: [(1032, 'straight', 2)],
    4: [(1032, 'straight', 2), (250, 'left', 0)],
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

graph2 = {
    100: [ (350, 'right', 136), (875, 'straight',135)],
    136: [ (700,'straight',137),(350,'straight',0)],
    137: [ (700,'straight',136)],
    135: [ (875,'straight',0),(523,'straight',134)],
    134: [ (523,'straight',135),(150,'straight',133)],
    133: [ (150,'straight',134),(1400,'straight',132)],
    132: [ (625,'straight',4),(1400,'straight',133),(1050,'straight',126)],
    4: [ (625,'straight',132)],
    126: [(625,'straight',3),(1050,'straight',132),(1050,'straight',127)],
    3: [ (625,'straight',126)],
    127: [ (150,'straight',128),(1050,'straight',126)],
    128: [(150,'straight',127),(529,'straight',129)],
    129: [(875,'straight',110),(529,'straight',128)],
    110: [(875,'straight',129),(1050,'straight',130)],
    130: [(1050,'straight',110)]
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
def home():
    return render_template('land.html')  # Your main HTML page

@app.route('/select')
def select():
    return render_template('sam.html')

@app.route('/staff-login')
def staff_login():
    return render_template('login.html')

@app.route('/path-finder')
def path_finder():
    return render_template('path.html')

@app.route('/availability-status')
def availability_status():
    return render_template('availability-status.html')

@app.route('/toggle')
def toggle():
    return render_template('tog.html')

@app.route('/sign-up')
def sign_up():
    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)
