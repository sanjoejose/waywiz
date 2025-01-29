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





g1 = {
    101000: [(1325, 'straight', 101003)],
    101001: [(175, 'right', 101005),(120, 'right', 101048),(875, 'straight', 101007)],
    101002: [(525, 'right', 101003),(525, 'left', 101005),(50, 'up', 102002)],
    101003: [(1325, 'straight', 101000),(525, 'left', 101002),(525, 'straight', 101004),(462, 'straight', 101005)],
    101004: [(525, 'straight', 101003),(525, 'right', 101005),(50, 'up', 102004)],
    101005: [(175, 'left', 101001),(525, 'right', 101002),(462, 'straight', 101003),(525, 'left', 101004),(325, 'right', 101051),(325, 'right', 101007),(700, 'left', 101006)],
    101006: [(700, 'right', 101005),(850, 'left', 101049),(875, 'straight', 101051),(295, 'left', 101048),(1225, 'straight', 101007),(875, 'straight', 101030)],
    101007: [(875, 'straight', 101001),(325, 'left', 101005),(1225, 'straight', 101006),(350, 'right', 101029),(700, 'straight', 101008),(612, 'left', 101026)],
    101008: [(700, 'straight', 101007),(100, 'left', 101052),(1397, 'straight', 101009),(175, 'right', 101026)],
    101009: [(175, 'right', 101085),(1397, 'straight', 101008),(525, 'right', 101010),(1400, 'straight', 101011),(873, 'right', 101052),(700, 'left', 101013)],
    101010: [(525, 'left', 101009),(875, 'right', 101011),(50, 'up', 102010)],
    101011: [(1400, 'left', 101009),(875, 'left', 101010),(700, 'right', 101013)],
    101013: [(700, 'right', 101009),(700, 'left', 101011)],
    101026: [(612, 'right', 101007),(175, 'left', 101008)],
    101029: [(350, 'left', 101007),(120, 'right', 101051)],
    101030: [(875, 'straight', 101006),(100, 'right', 101050),(643, 'straight', 101031),(120, 'left', 101049)],
    101031: [(643, 'left', 101030),(785, 'right', 101050),(525, 'left', 101032),(700, 'right', 101035),(1400, 'straight', 101033)],
    101032: [(525, 'right', 101031),(787, 'left', 101033),(50, 'up',102032)],
    101033: [(1400, 'straight', 101031),(787, 'right', 101032),(350, 'straight', 101035)],
    101035: [(700, 'left', 101031),(350, 'straight', 101033)],
    101048: [(120, 'left', 101001),(295, 'right', 101006)],
    101049: [(850, 'right', 101006),(120, 'right', 101030)],
    101050: [(100, 'left', 101030),(785, 'left', 101031)],
    101051: [(325, 'left', 101005),(875, 'straight', 101006),(120, 'left', 101029)],
    101052: [(100, 'right', 101008),(873, 'left', 101009)]
}


g2 = {
    102000: [ (300, 'right', 202), (700, 'right',203)],
    102001: [ (462, 'right', 202), (287, 'left', 219)],
    102002: [ (462, 'left', 201), (300, 'left', 200), (50, 'up', 302), (50, 'down', 102)],
    102003: [ (162, 'right', 206), (287, 'left then right', 207), (700, 'left', 200), (287, 'left then right', 219)],
    102004: [ (300, 'right', 206), (462, 'right', 205), (50, 'up', 304), (50, 'down', 104)],
    102005: [ (287, 'right', 207), (462, 'left', 204)],
    102006: [ (162, 'left', 203), (300, 'left', 204)],
    102007: [ (350, 'straight', 208), (287, 'left', 205), (287, 'right then left', 203)],
    102008: [ (700, 'straight', 209), (850, 'left', 218), (350, 'straight', 207)],
    102009: [ (261, 'straight', 211), (321, 'left', 217), (350, 'right', 218), (700, 'straight', 208)],
    102010: [ (700, 'left', 212), (350, 'right', 213), (50, 'up', 310), (50, 'down', 110)],
    102011: [ (675, 'straight', 212), (700, 'left', 216), (300, 'right', 217), (261, 'straight', 209)],
    102012: [ (1050, 'straight', 213), (700, 'right', 216), (700, 'right', 210), (675, 'straight', 211)],
    102013: [ (525, 'left', 214), (925, 'straight', 215), (350, 'left', 210), (1050, 'straight', 212)],
    102014: [ (175, 'left', 215), (525, 'right', 213)],
    102015: [ (925, 'straight', 213), (175, 'right', 214)],
    102016: [ (700, 'right', 211), (700, 'left', 212)],
    102017: [ (321, 'right', 209), (300, 'left', 211)],
    102018: [ (850, 'right', 208), (350, 'left', 209)],
    102019: [ (287, 'right then left', 203), (150, 'straight', 220), (287, 'right', 201)],
    102020: [ (875, 'right', 230), (700, 'straight', 221), (150, 'straight', 219)],
    102021: [ (543, 'straight', 222), (400, 'left', 230), (500, 'right', 229), (700, 'straight', 220)],
    102022: [ (750, 'straight', 223), (550, 'right', 228), (543, 'straight', 221)],
    102023: [ (700, 'left', 228), (700, 'straight', 224), (700, 'left', 232), (750, 'straight', 222)],
    102024: [ (700, 'right', 227), (500, 'straight', 225), (200, 'right', 232), (700, 'straight', 223)],
    102025: [ (450, 'straight', 226), (500, 'left', 227), (500, 'straight', 224)],
    102026: [ (450, 'straight', 225)],
    102027: [ (700, 'left', 224), (500, 'right', 225)],
    102028: [ (550, 'left', 222), (700, 'right', 223)],
    102029: [ (500, 'left', 221)],
    102030: [ (875, 'left', 220), (400, 'right', 221)],
    102032: [ (700, 'right', 223), (200, 'left', 224),(50, 'up', 332), (50, 'down', 132)],
}