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

graph2 = {
    200: [ (350, 'right', 236), (875, 'straight',235)],
    236: [ (700,'straight',237),(350,'straight',200)],
    237: [ (700,'straight',236)],
    235: [ (875,'straight',200),(523,'straight',234)],
    234: [ (523,'straight',235),(150,'straight',233)],
    233: [ (150,'straight',234),(1400,'straight',232)],
    232: [ (625,'straight',204),(1400,'straight',233),(1050,'straight',226)],
    204: [ (625,'straight',232)],
    226: [(625,'straight',203),(1050,'straight',232),(1050,'straight',227)],
    203: [ (625,'straight',226)],
    227: [ (150,'straight',228),(1050,'straight',226)],
    228: [(150,'straight',227),(529,'straight',229)],
    229: [(875,'straight',210),(529,'straight',228)],
    210: [(875,'straight',229),(1050,'straight',230)],
    230: [(1050,'straight',210)]
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
