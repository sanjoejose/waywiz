from flask import Flask, render_template, request, jsonify
import heapq

app = Flask(__name__)

# Define the graph
g1 = {
    100: [ ( 1136, 'right', 122), (250, 'straight',123), (200, 'up',200)],
    101: [(1175, 'straight', 102)],
    102: [(1032, 'right', 103), (1032, 'left', 104), (775, 'straight', 105), (1175, 'straight',101)],
    103: [(1032, 'straight', 102), (200, 'up', 203)],
    104: [(1032, 'straight', 102), (200, 'up',204)],
    105: [(250, 'left', 120), (250,'right', 106),(775,'straight',102)],
    106: [(880, 'straight', 107), (250, 'left', 105)],
    107: [(523, 'straight', 108), (880, 'straight', 106)],
    108: [(523, 'straight', 107), (1136, 'straight', 109), (1050, 'straight', 110)],
    109: [(1136, 'right', 108), (250, 'straight', 110)],
    110: [(250, 'straight', 109), (1050, 'left', 108), (200, 'up',210)],
    120: [ (250, 'right', 105), (880, 'straight', 121)],
    121: [ ( 880, 'straight', 120), (350, 'straight', 122)],
    122: [ ( 350, 'straight', 121), (1136, 'straight', 123), (1136, 'straight', 100)],
    123: [ ( 1136, 'left', 122), (250, 'straight',100)]
}

g2 = {
    200: [ (350, 'right', 236), (875, 'straight',235), (200, 'down',100)],
    236: [ (700,'straight',237),(350,'straight',200)],
    237: [ (700,'straight',236)],
    235: [ (875,'straight',200),(523,'straight',234)],
    234: [ (523,'straight',235),(150,'straight',233)],
    233: [ (150,'straight',234),(1400,'straight',232)],
    232: [ (625,'straight',204),(1400,'straight',233),(1050,'straight',226)],
    204: [ (625,'straight',232),(200, 'down',104)],
    226: [(625,'straight',203),(1050,'straight',232),(1050,'straight',227)],
    203: [ (625,'straight',226), (200, 'down',103)],
    227: [ (150,'straight',228),(1050,'straight',226)],
    228: [(150,'straight',227),(529,'straight',229)],
    229: [(875,'straight',210),(529,'straight',228)],
    210: [(875,'straight',229),(1050,'straight',230),(200,'down',110)],
    230: [(1050,'straight',210)]
}

unified_graph = {**g1, **g2}
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
print(shortest_path(unified_graph,107,235))

# API endpoint
@app.route('/shortest-path', methods=['POST']) 
def get_shortest_path():
    data = request.json
    start = int(data.get('start'))
    end = int(data.get('end'))
    total_distance, path_taken, directions_taken = shortest_path(unified_graph, start, end)
    
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
